#! /usr/bin/env python3
# -*- coding: utf-8 -*-
######## ########################
##
##	F T <ft2011@gmail.com>
##	
##### #####################
######## ########################
##
##	main
##	
##### #####################
import sys
import os
import getopt
import re
import zlib

badChars = ["'", "ß", "ä", "ö", "ü", "Ä", "Ö", "Ü", "á", "à", "ú", "ù", "é", "è", "À", "Á", "É", "È", "Ú", "Ù", ",", "[", "]"]
goodChars = ["_", "ss", "ae", "oe", "ue", "Ae", "Oe", "Ue", "a", "a", "u", "u", "e", "e", "A", "A", "E", "E", "U", "U", "_", "_", "_"]

badFiles = ["Thumbs.db"]

######## ########################
##
##	util
##	
##### #####################
def usage():
	print("scene_renamer.py [-v] [--recursive] [--no-sfv] [--no-rename] [-o output.sfv] -i /input/directory/")

######## ########################
##
##	rename
##	
##### #####################
def ren(inDir, inFiles, verbose, recursive):	

	if len(badChars) != len(goodChars):
		print(str("kernel panic! exiting!"))
		sys.exit(-1)

	for f in inFiles:

		if os.path.isdir(f) and recursive:
			checksum(f, os.listdir(f), verbose, recursive)

		if str(f) in badFiles:
			continue

		result = re.sub(r"\s+", "_", f)

		for b,g in zip(badChars, goodChars):
			result = result.replace(b, g)

		result = re.sub(r"_+", "_", result)

		src = os.path.join(inDir, f)
		dest = os.path.join(inDir, result)

		if str(f) == str(result):
			print("nothing to do, skipping...")
			continue

		if verbose:
			print("renaming: '{}' to '{}'...".format(f, result))

		os.rename(src, dest)

######## ########################
##
##	checksum
##	
##### #####################
def checksum(inDir, inFiles, outFile, verbose, recursive):

	if os.path.isfile(os.path.join(inDir, outFile)):
		os.remove(os.path.join(inDir, outFile))

	for f in inFiles:

		if os.path.isdir(f) and recursive:
			checksum(f, os.listdir(f), 
				"{}.sfv".format(os.path.basename(
					os.path.abspath(f))), verbose, recursive)

		if str(f) in badFiles:
			continue

		if verbose:
			print("calucating sum crc32 of {}...".format(f))

		prev = 0
		for line in open(os.path.join(inDir, f), "rb"):
			prev = zlib.crc32(line, prev)

		crc32 = str("{0:08x}").format((prev & 0xFFFFFFFF))

		if verbose:
			print("done: {}...".format(crc32))

		with open(os.path.join(inDir, outFile), "a") as out:
			out.write("{} {}\n".format(str(f), crc32))

######## ########################
##
##	main (parsing, calling...)
##	
##### #####################
def main(argv=None):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hrvo:i:sn", ["help", "recursive", "verbose", "output", "input", "no-sfv", "no-rename"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err)) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	userIn = None
	userOut = None
	verbose = False
	doSfv = True
	doRename = True
	recursive = False

	for o, a in opts:
		if o in ("-v", "--verbose"):
			verbose = True

		elif o in ("-h", "--help"):
			usage()
			sys.exit()

		elif o in ("-i", "--input"):
			userIn = a

		elif o in ("-o", "--output"):
			userOut = a

		elif o in ("-s", "--no-sfv"):
			doSfv = False

		elif o in ("-n", "--no-rename"):
			doRename = False

		elif o in ("-r", "--recursive"):
			recursive = True
		else:
			assert False, "unhandled option"

	## input is always needed
	if not userIn:
		print("no input-dir specified, check --help")
		sys.exit()

	if os.path.isdir(userIn):
		inFiles = os.listdir(userIn)
		inDir = os.path.abspath(userIn)
	else:
		inFiles = [os.path.basename(userIn)]
		inDir = os.path.dirname(userIn)

	######
	## rename
	####
	if doRename:
		ren(inDir, inFiles, verbose, recursive)

	######
	## sfv
	####
	if doSfv:
		inFiles = os.listdir(userIn)
		if not userOut or os.path.isdir(userOut):
			outFile = "{}.sfv".format(os.path.basename(os.path.abspath(userIn)))
		else:
			outFile = str(userOut)

		if verbose:
			print("generating checksums in sfv-file: '{}'".format(outFile))
			pass

		checksum(inDir, inFiles, outFile, verbose, recursive)

######## ########################
##
##	entry point
##	
##### #####################
if __name__ == "__main__":
    # ./scene_renamer.py /media/MyBook/data/TV-XViD/00_P2P/Stargate.Atlantis/S01
    sys.exit(main())
