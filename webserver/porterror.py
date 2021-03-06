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
        LibDepends = self.DependsErrors(MainPort[0], 'LibDepends')
        BuildDepends = self.DependsErrors(MainPort[0], 'BuildDepends')
        RunDepends = self.DependsErrors(MainPort[0], 'RunDepends')

        Dict = {"MainPort":MainPort, "LibDepends":LibDepends, "BuildDepends":BuildDepends, "RunDepends":RunDepends}

        Html = Template(file="porterror.tmpl", searchList=[Dict])

        return str(Html)


    def DependsErrors(self, Id, Table):

        cmd = 'SELECT * FROM %s WHERE Id=%s' % (Table, Id)
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result


    def NoBuild(self):

        offset = None
        cmd = 'SELECT * FROM NoBuild ORDER BY Id DESC'
        cursor.execute(cmd)
        Result = cursor.fetchall()

        cmd = 'SELECT Id, StartBuild, JailId FROM Queue'
        cursor.execute(cmd)
        Date = cursor.fetchall()

        cmd = 'SELECT * FROM Jail'
        cursor.execute(cmd)
        Jail = cursor.fetchall()

        Dict = {"NoBuild":Result, "Date":Date, "Jail":Jail}
        Html = Template(file="nobuild.tmpl", searchList=[Dict])

        return str(Html)
