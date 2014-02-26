#!/bin/sh
###### ################
##
##	root (currently running) android virtual device (emulator)
##	thx: http://forum.xda-developers.com/showthread.php?t=2295075
##	input armeabi/mips/x86
##
#### ##########

baseDir="$(dirname $(dirname $(realpath $0)))"
cpuType=$1

if [ -z $baseDir ]; then
	echo "error accessing root files in $baseDir/root"
	exit 1
fi
if [ -z $cpuType ]; then
	echo "no cpu type given choose one of 'armeabi', 'mips', 'x86'"
	exit 1
fi

echo "initiate..."
adb connect 127.0.0.1:5554
adb root
adb remount

echo "pushing 'su'..."
adb push "$baseDir"/root/koush/"$cpuType"/su /system/bin/su
adb push "$baseDir"/root/koush/"$cpuType"/su /system/sbin/su
adb push "$baseDir"/root/koush/"$cpuType"/su /system/xbin/su
adb shell chmod 6755 /system/bin/su
adb shell chmod 6755 /system/sbin/su
adb shell chmod 6755 /system/xbin/su

echo "pushing 'reboot'..."
adb push "$baseDir"/root/koush/"$cpuType"/reboot /system/bin/reboot
adb push "$baseDir"/root/koush/"$cpuType"/reboot /system/sbin/reboot
adb push "$baseDir"/root/koush/"$cpuType"/reboot /system/xbin/reboot
adb shell chmod 6755 /system/bin/reboot
adb shell chmod 6755 /system/sbin/reboot
adb shell chmod 6755 /system/xbin/reboot

echo "pushing Superuser.apk..."
adb push "$baseDir"/root/koush/Superuser.apk /system/app/
#adb install "$baseDir"/root/koush/Superuser.apk

#echo "restarting adb..."
#adb kill-server
#adb start-server