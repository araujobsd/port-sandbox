#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# checkall.py - Check all dependencies marked as any related error included in  ports.
#
# Copyright (c) 2010 Marcelo Araujo <araujo@FreeBSD.org>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# MAINTAINER = araujo@FreeBSD.org
#

import commands
import MySQLdb
import configparser

def CheckPortError(file):

    File = open(file, 'r')
    errorcontrol = 0

    for line in File:
        line = line.split(";")
        if 'Error' in line[0]:
            path = line[2].split("\n")
            errorcontrol = 1

    return errorcontrol

def NoPackage(port):

    NoPackage = commands.getstatusoutput('cd %s; make -V NO_PACKAGE' \
                                        % (port))
    NoPackage = NoPackage[1].replace('"', ' ')
    return NoPackage


def NoCdrom(port):

    NoCdrom = commands.getstatusoutput('cd %s; make -V NO_CDROM' \
                                      % (port))
    NoCdrom = NoCdrom[1].replace('"', ' ')
    return NoCdrom


def Restricted(port):

    Restricted = commands.getstatusoutput('cd %s; make -V RESTRICTED' \
                                         % (port))
    Restricted = Restricted[1].replace('"', ' ')
    return Restricted


def Forbidden(port):

    Forbidden = commands.getstatusoutput('cd %s; make -V FORBIDDEN' \
                                        % (port))
    Forbidden = Forbidden[1].replace('"', ' ')
    return Forbidden


def Broken(port):

    Broken = commands.getstatusoutput('cd %s; make -V BROKEN' \
                                     % (port))
    Broken = Broken[1].replace('"', ' ')
    return Broken


def Deprecated(port):

    Deprecated = commands.getstatusoutput('cd %s; make -V DEPRECATED' \
                                         % (port))
    Deprecated = Deprecated[1].replace('"', ' ')
    return Deprecated


def Ignore(port):

    Ignore = commands.getstatusoutput('cd %s; make -V IGNORE' \
                                     % (port))
    Ignore = Ignore[1].replace('"', ' ')
    return Ignore


def CheckPCRFBDI(Id, port,offset):

    conf = configparser.MySQL()
    host, user, password, db = conf.config()

    try:
        database = MySQLdb.connect(host, user, password)
        database.select_db(db)
        cursor = database.cursor()
    except:
        print "Error connecting to the database....\n"

    print "====> OFFSET: ",
    print port
    offset = offset.split('(')
    offset = offset[1].split(')')
    offset = offset[0].split(',')

    if int(offset[0]) == 1:
        print "No Package"
        msg = NoPackage(port)
        cmd = 'UPDATE NoBuild SET NoPackage="%s", NoPackageMsg="%s" WHERE \
               PortName="%s"' % (int(offset[0]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[1]) == 1:
        print "No Cdrom"
        msg = NoCdrom(port)
        cmd = 'UPDATE NoBuild SET NoCdrom="%s", NoCdromMsg="%s" WHERE \
               PortName="%s"' % (int(offset[1]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[2]) == 1:
        print "Restricted"
        msg = Restricted(port)
        cmd = 'UPDATE NoBuild SET Restricted="%s", RestrictedMsg="%s" WHERE \
               PortName="%s"' % (int(offset[2]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[3]) == 1:
        print "Forbidden"
        msg = Forbidden(port)
        cmd = 'UPDATE NoBuild SET Forbidden="%s", ForbiddenMsg="%s" WHERE \
               PortName="%s"' % (int(offset[3]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[4]) == 1:
        print "Broken"
        msg = Broken(port)
        cmd = 'UPDATE NoBuild SET Broken="%s", BrokenMsg="%s" WHERE \
               PortName="%s"' % (int(offset[4]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[5]) == 1:
        print "Deprecated"
        msg = Deprecated(port)
        cmd = 'UPDATE NoBuild SET Deprecated="%s", DeprecatedMsg="%s" WHERE \
               PortName="%s"' % (int(offset[5]), msg, port)
        cursor.execute(cmd)
        database.commit()

    if int(offset[6]) == 1:
        print "Ignore"
        msg = Ignore(port)
        cmd = 'UPDATE NoBuild SET Ignorec="%s", IgnoreMsg="%s" WHERE \
               PortName="%s"' % (int(offset[6]), msg, port)
        cursor.execute(cmd)
        database.commit()


