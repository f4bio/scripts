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

__module_name__ = "bitlbee-identify"
__module_version__ = "0.1"
__module_description__ = "Send identify command to BitlBee channel"
__author__ = "F T (ft2011)"

CMD_PREFIX = "bbi"
CONST_CMDS = ["help", "set", "show", "clear"]
CONST_PREFS = ["server", "chan", "pass", "nick",  "debug"]
DEF_PREFS = ["irc.c.y", "#some", "pass123", "yaname",  False]

def showHelp():
	hexchat.prnt("---------------")
	hexchat.prnt("/{} {}".format(CMD_PREFIX, CONST_CMDS[0]))
	hexchat.prnt("\t\t\t - show this")

	hexchat.prnt("/{} {} <server> <channel> <password> [<nick>] [<debug>]".format(CMD_PREFIX, CONST_CMDS[0]))
	hexchat.prnt("\t\t\t - set values!")
	hexchat.prnt("\t\t\t - server and channel are regex!")
	hexchat.prnt("\t\t\t - example: /{} {} (.*)\.efnet\.[net|com] #chan[one|two] mypassword123".format(CMD_PREFIX, CONST_CMDS[1]))

	hexchat.prnt("/{} {}".format(CMD_PREFIX, CONST_CMDS[2]))
	hexchat.prnt("\t\t\t - show values!")
	hexchat.prnt("---------------")

def clearVals():
	for k in range(len(CONST_PREFS)):
		hexchat.set_pluginpref(CONST_PREFS[k], "")

def saveVals(vals, nick):
	hexchat.prnt("------> new values: '{}'".format(str(vals)))
	for k in range(len(vals)):
		hexchat.set_pluginpref(CONST_PREFS[k], vals[k])

	hexchat.set_pluginpref("nick", nick)

def showVals():
	hexchat.prnt("------------")
	for k in range(len(CONST_PREFS)):
		hexchat.prnt(hexchat.get_pluginpref(CONST_PREFS[k]))

def gV(key):
	return hexchat.get_pluginpref(key)

def onJoin_cb(word, word_eol, userdata):
	# get info of current context
	server = hexchat.get_info("server")
	chan = str(word[2])[1:]
	nick = hexchat.get_info("nick")

	if re.match(gV("nick"), str(nick)) == None:
		if gV("debug"):
			msg = "nick: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(nick, gV("nick")))
		return hexchat.EAT_NONE

	if re.match(prefs["server"], str(server)) == None:
		if gV("debug"):
			msg = "server: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(server, gV("server")))
		return hexchat.EAT_NONE

	if re.match(prefs["chan"], str(chan)) == None:
		if gV("debug"):
			msg = "channel: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(chan, gV("chan")))
		return hexchat.EAT_NONE

	hexchat.command("msg {} identify {}".format(chan, gV("pass")))

def onCommand_cb(word, word_eol, userdata):
	if word[1] == CONST_CMDS[0]: # show help
		showHelp()
		return hexchat.EAT_ALL
	
	elif word[1] == CONST_CMDS[1]: # save values
		nick = hexchat.get_info("nick")
		saveVals(word[2:], nick)
		return hexchat.EAT_ALL

	elif word[1] == CONST_CMDS[2]:  # show values
		showVals()
		return hexchat.EAT_ALL

	elif word[1] == CONST_CMDS[3]:  # clear values
		clearVals()
		return hexchat.EAT_ALL

	hexchat.prnt("unknown command: '/{}'".format(word_eol[0]))
	hexchat.prnt("check out: /{} {}".format(CMD_PREFIX, CONST_CMDS[0]))
	return hexchat.EAT_ALL

def unload_cb(userdata):
	hexchat.prnt("BitlBee-identify unloaded!")

### setting up hook
hexchat.hook_command(CMD_PREFIX, onCommand_cb)
hexchat.hook_server("JOIN", onJoin_cb)
hexchat.hook_unload(unload_cb)

hexchat.prnt("BitlBee-identify loaded!")