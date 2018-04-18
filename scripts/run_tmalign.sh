#!/bin/bash

#$1 tmalign binary path
#$2 pdb dir
#$3 dest dir
counter=0
for filesrc in $2*
do
	for filedb in $3*
	do
		f=$(basename $filedb)
		g=$(basename $filesrc)
		dest_name="$4$g-$f"
	    OUTPUT="$($1 $filesrc $filedb &)"
	    echo "$OUTPUT" > "$dest_name"
	    let counter++
	    echo $counter
	done
done
