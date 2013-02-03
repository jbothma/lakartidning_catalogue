#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def HTTPGetIssueArtnos(issuenum):
    conn = httplib.HTTPConnection("ltarkiv.lakartidningen.se")
    path = "/nummer" + issuenum
    conn.request("GET", path)
    response = conn.getresponse()
    print response.status, response.reason
    page = response.read()
    conn.close()
    return page

def HTMLGetArtNums(page):
    regex = "<A HREF=/artNo(\d+)>(.+?)</A>"
    return [{u'artno': unicode(m.group(1)),
             u'ref':  unicode(m.group(2))}
            for m in re.finditer(regex , page)]

issuenum = sys.argv[1]

pageHTML = HTTPGetIssueArtnos(issuenum)
artNums = HTMLGetArtNums(pageHTML)

with io.open('issues/issue-' + issuenum + '-artnos.json', 'w', encoding='utf-8') as outfile:
    artNumsJson = json.dumps(artNums, ensure_ascii=False)
    outfile.write(artNumsJson)
