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

def searchMeSHNo(meshno):
    return {u'articles': HTTPGetCategory(meshno)}

meshno = sys.argv[1]

with io.open('cat/mesh-' + meshno + '.search.json', 'w', encoding='utf-8') as outfile:
    artnosJson = json.dumps(searchMeSHNo(meshno), ensure_ascii=False)
    outfile.write(artnosJson)
