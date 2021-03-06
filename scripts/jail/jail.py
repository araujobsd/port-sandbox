#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import sys
import os
import commands
import MySQLdb
import configparser

conf = configparser.MySQL()
host, user, password, db = conf.config()

database = MySQLdb.connect(host, user, password)
database.select_db(db)
cursor = database.cursor()

class Jail:

    def CreateJailEnvironment(self, Name, Releng):

        JailDir = '/usr/Jail/' + Name

        if not os.path.exists(JailDir):
            try:
                os.makedirs(JailDir)
            except:
                print "===> Can't create the %s." % (JailDir)
            self.CreateCvsFile(Name, JailDir, Releng)
        else:
            print "===> There is a Jail at: %s" % (JailDir)


    def CreateCvsFile(self, Name, JailDir, Releng):

        host = "*default host=cvsup3.us.FreeBSD.org\n"
        base = "*default base=%s\n" % (JailDir)
        prefix = "*default prefix=%s\n" % (JailDir)
        release = "*default release=cvs tag=%s\n" % (Releng)
        other = "*default delete use-rel-suffix\n*default compress\nsrc-all"

        ConfFile = JailDir + '/csup.conf'
        try:
            CvsupFile = open(ConfFile, 'w')
            CvsupFile.write(host)
            CvsupFile.write(base)
            CvsupFile.write(prefix)
            CvsupFile.write(release)
            CvsupFile.write(other)
            CvsupFile.close()
            self.CreateJail(Name, Releng, JailDir, ConfFile)
        except:
            print "===> Can't open the csup.conf file at: %s" % (ConfFile)



    def CreateJail(self, Name, Releng, JailDir, ConfFile):

        csup = '/usr/bin/csup'

        if not os.path.exists(csup):
            print '===> You supposed to have csup installed.'
        else:
            Prefix = JailDir + '/build'

            if not os.path.exists(Prefix):
                os.makedirs(Prefix)

            print "===================< DEBUG >==============="
            print "Jaildir: %s" % (Jaildir)
            print "Prefix: %s" % (Prefix)
            print "===================< DEBUG >==============="

            os.system('%s -L2 -g %s' % (csup, ConfFile))
            os.system('cd %s/src/; make buildworld DESTDIR=%s' % (JailDir, Prefix))
            os.system('cd %s/src/; make installworld DESTDIR=%s' % (JailDir, Prefix))
            os.system('cd %s/src/; make distribution DESTDIR=%s' % (JailDir, Prefix))
            os.system('cd %s; tar -jcpvf build.bz2 %s' % (JailDir, Prefix))
            self.JailDatabase(Name, JailDir, Prefix, Releng)


    def JailDatabase(self, Name, JailDir, BuildDir, Releng):

        if Name != None and JailDir != None and BuildDir != None and Releng != None:
            print "OK"
            cmd = "INSERT INTO Jail (JailName, JailDir, BuildDir, Releng) \
                   VALUES ('%s', '%s', '%s', '%s')" % (Name, JailDir, BuildDir, Releng)
            cursor.execute(cmd)
            database.commit()
        else:
            print "===> Something is wrong and not able to insert into Jail table."



    def UpdateJail(self, Id):

        if Id != None:
            cmd = 'SELECT Id, JailDir FROM Jail WHERE Id=%s' % (Id)
            cursor.execute(cmd)
            Result = cursor.fetchone()
            if Result:
                Id = Result[0]
                JailDir = Result[1]
                csup = '/usr/bin/csup'
                Prefix = JailDir + '/build'
                ConfFile = JailDir + '/csup.conf'

                if not os.path.exists(Prefix):
                    os.makedirs(Prefix)

                os.system('%s -L2 -g %s' % (csup, ConfFile))
                os.system('cd %s/src/; make buildworld DESTDIR=%s' % (JailDir, Prefix))
                os.system('cd %s/src/; make installworld DESTDIR=%s' % (JailDir, Prefix))
                os.system('cd %s/src/; make distribution DESTDIR=%s' % (JailDir, Prefix))
                os.system('cd %s; tar -jcpvf build.bz2 %s' % (JailDir, Prefix))
            else:
                print "There isn't a Jail with Id number %s" % (Id)
        else:
            print "You should pass the Id number, consulting with the option list"



    def RmJail(self, Id):

        if Id != None:
            cmd = 'SELECT Id from Jail WHERE Id=%s' % (Id)
            cursor.execute(cmd)
            Result = cursor.fetchone()
            if Result:
                cmd = 'SELECT Id, JailDir from Jail WHERE Id="%s"' % (Result[0])
                cursor.execute(cmd)
                Result = cursor.fetchone()
                Id = Result[0]
                JailDir = Result[1]
                cmd = "DELETE from Jail WHERE Id='%s'" % (Id)
                cursor.execute(cmd)
                database.commit()
                os.system('cd %s/build ; find . | xargs chflags noschg' % (JailDir))
                os.system('rm -rf %s' % (JailDir))
            else:
                print "There isn't a Jail with Id number %s" % (Id)
        else:
            print "You should pass the Id number, consulting with the option list"


    def ListJail(self):

        cmd = 'SELECT Id, JailName, Releng from Jail'
        cursor.execute(cmd)
        Result = cursor.fetchall()
        for i in Result:
            print "--------------------------"
            print "Id: \t%s" % (i[0])
            print "Name: \t%s" % (i[1])
            print "Releng: %s" % (i[2])
            print "--------------------------"


    def UpdatePortsTree(self):


        print "==> Waiting while portstree is updating."
        update_portstree = commands.getstatusoutput("cvsup -L2 -g ports-supfile")

        if update_portstree[0] == 0:
            print "==> PortsTree Updated [OK]"
        else:
            print "==> Error to update PortsTree: "
            print update_portstree[1]


