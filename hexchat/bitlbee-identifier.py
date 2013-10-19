#!/usr/bin/env python
#### ###################
##
##	F T (ft2011)
##	plugin to autoidentify on bitlbee
##	v0.1 - 2013-10-19
##	----------------
##	usage: /bbi help
##
### #########
import hexchat
import re

__module_name__ = "BitlBee Identifier"
__module_version__ = "0.1"
__module_description__ = "Send identify command to BitlBee channel"
__author__ = "F T (ft2011)"

CMDS = 	{ 
			"bbi" : ["help", "set", "show", "clear"] 
		}
PREFS = {
			"server" : "(.*)\.efnet\.[net|com]",
			"chan" : "#chan[one|two]",
			"pass" : "pass123",
			"debug" : "False"
		}

HELP =	[
			"...........",
			"...........",
			".../bbi help",
			"...........",
			"...........this",
			"...........",
			"...........",
			".../bbi set <server> <channel> <password>",
			"...........",
			"...........set values!",
			"...........server and channel are regex!",
			"...........example:",
			".........../bbi set (.*)\.efnet\.[net|com] #chan[one|two] pass123",
			"...........",
			"...........",
			".../bbi show",
			"...........",
			"...........displays current values this",
			"...........",
			"...........",
			".../bbi match <regex1> <regex2>",
			"...........",
			"...........test regex test",
			"...........",
			"..........."
		]

trigger = "bbi"

### basic getter / setter
def showHelp():
	for line in HELP:
		hexchat.prnt(line)

def clearVals():
	for k in PREFS.keys():
		hexchat.set_pluginpref(PREFS[k], "")

def saveVals(par):
	hexchat.set_pluginpref("server", par[0])
	hexchat.set_pluginpref("chan", par[1])
	hexchat.set_pluginpref("pass", par[2])
	hexchat.set_pluginpref("debug", par[3])
	hexchat.set_pluginpref("nick", par[4])

def showVals():
	for k in PREFS.keys():
		hexchat.prnt(hexchat.get_pluginpref(k))

def gV(key):
	return hexchat.get_pluginpref(key)

def onJoin_cb(word, word_eol, userdata):
	# get info of current context
	server = hexchat.get_info("server")
	chan = str(word[2])[1:]
	nick = hexchat.get_info("nick")

	if re.match(gV("nick"), str(nick)) == None:
		if gV("debug") == "True":
			msg = "nick: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(nick, gV("nick")))
		return hexchat.EAT_NONE

	if re.match(gV("server"), str(server)) == None:
		if gV("debug") == "True":
			msg = "server: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(server, gV("server")))
		return hexchat.EAT_NONE

	if re.match(gV("chan"), str(chan)) == None:
		if gV("debug") == "True":
			msg = "channel: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(chan, gV("chan")))
		return hexchat.EAT_NONE

	hexchat.command("msg {} identify {}".format(chan, gV("pass")))

def onCommand_cb(word, word_eol, userdata):

	hexchat.prnt(word_eol[0])

	if word[1] == CMDS[trigger][0]: # show help
		showHelp()
		return hexchat.EAT_ALL
	
	elif word[1] == CMDS[trigger][1]: # save values
		se = str(word[2])
		ch = str(word[3])
		pa = str(word[4])
		de = str("False")
		ni = str(hexchat.get_info("nick"))

		saveVals([se, ch, pa, de, ni])
		return hexchat.EAT_ALL

	elif word[1] == CMDS[trigger][2]:  # show values
		showVals()
		return hexchat.EAT_ALL

	elif word[1] == CMDS[trigger][3]:  # clear values
		clearVals()
		return hexchat.EAT_ALL


	hexchat.prnt("unknown command: '/{}'".format(word_eol[0]))
	hexchat.prnt("check out: /{} {}".format(trigger, CMDS[trigger][0]))
	return hexchat.EAT_ALL

def unload_cb(userdata):
	hexchat.prnt("BitlBee-identify unloaded!")

### setting up hook
hexchat.hook_command(trigger, onCommand_cb)
hexchat.hook_server("JOIN", onJoin_cb)
hexchat.hook_unload(unload_cb)

hexchat.prnt("BitlBee-identify loaded!")