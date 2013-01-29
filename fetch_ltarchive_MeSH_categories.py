#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import httplib
import re
import htmlentitydefs
import sys
import codecs
import json
import io,json

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def pathList():
    alpha = [chr(number) for number in xrange(65, 91)] + [ "AA", "AE", "OE", "XX"]
    return ["/keyw" + letter + ".htm" for letter in alpha]

def HTTPGetMeSHList(path):
    conn = httplib.HTTPConnection("ltarkiv.lakartidningen.se")
    conn.request("GET", path)
    response = conn.getresponse()
    print response.status, response.reason
    page = response.read()
    meshNos = HTMLGetMeSHList(page)
    conn.close()
    return meshNos

def HTMLGetMeSHList(page):
    regex = "<a href=\"/trafflista\?meshNo=(\d+)\">(.+?)</a>"
    return [{unicode('meshno'): unicode(m.group(1)),
             unicode('name_sv'): unicode(unescape(m.group(2)))}
            for m in re.finditer(regex , page)]


##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.
# http://effbot.org/zone/re-sub.htm#unescape-html
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def allMeSHNos():
    return [MeSHNo for path in pathList() for MeSHNo in HTTPGetMeSHList(path)]

for path in pathList():
    for MeSHNoData in HTTPGetMeSHList(path):
        with io.open('cat/mesh-' + MeSHNoData[u'meshno' + '.json'], 'w', encoding='utf-8') as outfile:
            MeSHNoJSON = json.dumps(MeSHNoData, ensure_ascii=False)
            outfile.write(MeSHNoJSON)
