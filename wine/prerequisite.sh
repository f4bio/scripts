#!/bin/sh

rm -rf "$HOME/.wine/"
WINEPREFIX="$HOME/.wine/" WINEARCH="win32" wine "wineboot"
winetricks msxml3 dotnet20 gdiplus riched20 riched30 vcrun2005sp1
winetricks dotnet40
