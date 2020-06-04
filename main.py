# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_mysql]
import os
import cherrypy
import wsgiref.handlers
import pymysql
from smartCollect import cnx,bin,trucker,usuario, database

class Interface(object):

    @cherrypy.expose
    def index(self):
        return str('Ola teste')

# [END gae_python37_cloudsql_mysql]



def CORS():
	    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

conf = {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),'tools.CORS.on': True}
        }

cherrypy.tree.mount(usuario.DataUsuario(), '/api/dataUsuario', conf)
cherrypy.tree.mount(trucker.DataTrucker(), '/api/dataTrucker', conf)
cherrypy.tree.mount(bin.DataBin(), '/api/dataBin', conf)
cherrypy.tree.mount(Interface(), '/')
cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
app = cherrypy.tree
wsgiref.handlers.CGIHandler().run(app)
