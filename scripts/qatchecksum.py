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

    StdiffConf = open('/tmp/stdiff.conf', 'w')
    StdiffConf.write("""
        db_type = dbm
        db = /tmp/fs.dbm
        # What we won't check - By Araujo
        !%s/root
        !%s/var
        !%s/tmp
        !%s/work
        !%s/compat/linux/proc
        !%s/proc
        !%s/usr/src
        !%s/usr/ports
        !%s/usr/local/lib/X11/xserver/SecurityPolicy
        !%s/usr/local/share/nls/POSIX
        !%s/usr/local/share/nls/en_US.US-ASCII
        !%s/usr/local/info/dir
        !%s/usr/local/lib/X11/fonts
        !%s/boot
        !%s/dev
        !%s/media
        !%s/rescue
        !%s/sys
        !%s/usr/lib/libcrypt.so
        !%s/usr/lib/libkvm.so
        !%s/usr/lib/libmd.so
        !%s/usr/lib/libncurses.so
        !%s/usr/lib/libcurses.so
        !%s/usr/lib/libtermcap.so
        !%s/usr/lib/libtermlib.so
        !%s/usr/lib/libtinfo.so
        !%s/usr/lib/libncursesw.so
        !%s/usr/lib/libcursesw.so
        !%s/usr/lib/libtermcapw.so
        !%s/usr/lib/libtermlibw.so
        !%s/usr/lib/libtinfow.so
        !%s/usr/lib/libsbuf.so
        !%s/usr/lib/libutil.so
        !%s/usr/lib/libalias.so
        !%s/usr/lib/libbegemot.so
        !%s/usr/lib/libbsnmp.so
        !%s/usr/lib/libcam.so
        !%s/usr/lib/libdevstat.so
        !%s/usr/lib/libedit.so
        !%s/usr/lib/libbsdxml.so
        !%s/usr/lib/libgeom.so
        !%s/usr/lib/libipsec.so
        !%s/usr/lib/libkiconv.so
        !%s/usr/lib/libipx.so
        !%s/usr/lib/libpcap.so
        !%s/usr/lib/libufs.so
        !%s/usr/lib/libz.so
        !%s/usr/lib/libavl.so
        !%s/usr/lib/libctf.so
        !%s/usr/lib/libdtrace.so
        !%s/usr/lib/libnvpair.so
        !%s/usr/lib/libumem.so
        !%s/usr/lib/libuutil.so
        !%s/usr/lib/libzfs.so
        !%s/usr/lib/libzpool.so
        !%s/usr/lib/libreadline.so
        !%s/usr/lib/libcrypto.so
        %s spug
    """ % (jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath,
            jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath, jailpath))
    StdiffConf.close()


    if Phase == 'Before':
        mtreebefore = commands.getstatusoutput('stdiff.py -C /tmp/stdiff.conf -u')
    elif Phase == 'Install':
        mtreeafter = commands.getstatusoutput('stdiff.py -C /tmp/stdiff.conf -u -o /tmp/diff')
    elif Phase == 'Deinstall':
        mtreeafter = commands.getstatusoutput('stdiff.py -C /tmp/stdiff.conf -u -o /tmp/diff')
    elif Phase == 'Diff':
        diff = commands.getstatusoutput('stdiff.py -C /tmp/stdiff.conf -c -o /tmp/diff')
        result = commands.getstatusoutput('cat /tmp/diff')
        return result
    elif Phase == 'Clean':
        rm = commands.getstatusoutput('rm -f /tmp/stdiff.conf /tmp/diff')



def PortsClean(path, JailId):


    Jail = jail.JailEngine()
    jailpath = Jail.JailPath(JailId)

    portsclean = commands.getstatusoutput('chroot %s /bin/csh -c "cd %s; make clean"'\
            % (jailpath, path))

