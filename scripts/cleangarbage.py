#!/usr/local/bin/python
#
# -*- coding: utf-8 -*-
#
import os

def CleanPreLog():

    for fname in os.listdir(os.getcwd()):
        if '.log' in fname:
            os.remove(fname)
