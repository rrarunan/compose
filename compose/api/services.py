from __future__ import unicode_literals
from __future__ import absolute_import
import falcon
import json

from ..service import Service

def __init__(self, storage_path):
    self.storage_path = storage_path

# Set current docker-compose directory
class ServiceResource(object):
    def on_get(self, req, res):
        #test service
        service = Service(
            project='composetest',
            name='db',
            build='tests/fixtures/dockerfile-with-volume',
        )
        res.body = json.dumps(service.__dict__)
        res.status = falcon.HTTP_200
