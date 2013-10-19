#!/bin/sh

# libs
yain lib32-mpg123 mpg123 
yain lib32-alsa-plugins alsa-plugins
yain lib32-alsa-oss alsa-oss
yain lib32-alsa-lib alsa-lib
# fonts
yain ttf-ms-fonts ttf-tahoma
ln -s /usr/share/fonts/TTF/ /usr/share/wine/fonts/
