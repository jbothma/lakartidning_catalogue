#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re
import os

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

meshno = str(int(sys.argv[1]))

with io.open('meshno2artno.json', 'r', encoding='utf-8') as file:
    meshno2artno = json.load(file)
    for artno in meshno2artno[meshno]:
        print artno
