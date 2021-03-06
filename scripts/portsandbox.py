#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import MySQLdb
import Queue
import datetime
import checkall
import cleangarbage
import configparser
import os

conf = configparser.MySQL()
host, user, password, db = conf.config()

database = MySQLdb.connect(host, user, password)
database.select_db(db)
cursor = database.cursor()

class Job(object):


    def __init__(self, Id, PortName, JailId):

        self.Id= Id
        self.PortName= PortName
        print 'Port out: ', PortName
        a = checkall.Init(PortName, Id, JailId)
        cmd = 'UPDATE Queue SET StatusBuild=1, Status=%s WHERE Id=%s' % (a, Id)
        cursor.execute(cmd)
        database.commit()
        date = str(datetime.datetime.now())
        date = date.split('.')
        cmd = 'UPDATE Queue SET StartBuild="%s" WHERE Id=%s' % (date[0], Id)
        cursor.execute(cmd)
        database.commit()
        cleangarbage.CleanPreLog()
        os.system("rm -f /tmp/portsandbox.lock")

        return

    def __cmp__(self, other):
        return cmp(self.Id, other.PortName)


if __name__ == '__main__':

    queue = Queue.PriorityQueue()
    cmd = 'SELECT Id, Port, JailId FROM Queue WHERE StatusBuild=0'
    cursor.execute(cmd)
    Result = cursor.fetchall()
    os.system("touch /tmp/portsandbox.lock")

    for result in Result:
        if result[0] and result[1]:
            queue.put(Job(result[0], result[1], result[2]))
        else:
            pass

    while not queue.empty():
        next_job = queue.get()
        print 'Processing Port: ', next_job.PortName

