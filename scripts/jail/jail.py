#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# araujo@FreeBSD.org
#

import sys
import os
import MySQLdb

database = MySQLdb.connect('localhost', 'root', '')
database.select_db('portsandbox')
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

            os.system('%s -L2 -g %s' % (csup, ConfFile))
            os.system('cd %s/src/; make buildworld DESTDIR=%s' % (JailDir, Prefix))
            os.system('cd %s/src/; make installworld DESTDIR=%s' % (JailDir, Prefix))
            os.system('cd %s; tar -jcpvf build.bz2 %s' % (JailDir, Prefix))
            self.JailDatabase(Name, JailDir, Prefix, Releng)

            """
            os.system('mount_nullfs /usr/ports %s/usr/ports/' % (Prefix))
            os.system('mount -t devfs devfs %s/dev' %(Prefix))
            os.system('devfs -m %s/dev rule apply path null unhide' % (Prefix))
            os.system('mount -t procfs proc %s/proc' %(Prefix))
            """

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
                os.system('%s -L2 -g %s' % (csup, ConfFile))
                os.system('cd %s/src/; make buildworld DESTDIR=%s' % (JailDir, Prefix))
                os.system('cd %s/src/; make installworld DESTDIR=%s' % (JailDir, Prefix))
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
        elif sys.argv[1] == 'help':
            print "Example: ./jail.py create NAME RELENG_X"
            print "Example: ./jail.py update ID"
            print "Example: ./jail.py remove ID"
            print "Example: ./jail.py list"
    else:
        print "Usage: ./jail.py help"

