#!/bin/sh

#### ##########################
##	
## 	source: http://goo.gl/DngKkW
##	thx: 	DiscipleOfDante
##	fixes: 	iCCP: known incorrect sRGB profile"
#### ###################

FILES=$(pacman -Qql virtualbox | grep .png)

for file in "$FILES"; do
	convert "$file" -strip "$file"
	convert "$file" -profile sRGB_v4_ICC_preference.icc "$file"
	convert "$file" -profile sRGB_v4_ICC_preference_displayclass.icc "$file"
	convert "$file" -profile RGB.icc "$file"
done
