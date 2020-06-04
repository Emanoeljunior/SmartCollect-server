# -*- coding: utf-8 -*-
import random
import string
import json
import cherrypy

from smartCollect import cnx

class Usuario(object):
    def __init__(self):
        self.nome=""
        self.email=""
        self.senha=""
        
    def return_JSON(self):
        data = json.dumps(self.__dict__)
        return data


class DataUsuario():
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, nome=None):
        if nome is None:
            l=[]
            with cnx.cursor() as c:
                sql ='SELECT * FROM usuarios'
                c.execute(sql,)
                rows = c.fetchall()
                
                for row in rows:
                    usuario = Usuario()
                    usuario.nome = row[0]
                    usuario.email = row[1]
                    usuario.senha = row[2]
                    print(usuario.__dict__)
                    l.append(usuario.return_JSON())
            c.close()
            return( str(l) )
        else:
            with cnx.cursor() as c:
                sql = 'SELECT * FROM usuarios WHERE nome like %s'
                c.execute(sql, nome)
                variavel = c.fetchone()
            c.close()
            if variavel is not None:
                usuario = Usuario()
                usuario.nome = variavel[0] 
                usuario.email = variavel[1]
                usuario.senha = variavel[2]
                return(usuario.return_JSON())
            else:
                return None

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        usuario = Usuario()
        usuario.__dict__ = data
            
        with cnx.cursor() as c:
            sql = "INSERT INTO usuarios  VALUES (%s, %s, %s)"
            c.execute(sql,(usuario.nome,usuario.email,usuario.senha))
        cnx.commit()
        c.close()
        return 'done'

    def DELETE(self, nome):
        with cnx.cursor() as c:
            sql = 'DELETE FROM usuarios WHERE nome = %s'
            c.execute(sql, (nome,)) 
        cnx.commit()
        c.close()
                   
           