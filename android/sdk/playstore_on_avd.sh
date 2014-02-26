#!/bin/sh
###### ################
##
##	install play store on android virtual device (emulator)
##	thx: http://goo.gl/AErPDV
##
#### ##########

basedir="$(dirname $(dirname $(realpath $0)))"

if [ -z $basedir ]; then
	echo "error accessing apks in $basedir/apk"
	exit 1
fi

# Remount in rw mode
echo "initiate..."
adb connect 127.0.0.1:5554
adb root
adb remount

echo "pushing apks..."
adb push "$basedir"/apk/GoogleLoginService.apk /system/app/
adb push "$basedir"/apk/GoogleServicesFramework.apk /system/app/
adb push "$basedir"/apk/Phonesky.apk /system/app/

#adb shell rm /system/app/SdkSetup*
adb shell rm /system/app/SdkSetup.apk