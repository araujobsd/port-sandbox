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


    def Queue(self):

        cmd = 'SELECT Id, Port, Status, JailId, StartBuild, StatusBuild FROM Queue ORDER BY Id DESC LIMIT 12'
        cursor.execute(cmd)
        Result = cursor.fetchall()

        return Result


    def JailName(self, JailId):

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
