#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import MySQLdb
import sys
import checkall
import configparser
from datetime import datetime

conf = configparser.MySQL()
host, user, password, db = conf.config()

database = MySQLdb.connect(host, user, password)
database.select_db(db)
cursor = database.cursor()

if __name__ == '__main__':

    sys_len = len(sys.argv)

    if sys_len == 4:
        cmd = 'INSERT INTO Queue (Port, StatusBuild, JailId) VALUES ("%s", "%s", "%s")' \
               % (sys.argv[2], 0, sys.argv[3])
        cursor.execute(cmd)
        database.commit()
    elif sys_len == 3:
        a = checkall.Init(sys.argv[1], None, sys.argv[2])
        print "===> Result: ",
        print a
    elif sys_len < 3:
        print 'Using ./app category/portname JailId'
        print 'Using ./app add category/portname JailId'

