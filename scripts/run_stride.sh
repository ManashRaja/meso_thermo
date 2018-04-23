#!/bin/bash

#$1 stride binary path
#$2 pdb dir
#$3 dest dir
#./run_stride.sh ./thirdparty/stride/stride ../data/meso_pdb/ ../data/meso_stride/

for file in $2*
do
	f=$(basename $file)
	dest_name="$3$f"
    $1 -f$dest_name $file &
done