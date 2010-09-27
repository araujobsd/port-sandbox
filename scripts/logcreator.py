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

    if LastId != None:
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
    else:
        LogFile = PathLog+ '/' + LogName

    File = open(LogFile, 'a')
    File.write("============= [ %s ] ===============\n" % (Phase))
    File.write("%s\n" % (Output))
    File.close()

def RefactoryCheckDeps(LogFile):

    Log = open(LogFile, 'r')
    List = []
    ListUniq = []
    for line in Log:
        line = line.split(';')
        if len(List) == 0:
            ToAppend = line[2]
            List.append(ToAppend)
            ToAppendUniq = line[0] + ';' + line[1] + ';' + line[2]
            ListUniq.append(ToAppendUniq)
        else:
            if line[2] in List:
                pass
            else:
                ToAppend = line[2]
                List.append(ToAppend)
                ToAppendUniq = line[0] + ';' + line[1] + ';' + line[2]
                ListUniq.append(ToAppendUniq)

    Log.close()
    print List
    print ListUniq

    LogUniq = open(LogFile, 'w')
    for line in ListUniq:
        LogUniq.write(str(line))
    LogUniq.close()
