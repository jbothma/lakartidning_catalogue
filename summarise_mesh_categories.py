#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def HTTPGetCategory(meshno):
    conn = httplib.HTTPConnection("ltarkiv.lakartidningen.se")
    path = "/trafflista?meshNo=" + meshno
    conn.request("GET", path)
    response = conn.getresponse()
    print response.status, response.reason
    page = response.read()
    meshNos = HTMLGetCategory(page)
    conn.close()
    return meshNos

def HTMLGetCategory(page):
    regex = "<A HREF=/artNo(\d+)>(.+?)</A>(.+?)<BR>"
    return [{unicode('artno'): unicode(m.group(1)),
             unicode('ref'): unicode(m.group(2))}
            for m in re.finditer(regex , page)]

with io.open('ltarkiv.lakartidning.se-MeSH.json', 'r', encoding='utf-8') as infile:
    categories = json.load(infile)

def artnosPerCategory():
    return [{u'meshno': cat[u'meshno'],
             u'name_sv': cat[u'name_sv'],
             u'articles': HTTPGetCategory(cat[u'meshno'])}
            for cat in categories]

artnosJson = json.dumps(artnosPerCategory(), ensure_ascii=False)

with io.open('artnos_per_category.json', 'w', encoding='utf-8') as outfile:
    outfile.write(artnosJson)
