#!/usr/bin/env python
#### ###################
##
##	F T
##	ft2011@gmail.com
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

DEBUG = False

cmdPrefix = "bbi"
cmds = ["help", "set", "show", "clear"]

def showHelp():
	hexchat.prnt("---------------")
	hexchat.prnt("/{} {}".format(cmdPrefix, cmds[0]))
	hexchat.prnt("\t\t\t - show this")

	hexchat.prnt("/{} {} <server> <channel> <password>".format(cmdPrefix, cmds[0]))
	hexchat.prnt("\t\t\t - set values!")
	hexchat.prnt("\t\t\t - server and channel are regex!")
	hexchat.prnt("\t\t\t - example: /{} {} (.*)\.efnet\.[net|com] #chan[one|two] mypassword123".format(cmdPrefix, cmds[1]))

	hexchat.prnt("/{} {}".format(cmdPrefix, cmds[2]))
	hexchat.prnt("\t\t\t - show values!")
	hexchat.prnt("---------------")

def setVals(data):
	hexchat.set_pluginpref("server", data[0])
	hexchat.set_pluginpref("channel", data[1])
	hexchat.set_pluginpref("password", data[2])
	hexchat.prnt("new values saved!")

def showVals():
	prefServ = hexchat.get_pluginpref("server")
	prefChan = hexchat.get_pluginpref("channel")
	prefPass = hexchat.get_pluginpref("password")
	hexchat.prnt("server: '{}' - channel: '{}' - password: '{}'".format(prefServ, prefChan, prefPass))

def clearVaĺs():
	hexchat.set_delpref("server")
	hexchat.set_delpref("channel")
	hexchat.set_delpref("password")
	hexchat.prnt("values deleted!")

def onJoin_cb(word, word_eol, userdata):
	# get info of current context
	curServ = hexchat.get_info("server")
	curChan = str(word[2])[1:]

	# get saved data
	prefServ = hexchat.get_pluginpref("server")
	prefChan = hexchat.get_pluginpref("channel")
	prefPass = hexchat.get_pluginpref("password")

	if DEBUG:
		msg = "saved values: '{}' '{}' '{}' context: '{}' '{}'"
		hexchat.prnt(msg.format(prefServ, prefChan, prefPass, curServ, curChan))

	if re.match(prefServ, curServ) == None:
		if DEBUG:
			msg = "server: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(curServ, prefServ))
		return hexchat.EAT_NONE

	if re.match(prefChan, curChan) == None:
		if DEBUG:
			msg = "channel: '{}' doesn't match '{}'"
			hexchat.prnt(msg.format(curChan, prefChan))
		return hexchat.EAT_NONE

	hexchat.command("msg {} identify {}".format(curChan, prefPass))

def onCommand_cb(word, word_eol, userdata):
	if word[1] == cmds[0]: # show help
		showHelp()		
		return hexchat.EAT_ALL
	
	elif word[1] == cmds[1]: # set values
		setVals([word[2], word[3], word[4]])
		return hexchat.EAT_ALL

	elif word[1] == cmds[2]:  # show values
		showVals()
		return hexchat.EAT_ALL

	elif word[1] == cmds[3]:  # clear values
		clearVaĺs()
		return hexchat.EAT_ALL

	hexchat.prnt("unknown command: '/{}'".format(word_eol[0]))
	hexchat.prnt("check out: /{} {}".format(cmdPrefix, cmds[0]))
	return hexchat.EAT_ALL

def unload_cb(userdata):
	hexchat.prnt("BitlBee-identify unloaded!")

### setting up hook
hexchat.hook_command(cmdPrefix, onCommand_cb)
hexchat.hook_server("JOIN", onJoin_cb)
hexchat.hook_unload(unload_cb)
if DEBUG:
	print("BitlBee-identify loaded!")