from __future__ import unicode_literals
from __future__ import absolute_import

class CORSMiddleware(object):
    def process_response(self, req, resp, resource):
        resp.set_header('ACCESS-CONTROL-ALLOW-ORIGIN', '*')
