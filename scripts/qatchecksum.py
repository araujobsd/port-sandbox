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
import sys
sys.path.append('jail')
import jail

#jailpath = '/usr/Jail/Qat/'

def PortVersion(path, JailId):

    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    portname = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s ; make -V PORTNAME"' \
                                % (jailpath, path))
    portversion = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s ; make -V PORTVERSION"' \
                                % (jailpath, path))
    port = str(portname[1]) + "-" + str(portversion[1])

    return port


def CheckSum(path, JailId):


     Jail = jail.JailEngine()
     jailpath = Jail.JailPath(JailId)

     checksum = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make checksum -DBATCH"' \
                            % (jailpath, path))

     if checksum[0] == 0:
         print "===> Checksum OK: %s" % (path)
     elif checksum[0] == 256:
         print "===> Checksum Error: %s" % (path)

     return checksum[0], checksum[1], path

def MakeExtract(path, JailId):

    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    extract = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make extract -DBATCH"' \
                                      % (jailpath, path))

    if extract[0] == 0:
        print "===> Extract OK: %s" % (path)
    else:
        print extract

    return extract[0], extract[1]

def MakePatch(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    patch = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make patch -DBATCH"' \
                                    % (jailpath, path))

    if patch[0] == 0:
        print "===> Applying patch OK: %s" % (path)
    else:
        print patch

    return patch[0], patch[1]

def MakeBuild(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    build = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make build -DBATCH"' \
                                    % (jailpath, path))

    if build[0] == 0:
        print "===> Build OK: %s" % (path)
    else:
        print build

    return build[0], build[1]

def InstallPort(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    install = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make install -DBATCH"' \
                                      % (jailpath, path))

    if install[0] == 0:
        print "===> Install OK: %s" % (path)
    else:
        print install

    return install[0], install[1]

def MakePackage(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    package = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make package -DBATCH"' \
                                      % (jailpath, path))

    if package[0] == 0:
        print "===> Package OK: %s" % (path)
    else:
        print package

    return package[0], package[1]


def DeinstallPort(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    deinstall = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make deinstall"' \
                                        % (jailpath, path))

    if deinstall[0] == 0:
        print "===> Deinstall OK: %s" % (path)
    else:
        print deinstall

    return deinstall[0], deinstall[1]


def MtreeCheck(Phase, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    mtree = 'mtree -c -i -n -k uname,gname,mode,nochange -p /usr/local/'

    if Phase == 'Before':
        mtreebefore = commands.getstatusoutput('chroot %s /bin/csh -c "%s >/tmp/before"' \
                                               % (jailpath, mtree))
    elif Phase == 'After':
        mtreeafter = commands.getstatusoutput('chroot %s /bin/csh -c "%s >/tmp/after"' \
                                              % (jailpath, mtree))
    elif Phase == 'Diff':
        mtree = 'mtree -f /tmp/after -f /tmp/before'
        diff = commands.getstatusoutput('chroot %s /bin/csh -c "%s"' % (jailpath, mtree))
        return diff
    elif Phase == 'Clean':
        rm = commands.getstatusoutput('chroot %s /bin/csh -c "rm -f /tmp/before /tmp/after"' \
                % (jailpath))



def PortsClean(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    portsclean = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make clean"'\
            % (jailpath, path))

