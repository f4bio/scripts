#!/bin/sh
###### ################
##
##	install play store on android virtual device (emulator)
##	thx: http://goo.gl/AErPDV
##	input: avd name
##
#### ##########

avd=$1
basedir="$( cd $(dirname $0) && pwd )"

if [ -z $avd ]; then
	echo "no avd-name passed. usage: $(basename $0) AVD_NAME"
	exit 1
fi

if [ -z $basedir ]; then
	echo "error accessing apks in $basedir/apk"
	exit 1
fi

emulator -avd $avd -partition-size 500 -no-audio -no-boot-anim &

echo "press any key when avd is completely started..."
read

# Remount in rw mode
adb shell mount -o remount,rw -t yaffs2 /dev/block/mtdblock0 /system

# Allow writing to app directory on system partition
adb shell chmod 777 /system/app

# Install following apk
adb push "$basedir"/apk/GoogleLoginService.apk /system/app/.
adb push "$basedir"/apk/GoogleServicesFramework.apk /system/app/.
adb push "$basedir"/apk/Phonesky.apk /system/app/. # Vending.apk in older versions

#adb shell rm /system/app/SdkSetup*
adb shell rm /system/app/SdkSetup.apk