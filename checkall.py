#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# checkall.py - Check all dependencies marked as any related error included in ports.
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

import sys
import commands
import shelve
import MySQLdb
import qatcheckporterror
import qatchecksum
import sql
import logcreator


PORT_PATH = '/usr/ports/'

class PortDepends:


    def Depends(self, portpath):

        path = portpath
        RunDepends = commands.getstatusoutput('cd %s; make -V RUN_DEPENDS' \
                                           % (path))
        LibDepends = commands.getstatusoutput('cd %s; make -V LIB_DEPENDS' \
                                           % (path))
        BuildDepends = commands.getstatusoutput('cd %s; make -V BUILD_DEPENDS' \
                                             % (path))
        return RunDepends, LibDepends, BuildDepends


    def ParserDependsList(self, Depends):

        DependsList = []
        depends = Depends.split(':')

        for path in depends:
            path = path.split(' ')
            if path[0] == '(0,':
                pass
            elif '\')' in path[0]:
                Refactor = path[0].split('\')')
                DependsList.append(Refactor[0])
            elif '((0,' in path[0]:
                pass
            else:
                DependsList.append(path[0])

        return DependsList


    def CheckProblems(self, port):

        Forbidden = commands.getstatusoutput('cd %s; make -V FORBIDDEN' \
                                         % (port))
        Broken = commands.getstatusoutput('cd %s; make -V BROKEN' \
                                         % (port))
        Deprecated = commands.getstatusoutput('cd %s; make -V DEPRECATED' \
                                         % (port))
        Ignore = commands.getstatusoutput('cd %s; make -V IGNORE' \
                                         % (port))

        forbidden = self.RemoveZero(Forbidden)
        broken = self.RemoveZero(Broken)
        deprecated = self.RemoveZero(Deprecated)
        ignore = self.RemoveZero(Ignore)

        return forbidden, broken, deprecated, ignore


    def CheckExtraDepends(self, port):

        Fetch = commands.getstatusoutput('cd %s; make -V FETCH_DEPENDS' \
                                        % (port))
        Extract = commands.getstatusoutput('cd %s; make -V EXTRACT_DEPENDS' \
                                        % (port))

        fetch = self.RemoveZero(Fetch)
        extract = self.RemoveZero(Extract)

        return fetch, extract


    def CheckRestrictions(self, port):

        NoPackage = commands.getstatusoutput('cd %s; make -V NO_PACKAGE' \
                                          % (port))
        NoCdrom = commands.getstatusoutput('cd %s; make -V NO_CDROM' \
                                          % (port))
        Restricted = commands.getstatusoutput('cd %s; make -V RESTRICTED' \
                                          % (port))

        nopackage = self.RemoveZero(NoPackage)
        nocdrom = self.RemoveZero(NoCdrom)
        restricted = self.RemoveZero(Restricted)

        return nopackage, nocdrom, restricted


    def RemoveZero(self, port):

        List = []

        for i in port:
            if 0 == i:
                pass
            elif not i:
                pass
            else:
                List.append(i)

        return List


