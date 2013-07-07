ISSUEPAGES = $(patsubst %, html/nummer%, $(shell cat tables/issuenum))
ARTNOPAGES = $(patsubst %, html/artNo%, $(shell cat tables/issueno-artno|cut -d"-" -f2))

#HJARTKARL07ENG = $(patsubst %, html/07engine%, $(shell 'join -t"-" <(shell grep -- "-953" tables/artNo-meshNo |sort) <(sort tables/artNo-07engineId)|cut -d"-" -f3'))

07ENGIDS = $(shell cat tables/artNo-07engineId|cut -d"-" -f2)
07ENGPAGES = $(patsubst %, html/07engine%, $(07ENGIDS))
07ENGTEXT = $(patsubst %, 07engine_text/%, $(07ENGIDS))

all: $(07ENGTEXT)

07engine_text/%:  $(07ENGPAGES)
	python ./07engine.py $* > 07engine_text/$*

html/07engine%: tables/artNo-meshNo tables/artNo-07engineId
	wget -O html/07engine$* http://www.lakartidningen.se/Functions/OldArticle.aspx?articleId=$*

tables/artNo-meshNo: $(ARTNOPAGES)
	perl -nle 'while (/meshNo=(\d+)/g) {$$meshno=$$1; $$artno=$$ARGV; $$artno =~ s/html\/artNo(\d+)/$$1/; print $$artno,"-",$$meshno}' html/artNo*>tables/artNo-meshNo

tables/artNo-07engineId: $(ARTNOPAGES)
	perl -nle 'while (/<A target=_new HREF=[^\=]+\=(\d+)>Artikeln i webbversion<\/A>/g) {$$webvsnurl=$$1; $$artno=$$ARGV; $$artno =~ s/html\/artNo(\d+)/$$1/; print $$artno,"-",$$webvsnurl}' html/artNo*>tables/artNo-07engineId

html/artNo%: tables/issueno-artno
	wget -O html/artNo$* http://ltarkiv.lakartidningen.se/artNo$*

tables/issueno-artno: $(ISSUEPAGES)
	perl -nle 'while (/artNo(\d+)/g) {$$artno=$$1; $$issueno=$$ARGV; $$issueno =~ s/html\/nummer(\d+)/$$1/; print $$issueno,"-",$$artno}' html/nummer*>tables/issueno-artno

html/nummer%:
	wget -O html/nummer$* http://ltarkiv.lakartidningen.se/nummer$*

tables/issuenum: html/nr.htm
	perl -nle 'while (/nummer(\d+)/g) {print $$1}' html/nr.htm > tables/issuenum

html/nr.htm:
	wget -O html/nr.htm "http://ltarkiv.lakartidningen.se/nr.htm"
