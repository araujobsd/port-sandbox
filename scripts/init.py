#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import MySQLdb
import sys
import checkall
from datetime import datetime

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

if __name__ == '__main__':

    sys_len = len(sys.argv)

    if sys_len == 3:
        print 'Using ./app add category/portname'
        cmd = 'INSERT INTO Queue (Port, StatusBuild) VALUES ("%s", "%s")' \
               % (sys.argv[2], 0)
        cursor.execute(cmd)
        database.commit()
    elif sys_len == 2:
        print 'Using ./app category/portname'
        checkall.Init(sys.argv[1])
    elif sys_len < 2:
        print 'Using ./app category/portname'
        print 'Using ./app add category/portname'