class CheckPorts(PortDepends):


    def AllErrors(self, dic):

        offset = 0
        NoPackage = ""
        NoCdrom = Restricted = Forbidden = Broken = Deprecated = Ignore = NoPackage

        if dic["NoPackage"]:
            offset = 1
            NoPackage = "NoPackage: \t" + str(dic["NoPackage"])
        if dic["NoCdrom"]:
            offset = 1
            NoCdrom = "NoCdrom:  \t"+ str(dic["NoCdrom"])
        if dic["Restricted"]:
            offset = 1
            Restricted = "Restricted: \t" + str(dic["Restricted"])
        if dic["Forbidden"]:
            offset = 1
            Forbidden = "Forbidden: \t" + str(dic["Forbidden"])
        if dic["Broken"]:
            offset = 1
            Broken = "Broken: \t" + str(dic["Broken"])
        if dic["Deprecated"]:
            offset = 1
            Deprecated = "Deprecated: \t" + str(dic["Deprecated"])
        if dic["Ignore"]:
            offset = 1
            Ignore = "Ignore: \t" + str(dic["Ignore"])

        if offset == 1:
            ##print "==> Errors: "
            if not NoPackage:
                pass
            else:
                print NoPackage
                pass
            if NoCdrom:
                print NoCdrom
                pass
            if Restricted:
                print Restricted
                pass
            if Forbidden:
                print Forbidden
                pass
            if Broken:
                print Broken
                pass
            if Deprecated:
                print Deprecated
                pass
            if Ignore:
                print Ignore
                pass



    def AllPorts(self, port):

        """ Port """


        PortNoPackage, PortNoCdrom, PortRestricted \
                = PortDepends.CheckRestrictions(port)

        PortForbidden, PortBroken, PortDeprecated, PortIgnore \
                = PortDepends.CheckProblems(port)

        PortFetch, PortExtract \
                = PortDepends.CheckExtraDepends(port)

        Errors = {"NoPackage":"", "NoCdrom":"", "Restricted":"", "Forbidden":"", \
                  "Broken":"", "Deprecated":"", "Ignore":"", "Fetch":"", "Extract":""}

        if len(PortNoPackage) == 0:
            PortNoPackage = 0
        else:
            Errors["NoPackage"] = PortNoPackage[0]
            PortNoPackage = 1

        if len(PortNoCdrom) == 0:
            PortNoCdrom = 0
        else:
            Errors["NoCdrom"] = PortNoCdrom[0]
            PortNoCdrom = 1

        if len(PortRestricted) == 0:
            PortRestricted = 0
        else:
            Errors["Restricted"] = PortRestricted[0]
            PortRestricted = 1

        if len(PortForbidden) == 0:
            PortForbidden = 0
        else:
            Errors["Forbidden"] = PortForbidden[0]
            PortForbidden = 1

        if len(PortBroken) == 0:
            PortBroken = 0
        else:
            Errors["Broken"] = PortBroken[0]
            PortBroken = 1

        if len(PortDeprecated) == 0:
            PortDeprecated = 0
        else:
            Errors["Deprecated"] = PortDeprecated[0]
            PortDeprecated = 1

        if len(PortIgnore) == 0:
             PortIgnore = 0
        else:
            Errors["Ignore"] = PortIgnore[0]
            PortIgnore = 1

        if len(PortFetch) == 0:
            PortFetch = 0
        else:
            Errors["Fetch"] = PortFetch[0]
            PortFetch = 1

        if len(PortExtract) == 0:
            PortExtract = 0
        else:
            Errors["Extract"] = PortExtract[0]
            PortExtract =1

        CheckPorts.AllErrors(Errors)
        """ Without PortFetch and PortExtract """
        return PortNoPackage, PortNoCdrom, PortRestricted, \
               PortForbidden, PortBroken, PortDeprecated, \
               PortIgnore


