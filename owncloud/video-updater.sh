#!/bin/bash
######## ########################
##
##	F T <ft2011@gmail.com>
##	
##### #####################
######## ########################
##
##	vars
##	
##### #####################
OC_DIR="/var/www/owncloud"
TMP_DIR="/tmp"

######## ########################
##
##	fetch latest source-files
##	from git
##	
##### #####################
if [ -d $TMP_DIR/mediaelement/.git ]; then
	git --git-dir=$TMP_DIR/mediaelement/.git fetch
	git --git-dir=$TMP_DIR/mediaelement/.git --work-tree=$TMP_DIR/mediaelement merge origin/master
else
	git clone https://github.com/johndyer/mediaelement.git $TMP_DIR/mediaelement
fi

######## ########################
##
##	copy stuff
##	
##### #####################
# css
#cp $TMP_DIR/mediaelement/build/mediaelementplayer.css $OC_DIR/apps/files_videoviewer/css
# images / svgs
cp $TMP_DIR/mediaelement/build/background.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/bigplay.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/bigplay.svg $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/controls.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/controls.svg $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/controls-ted.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/controls-wmp.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/controls-wmp-bg.png $OC_DIR/apps/files_videoviewer/img/skin
cp $TMP_DIR/mediaelement/build/loading.gif $OC_DIR/apps/files_videoviewer/img/skin
# swf / js
cp $TMP_DIR/mediaelement/build/flashmediaelement.swf $OC_DIR/apps/files_videoviewer/js
cp $TMP_DIR/mediaelement/build/mediaelement-and-player.js $OC_DIR/apps/files_videoviewer/js
cp $TMP_DIR/mediaelement/build/mediaelement-and-player.min.js $OC_DIR/apps/files_videoviewer/js
cp $TMP_DIR/mediaelement/build/silverlightmediaelement.xap $OC_DIR/apps/files_videoviewer/js
# src-dir
cp -r $TMP_DIR/mediaelement/src $OC_DIR/apps/files_videoviewer/mediaelement/src

echo "all done!"
