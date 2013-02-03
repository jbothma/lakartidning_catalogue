MESHNOS = $(shell find cat -type f -name 'mesh-*.catno.json')
SEARCH = $(patsubst %.catno.json, %.search.json, $(MESHNOS))

ISSUES = $(shell find issues -type f -regex "issues/issue-[0-9][0-9][0-9][0-9][0-9][0-9].json")
ISSUEARTNOS = $(patsubst issues/issue-%.json, issues/issue-%-artnos.json, $(ISSUES))

ARTNOS = $(wildcard artnos/artno-*.json)
ARTDATA = $(patsubst artnos/artno-%.json, artdata/art-%-data.json, $(ARTNOS))

MESHNO_ARTNOS = $(shell ./list_artnos_per_meshno.py $(MESHNO))
PDFS = $(patsubst %, corpus/pda%.pdf, $(MESHNO_ARTNOS))

corpus: $(PDFS)

# use PDF from local cache
corpus/pda%.pdf: /Users/jdb/thesis/data/medical_sv/all_pdfs/pda%.pdf
	cp /Users/jdb/thesis/data/medical_sv/all_pdfs/pda$*.pdf corpus

# fill local cache
/Users/jdb/thesis/data/medical_sv/all_pdfs/pda%.pdf:
	echo "need to download PDF for " $*

art-data: $(ARTDATA)

artdata/art-%-data.json:
	./get_article_data.py $*

issue-artnos: $(ISSUEARTNOS)

issues/issue-%-artnos.json:
	./list_issue_artnos.py $*

search: $(SEARCH)

%.search.json: %.catno.json
	./search_MeSH_category.py $(patsubst cat/mesh-%, %, $*)
