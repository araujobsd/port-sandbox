#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#

import os
import random
import MySQLdb

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

def LogCreator(Phase, Output, PathLog, LogName, LastId):

    cmd = 'SELECT PortLog from MainPort where id=%s' % (LastId)
    cursor.execute(cmd)
    PortLog = cursor.fetchone()

    if PortLog[0] == None:
        MagicNumber = random.random()
        DirLog = 'log/' + str(MagicNumber) + '/'
        if not os.path.exists(DirLog):
            os.makedirs(DirLog)
        LogFile = DirLog + '/' + LogName
        cmd = 'UPDATE MainPort SET PortLog="%s" WHERE id=%s' \
               % (LogFile, LastId)
        cursor.execute(cmd)
        database.commit()
    else:
        LogFile = PortLog[0]

    File = open(LogFile, 'a')
    File.write("============= [ %s ] ===============\n" % (Phase))
    File.write("%s\n" % (Output))
    File.close()
