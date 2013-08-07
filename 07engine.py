#!/usr/bin/python
# coding=utf8
# -*- coding: utf-8 -*-

import io, sys
from bs4 import BeautifulSoup

id = sys.argv[1]

with io.open('html/07engine'+ id,
             'r',
             encoding='utf-8') as infile:
    html = infile.read(-1)
    infile.close()
    soup = BeautifulSoup(html)
    divs = soup.find_all("div", attrs={"class": "article-text"})
    for div in divs:
        print div.get_text().encode('utf-8')
