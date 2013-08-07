IDS=`join -t"-" <(grep -- "-$1\$" tables/artNo-meshNo |sort) <(sort tables/artNo-07engineId)|cut -d"-" -f3`

for ID in $IDS
do
    mkdir -p $2
    cp 07engine_text/$ID $2/$ID.raw
done