#!/bin/sh

input=$1
draw=("drawable-hdpi" "drawable-ldpi" "drawable-mdpi" "drawable-xhdpi")
res=("72x72" "36x36" "48x48" "96x96")

for (( i = 0 ; i < ${#draw[@]} ; i++ )); do
	sh -c "convert $input -resize ${res[$i]} ${draw[$i]}/$(basename $input)"
done
