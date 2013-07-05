ISSUEPAGES = $(patsubst %, html/nummer%, $(shell cat tables/issuenum))

tables/issue-artno: $(ISSUEPAGES)
	perl -nle 'while (/artNo(\d+)/g) {$artno=$1; $issueno=$ARGV; $issueno =~ s/html\/nummer(\d+)/$1/; print $issueno,"-",$artno}' html/nummer*>tables/issueno-artno

html/nummer%: html
	wget -O html/nummer$* http://ltarkiv.lakartidningen.se/nummer$*

tables/issuenum: tables html/nr.htm
	perl -nle 'while (/nummer(\d+)/g) {print $$1}' html/nr.htm > tables/issuenum

tables:
	mkdir -p tables

html/nr.htm: html
	wget -O html/nr.htm "http://ltarkiv.lakartidningen.se/nr.htm"

html:
	mkdir -p html

