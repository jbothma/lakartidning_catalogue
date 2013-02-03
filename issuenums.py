#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import json, io, sys, codecs, httplib, re

sys.stdout = codecs.getwriter('utf8')(sys.stdout);

def HTTPGetIssueNums():
    conn = httplib.HTTPConnection("ltarkiv.lakartidningen.se")
    path = "/nr.htm"
    conn.request("GET", path)
    response = conn.getresponse()
    print response.status, response.reason
    page = response.read()
    conn.close()
    return page

def HTMLGetIssueNums(page):
    regex = "<a href=\"nummer(\d+)\">(\d+)</a>"
    return [{u'nummer': unicode(m.group(1))}
            for m in re.finditer(regex , page)]
pageHTML = HTTPGetIssueNums()
issueNums = HTMLGetIssueNums(pageHTML)

for issue in issueNums:
    with io.open('issues/issue-' + issue[u'nummer'] + '.json', 'w', encoding='utf-8') as outfile:
        issueJson = json.dumps(issue, ensure_ascii=False)
        outfile.write(issueJson)