class JailEngine:


    def JailPath(self, Id):

        cmd = 'SELECT BuildDir FROM Jail WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchone()

        if Result:
            return Result[0]
        else:
            print "First of all, create a Jail with the jail command."


    def ExtractJail(self, Id):

        cmd = 'SELECT JailDir, BuildDir FROM Jail WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchone()
        JailDir = Result[0]
        BuildDir = Result[1]
        os.system('cd %s ; tar -jxpvf build.bz2' % (JailDir))
        os.system('mount -t devfs devfs %s/dev' % (BuildDir))
        os.system('devfs -m %s/dev rule apply path null unhide' % (BuildDir))
        os.system('mkdir %s/usr/ports' % (BuildDir))
        #os.system('mount_nullfs /usr/Jail/lib/ports %s/usr/ports' % (BuildDir))
        os.system('mount_nullfs /usr/ports %s/usr/ports' % (BuildDir))
        os.system('mount_nullfs /usr/Jail/lib/var %s/var' % (BuildDir))
        os.system('mkdir %s/usr/src' % (BuildDir))
        os.system('mount_nullfs /usr/src %s/usr/src' % (BuildDir))
        os.system('cp /etc/resolv.conf %s/etc' % (BuildDir))
        os.system('mtree -deU -f %s/etc/mtree/BSD.root.dist -p %s/' % (BuildDir, BuildDir))
        os.system('mtree -deU -f %s/etc/mtree/BSD.var.dist -p %s/var' % (BuildDir, BuildDir))
        os.system('mtree -deU -f %s/etc/mtree/BSD.usr.dist -p %s/usr' % (BuildDir, BuildDir))
        os.system('mtree -deU -f %s/usr/ports/Templates/BSD.local.dist -p %s/usr/local' % (BuildDir, BuildDir))



    def CleanJail(self, Id):

        cmd = 'SELECT BuildDir FROM Jail WHERE Id=%s' % (Id)
        cursor.execute(cmd)
        Result = cursor.fetchone()
        BuildDir = Result[0]
        os.system('umount %s/usr/ports' % (BuildDir))
        os.system('umount %s/var' % (BuildDir))
        os.system('umount %s/usr/src' % (BuildDir))
        os.system('umount %s/dev' % (BuildDir))
        os.system('cd %s ; find . | xargs chflags noschg' % (BuildDir))
        os.system('rm -rf %s' % (BuildDir))
        print BuildDir



if __name__ == '__main__':

    jail = Jail()
    sys_len = len(sys.argv)

    if sys_len == 4:
        if sys.argv[1] == 'create':
            jail.CreateJailEnvironment(sys.argv[2], sys.argv[3])
        else:
            print "Usage: ./jail.py create NAME RELENG_X"
    elif sys_len == 3:
        if sys.argv[1] == 'update':
            jail.UpdateJail(sys.argv[2])
        elif sys.argv[1] == 'remove':
            jail.RmJail(sys.argv[2])
    elif sys_len == 2:
        if sys.argv[1] == 'list':
            jail.ListJail()
        elif sys.argv[1] == 'updatePorts':
            jail.UpdatePortsTree()
        elif sys.argv[1] == 'help':
            print "Example: ./jail.py create NAME RELENG_X"
            print "Example: ./jail.py update ID"
            print "Example: ./jail.py remove ID"
            print "Example: ./jail.py updatePorts"
            print "Example: ./jail.py list"
    else:
        print "Usage: ./jail.py help"

