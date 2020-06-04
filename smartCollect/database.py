# -*- coding: utf-8 -*-
import string
import json
from smartCollect import cnx

def setup_database():
    """
    Criando tabela bins
    """
    with cnx.cursor() as con:
        try:
            con.execute("CREATE TABLE bins (ID varchar(255) NOT NULL, volume int, local varchar(255) NOT NULL)")
            con.execute("CREATE TABLE truckers (ID varchar(255) NOT NULL, volume int, local varchar(255) NOT NULL)")
            con.close()
        except:
            print ('already exists')
         
def cleanup_database():
    """
    Destruir tabela de bins
    """
    try:
        with cnx.cursor() as con:
            con.execute("DROP TABLE bins")
            con.execute("DROP TABLE truckers")
            cnx.commit()
        
    except:
        print ('don´t exist')
