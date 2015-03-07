from __future__ import unicode_literals
from __future__ import absolute_import
import falcon
import jsonpickle

from .project import ProjectResource

# Set current docker-compose directory
class Config(object):
    def on_post(self, req, res):
        configJSON = req.stream.read(4096)
        config = jsonpickle.decode(configJSON)
        res.status = falcon.HTTP_201