if __name__ == '__main__':

    sys_len = len(sys.argv)
    MainPort = None

    if sys_len < 2:
        print 'Using: ./dep.py category/portname'
    else:
        """ Check first the PORT itself """
        port = PORT_PATH + sys.argv[1]
        MainPort = port
        PortDepends = PortDepends()
        CheckPorts = CheckPorts()
        RunDepends, LibDepends, BuildDepends = PortDepends.Depends(port)
        Rundepends = PortDepends.ParserDependsList(str(RunDepends))
        Libdepends = PortDepends.ParserDependsList(str(LibDepends))
        Builddepends = PortDepends.ParserDependsList(str(BuildDepends))
        a = CheckPorts.AllPorts(port)
        PortName = commands.getstatusoutput('cd %s; make -V PORTNAME' \
                                            % (port))
        PortVersion = commands.getstatusoutput('cd %s; make -V PORTVERSION' \
                                              % (port))
        PortReference = str(PortName[1]) + "-" + str(PortVersion[1]) + ".log"
        PortReferenceDir = str(PortName[1]) + "-" + str(PortVersion[1])
        Output = open(PortReference, 'w')

        if 1 in a:
            print "[Error] ==> Port Name: \t%s" % (port)
            Output.write("Error;Port Name;" + port + "\n")
        else:
            print "===> Port Name: \t%s" % (port)
            Output.write("OK;Port Name;" + port + "\n")

        for port in Rundepends:
            a = CheckPorts.AllPorts(port)
            if 1 in a:
                print "[Error] ==> RUN_DEPENDS: \t%s" % (port)
                Output.write("Error;Run Depends;" + port + "\n")
            else:
                print "==> RUN_DEPENDS: \t%s" % (port)
                Output.write("OK;Run Depends;" + port + "\n")

        for port in Libdepends:
            a = CheckPorts.AllPorts(port)
            if 1 in a:
                print "[Error] ==> LIB_DEPENDS: \t%s" % (port)
                Output.write("Error;Lib Depends;" + port + "\n")
            else:
                print "==> LIB_DEPENDS: \t%s" % (port)
                Output.write("OK;Lib Depends;" + port + "\n")

        for port in Builddepends:
            a = CheckPorts.AllPorts(port)
            if 1 in a:
                print "[Error] ==> BUILD_DEPENDS: \t%s" % (port)
                Output.write("Error;Build Depends;" + port + "\n")
            else:
                print "==> BUILD_DEPENDS: \t%s" % (port)
                Output.write("OK;Build Depends;" + port + "\n")

        Output.close()
        ControlError = qatcheckporterror.CheckPortError(PortReference)

        listPorts = []

        if ControlError == 0:
            File = open(PortReference, 'r')
            database = shelve.open('qat', writeback=True)

            try:
                database = MySQLdb.connect('localhost', 'root', '')
                database.select_db('portsandbox')
                cursor = database.cursor()
            except:
                print "Error connecting to the database....\n"

            for line in File:
                line = line.split(';')
                if line[1] == 'Port Name':
                    portname = line[2].split('\n')
                    cursor.execute('INSERT INTO MainPort (PortName) VALUES (%s)', \
                            (portname[0]))
                    database.commit()
                    cursor.execute('SELECT MAX(id) FROM MainPort')
                    last = cursor.fetchone()
                elif line[1] == 'Run Depends':
                    rdepends = line[2].split('\n')
                    cursor.execute('INSERT INTO RunDepends (Id, PortName) VALUES (%s, %s)', \
                            (last[0], rdepends[0]))
                    database.commit()
                elif line[1] == 'Lib Depends':
                    ldepends = line[2].split('\n')
                    cursor.execute('INSERT INTO LibDepends (Id, PortName) VALUES (%s, %s)', \
                            (last[0], ldepends[0]))
                    database.commit()
                elif line[1] == 'Build Depends':
                    bdepends = line[2].split('\n')
                    cursor.execute('INSERT INTO BuildDepends (Id, PortName) VALUES (%s, %s)', \
                            (last[0], bdepends[0]))
                    database.commit()


            # Verify the integrity of MainPort CheckSum
            cursor.execute('SELECT PortName from MainPort where id=%s', (last[0]))
            PortName = cursor.fetchone()
            CheckSumControl, CheckSumReason, Portname \
                    = qatchecksum.CheckSum(PortName[0])
            cursor.execute('UPDATE MainPort SET CheckSumControl=%s \
                               WHERE id=%s', (CheckSumControl, \
                                                         last[0]))
            database.commit()
            logcreator.LogCreator('CheckSum', CheckSumReason, PortReferenceDir, \
                                  PortReference, last[0])

            # Test MainPortExtract
            Table = "MainPort"
            if CheckSumControl == 0:
                ExtractControl = sql.PortExtract(last[0], Table, None, PortReferenceDir,
                                                PortReference)
            else:
                ExtractControl = 256

            if ExtractControl == 0:
                PatchControl = sql.PortPatch(last[0], Table, None, PortReferenceDir, \
                                             PortReference)
            else:
                PatchControl = 256

            # Check LibDepends
            Table = "LibDepends"
            sql.Checking(last[0], Table)

            # Check BuildDepends
            Table = "BuildDepends"
            sql.Checking(last[0], Table)

            # Check RunDepends
            Table = "RunDepends"
            sql.Checking(last[0], Table)

            # Check if every port related with the MainPort is OK
            Table = "MainPort"
            cmd = 'SELECT BuildControl from LibDepends WHERE id=%s' % (last[0])
            cursor.execute(cmd)
            result_Lib = cursor.fetchall()
            cmd = 'SELECT BuildControl from BuildDepends WHERE id=%s' % (last[0])
            cursor.execute(cmd)
            result_Build = cursor.fetchall()
            cmd = 'SELECT BuildControl from RunDepends WHERE id=%s' % (last[0])
            cursor.execute(cmd)
            result_Run = cursor.fetchall()

            LibControler = 0
            BuildControler = 0
            RunControler = 0

            for interator in result_Lib:
                if interator[0] != 0:
                    LibControler = 1

            for interator in result_Build:
                if interator[0] != 0:
                    BuildControler = 1

            for interator in result_Run:
                if interator[0] != 0:
                    RunControler = 1

            # Test MainPort
            if LibControler == 0 and BuildControler == 0 and RunControler == 0:
                sql.PortBuild(last[0], Table, None, PortReferenceDir, PortReference)
                sql.PortInstall(last[0], Table, PortReferenceDir, PortReference)
                sql.MakePackage(last[0], Table, PortReferenceDir, PortReference)
                sql.PortDeinstall(last[0], Table, PortReferenceDir, PortReference)

                # Show on console where is the log
                cmd = 'SELECT PortLog from MainPort where id=%s' % (last[0])
                cursor.execute(cmd)
                PortLogFile = cursor.fetchone()
                print "===> Log at: %s" % (PortLogFile)
            else:
                print "Something is BROKEN....."

        elif ControlError == 1:
            print "PORT NOK"

