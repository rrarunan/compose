import falcon
import services
import project
import config

from .cors import CORSMiddleware

api = application = falcon.API(middleware=CORSMiddleware())

services = services.ServiceResource()
project = project.ProjectResource()
config = config.Config()

api.add_route('/config', config)
api.add_route('/services', services)
api.add_route('/project', project)
api.add_route('/project/config', project)
