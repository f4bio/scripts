#!/bin/bash

BOOTHDD="sda1"
ROOTHDD="sda2"

mount --bind /dev /mnt/"$ROOTHDD"/dev
mount --bind /proc /mnt/"$ROOTHDD"/proc
mount --bind /sys /mnt/"$ROOTHDD"/sys

mount /dev/sda1 /mnt/"$ROOTHDD"/boot
