#!/bin/sh

##############
#	
# 	source: 	http://goo.gl/DngKkW
#	thx: 		DiscipleOfDante
#	fixes: 		iCCP: known incorrect sRGB profile"
#########

for i in "$(pacman -Qql playonlinux)*"; do
	convert "$i" -strip "$i"
done
