#!/usr/local/bin/python
#
# -*- coding: utf-8 -*-
#

import MySQLdb
import ConfigParser

class MySQL:


    def config(self):

        config = ConfigParser.ConfigParser()
        config.read("conf/mysql.conf")

        host = config.get("mysql", "host")
        user = config.get("mysql", "user")
        password = config.get("mysql", "password")
        database = config.get("mysql", "database")

        return host, user, password, database
