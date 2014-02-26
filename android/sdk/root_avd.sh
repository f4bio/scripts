#!/bin/sh
###### ################
##
##	root (currently running) android virtual device (emulator)
##	thx: http://forum.xda-developers.com/showthread.php?t=2295075
##
#### ##########

basedir="$( cd $(dirname $0) && pwd )"

if [ -z $basedir ]; then
	echo "error accessing apks in $basedir/apk"
	exit 1
fi

adb root
adb remount
adb push "$basedir"/apk/root_utils/Superuser.apk /system/app/
adb push "$basedir"/apk/root_utils/su /system/bin/su
adb push "$basedir"/apk/root_utils/su /system/sbin/su
adb push "$basedir"/apk/root_utils/su /system/xbin/su
adb shell chmod 6755 /system/bin/su
adb shell chmod 6755 /system/sbin/su
adb shell chmod 6755 /system/xbin/su
adb kill-server
adb start-server