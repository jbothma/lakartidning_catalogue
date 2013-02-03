#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

issuenum = sys.argv[1]

with io.open('issues/issue-'+ issuenum + '-artnos.json', 'r', encoding='utf-8') as infile:
    artNums = json.load(infile)
    for artNum in artNums:
        with io.open('artnos/artno-'+ artNum[u'artno'] + '.json', 'w', encoding='utf-8') as outfile:
            artnoJson = json.dumps(artNum, ensure_ascii=False)
            outfile.write(artnoJson)
