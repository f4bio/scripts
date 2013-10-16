#!/bin/sh

##############
#	
# 	source: 	http://goo.gl/friK5H
#	thx: 		mathfeel
#	fixes: 		(python2:6093): Gtk-WARNING **: 
#				Theme directory preferences/48 of theme Numix has no size field
#########

echo "" >> /usr/share/icons/Numix/index.theme
echo "[preferences/48]" >> /usr/share/icons/Numix/index.theme
echo "Size=48" >> /usr/share/icons/Numix/index.theme
echo "Context=Stock" >> /usr/share/icons/Numix/index.theme
echo "Type=Scalable" >> /usr/share/icons/Numix/index.theme
