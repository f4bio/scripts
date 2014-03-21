#!/usr/bin/env python
#### ###################
##
##	Ff Tt (ft2011)
##	plugin to autoidentify on bitlbee
##	v0.1 - 2013-10-19
##	----------------
##	usage: /bbi help
##
### #########
import hexchat
import time

__module_name__ = "MG"
__module_version__ = "0.1"
__module_description__ = "MG"
__author__ = "Ff Tt (ft2011)"

def onCommand_cb(word, word_eol, userdata):
	hexchat.prnt(".")
	time.sleep(0.100)
	hexchat.prnt(",")
	time.sleep(0.200)
	hexchat.prnt("-")
	return hexchat.EAT_ALL

def unload_cb(userdata):
	hexchat.prnt("MG unloaded!")

### setting up hook
hexchat.hook_command("mg", onCommand_cb)
hexchat.hook_unload(unload_cb)

hexchat.prnt("MG loaded!")