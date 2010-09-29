#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#

import commands
import MySQLdb
import qatchecksum
import logcreator


database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
cursor = database.cursor()

def GetCommitter(Last):

    cmd = 'SELECT PortName FROM MainPort WHERE id=%s' % (Last)
    cursor.execute(cmd)
    PortName = cursor.fetchone()
    Committer_Line = None
    File = PortName[0] + '/' + 'Makefile'
    Makefile = open(File, 'r')

    for line in Makefile:
        if '$FreeBSD' in line:
            Committer_Line = line

    Committer_Line = Committer_Line.split(' ')
    cmd = 'UPDATE MainPort SET Committer="%s" WHERE id="%s"' \
           % (Committer_Line[6], Last)
    cursor.execute(cmd)
    database.commit()
    Makefile.close()

    return Committer_Line[6]


def LogDepends(Last, PortName, Table):

    cmd = 'SELECT PortName from %s WHERE id=%s and PortName="%s"' \
           % (Table, Last, PortName)
    cursor.execute(cmd)
    PortName= cursor.fetchone()
    Name = commands.getstatusoutput('cd %s; make -V PORTNAME' % (PortName[0]))
    Version = commands.getstatusoutput('cd %s; make -V PORTVERSION' \
              % (PortName[0]))
    Log = str(Name[1]) + '-' + str(Version[1]) + '.log'
    cmd = 'SELECT PortLog from MainPort WHERE id=%s' % (Last)
    cursor.execute(cmd)
    LogDir = cursor.fetchone()
    Result = LogDir[0].split('/')
    Dir = Result[0] + '/' + Result[1] + '/'

    return Dir, Log


def Checking(Last, Table, StartBuild):

    cmd = 'SELECT PortName from %s where id=%s' % (Table, Last)
    cursor.execute(cmd)
    PortName = cursor.fetchall()
    for Port in PortName:
        if StartBuild == 0:
            CheckSumControl = PortSum(Last, Table, Port[0])
            if CheckSumControl == 0:
                ExtractControl = PortExtract(Last, Table, Port[0], None, None)
            else:
                print "Error CheckSum..."
                ExtractControl = 256
            if ExtractControl == 0:
                PatchControl = PortPatch(Last, Table, Port[0], None, None)
            else:
                print "Error Extract..."
                PatchControl = 256
        # ALERT: Here maybe there is a bug.
        # Should I check the PatchControl(SQL) before? Yes, I think so!
        if StartBuild == 1:
            BuildControl = PortBuild(Last, Table, Port[0], None, None)


def PortSum(IdMainPort, Table, Port):

    CheckSumControl, CheckSumReason, PortName = qatchecksum.CheckSum(Port)
    cmd = 'UPDATE %s SET CheckSumControl=%s WHERE id=%s and PortName="%s"' \
            % (Table, CheckSumControl, IdMainPort, Port)
    cursor.execute(cmd)
    database.commit()
    Dir, Log = LogDepends(IdMainPort, Port, Table)
    logcreator.LogCreator('CheckSum', CheckSumReason, Dir, Log, None)

    if CheckSumControl == 0:
        return 0
    else:
        return 1



def PortExtract(IdMainPort, Table, PortName, PortReferenceDir, PortReference):

    if PortName == None:
        cmd = 'SELECT PortName, CheckSumControl from %s where id=%s' \
                 % (Table, IdMainPort)
        cursor.execute(cmd)
        result = cursor.fetchone()
        PortName = result[0]
        CheckSumControl = result[1]
    else:
        cmd = 'SELECT CheckSumControl from %s where id=%s and PortName="%s"' \
                 % (Table, IdMainPort, PortName)
        cursor.execute(cmd)
        result = cursor.fetchone()
        CheckSumControl = result[0]


    if CheckSumControl == 0:
        ExtractControl, ExtractReason = qatchecksum.MakeExtract(PortName)
        cmd = 'UPDATE %s SET ExtractControl=%s WHERE id=%s and PortName="%s"' \
                % (Table, ExtractControl, IdMainPort, PortName)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Extract', ExtractReason, PortReferenceDir,\
                                  PortReference, IdMainPort)
        else:
            Dir, Log = LogDepends(IdMainPort, PortName, Table)
            logcreator.LogCreator('Extract', ExtractReason, Dir, Log, None)
        return 0
    else:
        return 1


