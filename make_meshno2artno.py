#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re
import os

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def filename2artno(filename):
    #art-18013-data.json
    regex = 'art-(\d+)-data.json'
    return re.match(regex, filename).group(1)

MeSHArtnoMap = {}

for filename in os.listdir('artdata'):
    with io.open('artdata/' + filename, 'r', encoding='utf-8') as file:
        artData = json.load(file)
        if artData[u'pdf_path'] != None:
            for meshno in artData[u'mesh']:
                if meshno[u'meshno'] not in MeSHArtnoMap:
                    MeSHArtnoMap[meshno[u'meshno']] = []
                MeSHArtnoMap[meshno[u'meshno']].append(filename2artno(filename))

with io.open('meshno2artno.json', 'w', encoding='utf-8') as outfile:
    meshno2artnoJson = json.dumps(MeSHArtnoMap, ensure_ascii=False)
    outfile.write(unicode(meshno2artnoJson))
