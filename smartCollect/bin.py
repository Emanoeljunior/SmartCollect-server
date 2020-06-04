# -*- coding: utf-8 -*-
import random
import string
import json
import cherrypy

from smartCollect import cnx

class Bin(object):
    def __init__(self):
        self.ID=""
        self.volume=""
        self.local=""
        
    def return_JSON(self):
        data = json.dumps(self.__dict__)
        return data


class DataBin():
    exposed = True

    @cherrypy.tools.json_out()
    def GET(self, local=None):
        if local is None:
            l=[]
            with cnx.cursor() as c:
                sql ='SELECT * FROM bins  ORDER BY ID'
                c.execute(sql,)
                rows = c.fetchall()
                
                for row in rows:
                    bin = Bin()
                    bin.ID = row[0]
                    bin.volume = row[1]
                    bin.local = row[2]
                    print(bin.__dict__)
                    l.append(bin.return_JSON())
            c.close()
            return('Bins \n: %s' % str(l) )
        else:
            with cnx.cursor() as c:
                sql = 'SELECT * FROM bins WHERE local like %s'
                c.execute(sql, local)
                variavel = c.fetchone()
            c.close()
            if variavel is not None:
                bin = Bin()
                bin.ID = variavel[0] 
                bin.volume = variavel[1]
                bin.local = variavel[2]
                return(bin.return_JSON())
            else:
                return None

    @cherrypy.tools.json_in()
    def POST(self):
        data = cherrypy.request.json
        bin = Bin()
        bin.__dict__ = data
            
        with cnx.cursor() as c:
            sql = "INSERT INTO bins  VALUES (%s, %s, %s)"
            c.execute(sql,(bin.ID,bin.volume,bin.local))
        cnx.commit()
        c.close()
        return 'done'

    def DELETE(self, ID):
        with cnx.cursor() as c:
            sql = 'DELETE FROM bins WHERE id = %s'
            c.execute(sql, (ID,))
        cnx.commit() 
        c.close()
                   
           