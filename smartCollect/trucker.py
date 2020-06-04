# -*- coding: utf-8 -*-
import random
import string
import json
import cherrypy

from smartCollect import cnx

class Trucker(object):
    def __init__(self):
        self.ID=""
        self.volume=""
        self.local=""
        
    def return_JSON(self):
        data = json.dumps(self.__dict__)
        return data


class DataTrucker():
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, local=None):
        if local is None:
            l=[]
            with cnx.cursor() as c:
                sql ='SELECT * FROM truckers  ORDER BY ID'
                c.execute(sql,)
                rows = c.fetchall()
            
                for row in rows:
                    trucker = Trucker()
                    trucker.ID = row[0]
                    trucker.volume = row[1]
                    trucker.local = row[2]
                    print(trucker.__dict__)
                    l.append(trucker.return_JSON())
            c.close()
            return('Truckers \n: %s' % str(l) )
        else:
            with cnx.cursor() as c:
                sql = 'SELECT * FROM truckers WHERE local like %s'
                c.execute(sql, local)
                variavel = c.fetchone()
            c.close()
            if variavel is not None:
                trucker = Trucker()
                trucker.ID = variavel[0] 
                trucker.volume = variavel[1]
                trucker.local = variavel[2]
                return(trucker.return_JSON())
            else:
                return None

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        trucker = Trucker()
        trucker.__dict__ = data
            
        with cnx.cursor() as c:
            sql = "INSERT INTO truckers  VALUES (%s, %s, %s)"
            c.execute(sql,(trucker.ID,trucker.volume,trucker.local))
        cnx.commit()
        c.close()
        return 'done'

    def DELETE(self, ID):
        with cnx.cursor() as c:
            sql = 'DELETE FROM truckers WHERE id = %s'
            c.execute(sql, (ID,))
        cnx.commit()     
        c.close()