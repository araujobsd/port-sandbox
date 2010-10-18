#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import cherrypy
import MySQLdb
from Cheetah.Template import Template
import psbdatabase

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

class HandleErrors():


    def MainPortErrors(self, Id):

        cmd = 'SELECT * FROM MainPort WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        MainPort = cursor.fetchone()
        LibDepends = self.LibDependsErrors(MainPort[0])
        Dict = {"MainPort":MainPort, "LibDepends":LibDepends}

        Html = Template(file="porterror.tmpl", searchList=[Dict])

        return str(Html)


    def LibDependsErrors(self, Id):

        cmd = 'SELECT * FROM LibDepends WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result
