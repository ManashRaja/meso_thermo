#!/bin/bash

#$1 stride binary path
#$2 pdb dir
#$3 dest dir

for file in $3*
do
	f=$(basename $file)
	dest_name="$4$f"
    OUTPUT="$($1 $2 $file &)"
    echo "$OUTPUT" > "$dest_name"
done