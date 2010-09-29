#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import MySQLdb
import Queue
from datetime import datetime
import checkall

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

class Job(object):


    def __init__(self, Id, PortName):

        self.Id= Id
        self.PortName= PortName
        print 'Port out: ', PortName
        a = checkall.Init(PortName, Id)
        cmd = 'UPDATE Queue SET StatusBuild=1, Status=%s WHERE Id=%s' % (a, Id)
        cursor.execute(cmd)
        database.commit()
        return

    def __cmp__(self, other):
        return cmp(self.Id, other.PortName)


if __name__ == '__main__':

    queue = Queue.PriorityQueue()
    cmd = 'SELECT Id, Port FROM Queue WHERE StatusBuild=0'
    cursor.execute(cmd)
    Result = cursor.fetchall()

    for result in Result:
        if result[0] and result[1]:
            queue.put(Job(result[0], result[1]))
        else:
            pass

    while not queue.empty():
        next_job = queue.get()
        print 'Processing Port: ', next_job.PortName

