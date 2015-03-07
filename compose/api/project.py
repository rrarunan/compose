from __future__ import unicode_literals
from __future__ import absolute_import
import falcon
import copy
import json
import logging
import os
import re
import yaml
import six
import jsonpickle

from ..project import Project
from ..service import ConfigError
from ..cli.docker_client import docker_client
from ..cli import verbose_proxy
from ..cli import errors
from .. import __version__

log = logging.getLogger(__name__)

# Set current docker-compose directory
class ProjectResource(object):
    def __init__(self):
        self.project = self.get_project('../compose/api/test/docker-compose.yml')

    def update(self, config):
        self.project = self.get_project(config)

    def on_post(self, req, res):
        configJSON = req.stream.read(4096)
        print(configJSON)
        log.info("Configuring Compose Project at: %s", configJSON)
        config = jsonpickle.decode(configJSON)
        print(config['config'])
        #log.info("Configuring Compose Project at: %s", config)
        #handle errors!
        self.update(config['config'])
        res.status = falcon.HTTP_201

    def on_get(self, req, res):
        res.body = jsonpickle.encode(self.project)
        res.status = falcon.HTTP_200

    def get_client(self, verbose=False):
        client = docker_client()
        if verbose:
            version_info = six.iteritems(client.version())
            log.info("Compose version %s", __version__)
            log.info("Docker base_url: %s", client.base_url)
            log.info("Docker version: %s",
                     ", ".join("%s=%s" % item for item in version_info))
            return verbose_proxy.VerboseProxy('docker', client)
        return client

    def get_config(self, config_path):
        try:
            with open(config_path, 'r') as fh:
                return yaml.safe_load(fh)
        except IOError as e:
            raise errors.UserError(six.text_type(e))

    def get_project(self, config_path, project_name=None, verbose=False):
        try:
            return Project.from_config(
                self.get_project_name(config_path, project_name),
                self.get_config(config_path),
                self.get_client(verbose=verbose))
        except ConfigError as e:
            raise errors.UserError(six.text_type(e))

    def get_project_name(self, config_path, project_name=None):
        def normalize_name(name):
            return re.sub(r'[^a-z0-9]', '', name.lower())

        if 'FIG_PROJECT_NAME' in os.environ:
            log.warn('The FIG_PROJECT_NAME environment variable is deprecated.')
            log.warn('Please use COMPOSE_PROJECT_NAME instead.')

        project_name = project_name or os.environ.get('COMPOSE_PROJECT_NAME') or os.environ.get('FIG_PROJECT_NAME')
        if project_name is not None:
            return normalize_name(project_name)

        project = os.path.basename(os.path.dirname(os.path.abspath(config_path)))
        if project:
            return normalize_name(project)

        return 'default'

    def get_config_path(self, file_path=None):
        if file_path:
            return os.path.join(self.base_dir, file_path)

        supported_filenames = [
            'docker-compose.yml',
            'docker-compose.yaml',
            'fig.yml',
            'fig.yaml',
        ]

        def expand(filename):
            return os.path.join(self.base_dir, filename)

        candidates = [filename for filename in supported_filenames if os.path.exists(expand(filename))]

        if len(candidates) == 0:
            raise errors.ComposeFileNotFound(supported_filenames)

        winner = candidates[0]

        if len(candidates) > 1:
            log.warning("Found multiple config files with supported names: %s", ", ".join(candidates))
            log.warning("Using %s\n", winner)

        if winner == 'docker-compose.yaml':
            log.warning("Please be aware that .yml is the expected extension "
                        "in most cases, and using .yaml can cause compatibility "
                        "issues in future.\n")

        if winner.startswith("fig."):
            log.warning("%s is deprecated and will not be supported in future. "
                        "Please rename your config file to docker-compose.yml\n" % winner)

        return expand(winner)
