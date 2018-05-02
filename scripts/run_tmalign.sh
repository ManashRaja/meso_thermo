#!/bin/bash

#$1 tmalign binary path
#$2 pdb dir
#$3 dest dir
#$4 out dir
counter=0
for filesrc in $2*
do
	for filedb in $3*
	do
		f=$(basename $filedb)
		g=$(basename $filesrc)
		dest_name="$4$g-$f"
		if [ ! -f $dest_name ]; then
		    echo "File not found!"
		    OUTPUT="$($1 $filesrc $filedb &)"
	    	echo "$OUTPUT" > "$dest_name"
	    	echo $dest_name
		fi
	    let counter++
	    echo $counter
	done
done
