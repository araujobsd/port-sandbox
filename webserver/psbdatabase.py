#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# By araujo@FreeBSD.org
#

import MySQLdb

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

class Select():


    def Queue(self, JailName):

        if JailName != 'None':
            cmd = 'SELECT Id, JailName FROM Jail WHERE JailName="%s"' % (JailName)
            cursor.execute(cmd)
            JailId = cursor.fetchone()

        if JailName == 'None':
            cmd = 'SELECT Id, Port, Status, JailId, StartBuild, StatusBuild FROM Queue ORDER BY Id DESC LIMIT 18'
        else:
            cmd = 'SELECT Id, Port, Status, JailId, StartBuild, StatusBuild FROM Queue WHERE JailId="%s" ORDER BY Id DESC' % (JailId[0])

        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result


    def JailName(self, JailId):

        Result = None

        if JailId == None:
            cmd = 'SELECT Id, JailName FROM Jail'
            cursor.execute(cmd)
            Result = cursor.fetchall()
        else:
            cmd = 'SELECT JailName FROM Jail WHERE Id=%s' % (JailId)
            cursor.execute(cmd)
            Result = cursor.fetchone()

        return Result


    def MainPort(self, Id):

        cmd = 'SELECT * FROM MainPort WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchone()

        return Result


    def DependsQuant(self, Table, Id):

        Quant = 0
        cmd = 'SELECT Id FROM %s WHERE Id=%s' % (Table, Id)
        cursor.execute(cmd)
        Result = cursor.fetchall()

        for result in Result:
            Quant = Quant + 1

        return Quant


    def NextInQueue(self):

        cmd = 'SELECT Port FROM Queue WHERE StatusBuild=0'
        cursor.execute(cmd)
        Result = cursor.fetchone()
        NoQueue = ['There is no PORT in the queue...']

        try:
            if Result[0]:
                return Result
        except:
            return NoQueue

    def AllPortsInQueue(self):

        cmd = 'SELECT Id, Port, JailId FROM Queue WHERE StatusBuild=0'
        cursor.execute(cmd)
        Result = cursor.fetchall()

        try:
            if Result[0]:
                return Result
        except:
            return 0