def PortPatch(IdMainPort, Table, PortName, PortReferenceDir, PortReference):

    if PortName == None:
        cmd = 'SELECT PortName, ExtractControl from %s WHERE id=%s' \
                 % (Table, IdMainPort)
        cursor.execute(cmd)
        result = cursor.fetchone()
        PortName = result[0]
        ExtractControl = result[1]
    else:
        cmd = 'SELECT ExtractControl from %s where id=%s AND PortName="%s"' \
                % (Table, IdMainPort, PortName)
        cursor.execute(cmd)
        result = cursor.fetchone()
        ExtractControl = result[0]

    if ExtractControl == 0:
        PatchControl, PatchReason = qatchecksum.MakePatch(PortName)
        cmd = 'UPDATE %s SET PatchControl=%s WHERE id=%s AND PortName="%s"' \
                % (Table, PatchControl, IdMainPort, PortName)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Patch', PatchReason, PortReferenceDir,\
                                   PortReference, IdMainPort)
        else:
            Dir, Log = LogDepends(IdMainPort, PortName, Table)
            logcreator.LogCreator('Patch', PatchReason, Dir, Log, None)
        return 0
    else:
        return 1


def PortBuild(IdMainPort, Table, PortName, PortReferenceDir, PortReference):

    if PortName == None:
        cmd = 'SELECT PortName, PatchControl from %s WHERE id=%s' \
                 % (Table, IdMainPort)
        cursor.execute(cmd)
        result = cursor.fetchone()
        PortName = result[0]
        PatchControl = result[1]
    else:
        cmd = 'SELECT PatchControl from %s where id=%s AND PortName="%s"' \
                % (Table, IdMainPort, PortName)
        cursor.execute(cmd)
        result = cursor.fetchone()
        PatchControl = result[0]

    if PatchControl == 0:
        BuildControl, BuildReason = qatchecksum.MakeBuild(PortName)
        cmd = 'UPDATE %s SET BuildControl=%s WHERE id=%s AND PortName="%s"' \
                % (Table, BuildControl, IdMainPort, PortName)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Build', BuildReason, PortReferenceDir,\
                                   PortReference, IdMainPort)
        else:
            Dir, Log = LogDepends(IdMainPort, PortName, Table)
            logcreator.LogCreator('Build', BuildReason, Dir, Log, None)
        return 0
    else:
        return 1


def PortInstall(IdMainPort, Table, PortReferenceDir, PortReference):

    cmd = 'SELECT PortName, BuildControl from %s WHERE id=%s' \
            % (Table, IdMainPort)
    cursor.execute(cmd)
    result = cursor.fetchone()
    PortName = result[0]
    BuildControl = result[1]
    if BuildControl == 0:
        InstallControl, InstallReason = qatchecksum.InstallPort(PortName)
        cmd = 'UPDATE %s SET InstallControl=%s WHERE id=%s' \
                % (Table, InstallControl, IdMainPort)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Install', InstallReason, PortReferenceDir,\
                                   PortReference, IdMainPort)
        return 0
    else:
        return 1

def MakePackage(IdMainPort, Table, PortReferenceDir, PortReference):

    cmd = 'SELECT PortName, InstallControl from %s WHERE id=%s' \
            % (Table, IdMainPort)
    cursor.execute(cmd)
    result = cursor.fetchone()
    PortName = result[0]
    InstallControl = result[1]
    if InstallControl == 0:
        PackageControl, PackageReason = qatchecksum.MakePackage(PortName)
        cmd = 'UPDATE %s SET PackageControl=%s WHERE id=%s' \
                % (Table, PackageControl, IdMainPort)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Package', PackageReason, PortReferenceDir,\
                                   PortReference, IdMainPort)
        return 0
    else:
        return 1


def PortDeinstall(IdMainPort, Table, PortReferenceDir, PortReference):

    cmd = 'SELECT PortName, InstallControl from %s WHERE id=%s' \
            % (Table, IdMainPort)
    cursor.execute(cmd)
    result = cursor.fetchone()
    PortName = result[0]
    InstallControl = result[1]
    if InstallControl == 0:
        DeinstallControl, DeinstallReason = qatchecksum.DeinstallPort(PortName)
        cmd = 'UPDATE %s SET DeinstallControl=%s WHERE id=%s' \
                % (Table, DeinstallControl, IdMainPort)
        cursor.execute(cmd)
        database.commit()
        if PortReference != None:
            logcreator.LogCreator('Deinstall', DeinstallReason, \
                                    PortReferenceDir, PortReference, IdMainPort)
        return 0
    else:
        return 1
