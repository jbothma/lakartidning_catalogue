ISSUEPAGES = $(patsubst %, html/nummer%, $(shell cat tables/issuenum))
ARTNOPAGES = $(patsubst %, html/artNo%, $(shell cat tables/issueno-artno|cut -d"-" -f2))

all: $(ARTNOPAGES)


html/artNo%: tables/issueno-artno
	mkdir -p html
	wget -O html/artNo$* http://ltarkiv.lakartidningen.se/artNo$*

tables/issueno-artno: $(ISSUEPAGES)
	perl -nle 'while (/artNo(\d+)/g) {$$artno=$$1; $$issueno=$$ARGV; $$issueno =~ s/html\/nummer(\d+)/$$1/; print $$issueno,"-",$$artno}' html/nummer*>tables/issueno-artno

html/nummer%:
	mkdir -p html
	wget -O html/nummer$* http://ltarkiv.lakartidningen.se/nummer$*

tables/issuenum: html/nr.htm
	mkdir -p tables
	perl -nle 'while (/nummer(\d+)/g) {print $$1}' html/nr.htm > tables/issuenum

html/nr.htm:
	mkdir -p html
	wget -O html/nr.htm "http://ltarkiv.lakartidningen.se/nr.htm"
