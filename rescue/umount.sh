#!/bin/bash

BOOTHDD="sda1"
ROOTHDD="sda2"

umount /mnt/"$ROOTHDD"/dev
umount /mnt/"$ROOTHDD"/proc
umount /mnt/"$ROOTHDD"/sys

umount /mnt/"$ROOTHDD"/boot
