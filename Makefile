MESHNOS = $(shell find cat -type f -name 'mesh-*.catno.json')
SEARCH = $(patsubst %.catno.json, %.search.json, $(MESHNOS))

ISSUES = $(shell find issues -type f -regex "issues/issue-[0-9][0-9][0-9][0-9][0-9][0-9].json")
ISSUEARTNOS = $(patsubst issues/issue-%.json, issues/issue-%-artnos.json, $(ISSUES))

ARTNOS = $(wildcard artnos/artno-*.json)
ARTDATA = $(patsubst artnos/artno-%.json, artdata/art-%-data.json, $(ARTNOS))

art-data: $(ARTDATA)

artdata/art-%-data.json:
	./get_article_data.py $*

issue-artnos: $(ISSUEARTNOS)

issues/issue-%-artnos.json:
	./list_issue_artnos.py $*

search: $(SEARCH)

%.search.json: %.catno.json
	./search_MeSH_category.py $(patsubst cat/mesh-%, %, $*)
