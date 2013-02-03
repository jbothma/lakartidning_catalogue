#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def HTTPGetIssueArtnos(issuenum):
    conn = httplib.HTTPConnection("ltarkiv.lakartidningen.se")
    path = "/artNo" + issuenum
    conn.request("GET", path)
    response = conn.getresponse()
    print response.status, response.reason
    page = response.read()
    conn.close()
    return unicode(page.decode('iso-8859-1'))

def HTMLGetArtData(page):
    #            <a href="/trafflista?meshNo=4675">Privat sektor</a>
    MeSHRegex = '<a href="/trafflista\?meshNo=(\d+)">(.+?)</a>'
    MeSHData = [{u'meshno': unicode(m.group(1)),
                 u'mesh_sv':  unicode(m.group(2))}
                for m in re.finditer(MeSHRegex , page)]
    # <A target="_blank" HREF=/2000/temp/pda20569.pdf>Artikeln i pdf-format</A>
    PDFRegex = '<A target="_blank" HREF=(.+?)>Artikeln i pdf-format</A>'
    PDFSearch = re.search(PDFRegex, page)
    PDFLink = None
    if PDFSearch != None:
        PDFLink = unicode(PDFSearch.group(1))
    return { u'mesh' : MeSHData,
             u'pdf_path': PDFLink }

artno = str(int(sys.argv[1]))

pageHTML = HTTPGetIssueArtnos(artno)
artData = HTMLGetArtData(pageHTML)

with io.open('artdata/art-' + artno + '-data.json', 'w', encoding='utf-8') as outfile:
    artDataJson = json.dumps(artData, ensure_ascii=False)
    outfile.write(artDataJson)
