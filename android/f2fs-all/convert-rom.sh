#!/bin/bash



ext4=(
	"format(\"ext4\", \"EMMC\", \"/dev/block/platform/msm_sdcc.1/by-name/system\", \"0\", \"/system\");"
	"mount(\"ext4\", \"EMMC\", \"/dev/block/platform/msm_sdcc.1/by-name/system\", \"/system\");"
	)
f2fs=(
	"run_program(\"/sbin/mkfs.f2fs\", \"/dev/block/platform/msm_sdcc.1/by-name/system\");"
	"run_program(\"/sbin/busybox\", \"mount\", \"/system\");"
	)

echo "doing checks..."
[[ ! -f "tools/signapk.jar" ]] && echo "signapk not found" && exit 1
[[ ! -f "tools/7za" ]] && echo "7za not found" && exit 1
[[ ! -f "tools/md5sum" ]] && echo "md5sum not found" && exit 1
[[ ! -f "$1" ]] && echo "no such file $1" && exit 1

P7ZIP="./tools/7za"
SIGNAPK="java -jar ./tools/signapk.jar ./tools/testkey.x509.pem ./tools/testkey.pk8"
MD5SUM="./tools/md5sum"

WORKINGDIR="$(mktemp -d)"
FILEIN="$1"
FILENAME="$(basename $FILEIN)"
EXTENSION="${FILENAME##*.}"
FILENAME="${FILENAME%.*}"
BASEDIR="$(dirname $FILEIN)"
FILESIGNED="$FILENAME-f2fsall-signed.$EXTENSION"

echo "unzipping..."
sh -c "$P7ZIP x -y -o$WORKINGDIR $FILEIN > /dev/null"

echo "changing commands..."
TMPFILE="$(mktemp)"
cp "$WORKINGDIR/META-INF/com/google/android/updater-script" "$TMPFILE"
sed -i -e "s#${ext4[0]}#${f2fs[0]}#" "$TMPFILE"
sed -i -e "s#${ext4[1]}#${f2fs[1]}#" "$TMPFILE"
cp "$TMPFILE" "$WORKINGDIR/META-INF/com/google/android/updater-script"
rm "$TMPFILE"

echo "zipping & signing..."
TMPFILE="$(mktemp)"
sh -c "$P7ZIP a -r $TMPFILE.zip $WORKINGDIR/* > /dev/null"
sh -c "$SIGNAPK $TMPFILE.zip $BASEDIR/$FILESIGNED"
rm "$TMPFILE.zip"

echo "final touches..."
sh -c "$MD5SUM $BASEDIR/$FILESIGNED > $BASEDIR/$FILESIGNED.md5sum"

echo "cleaning up..."
rm -rf "$WORKINGDIR"
rm -rf "$TMPFILE"

echo "files are in: $BASEDIR"
