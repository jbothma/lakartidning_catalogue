#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re
import os

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

with io.open('meshno2artno.json', 'r', encoding='utf-8') as file:
    meshno2artno = json.load(file)
    for meshno in meshno2artno.keys():
        try:
            with io.open('cat/mesh-'+meshno+'.catno.json', encoding='utf-8') as meshfile:
                meshnodata = json.load(meshfile)
                meshname = meshnodata[u'name_sv']
        except IOError:
            meshname = ''
        print len(meshno2artno[meshno]), meshno, meshname
