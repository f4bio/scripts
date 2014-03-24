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
import re
import threading

replaceChar = {	ord('ä'): 'ae', ord('ö'): 'oe', ord('ü'): 'ue', 
				ord('á'): 'a',  ord('é'): 'e',  ord('ú'): 'u',
				ord('à'): 'a',  ord('è'): 'e',  ord('ù'): 'u',

				ord('Ä'): 'Ae', ord('Ö'): 'Oe', ord('Ü'): 'Ue',
				ord('À'): 'A',  ord('É'): 'E',  ord('Ú'): 'U',
				ord('À'): 'A',  ord('È'): 'E',  ord('Ù'): 'U',

				ord('['): "(",  ord(']'): ')',	ord(','): "_",
				ord('ß'): "ss", ord(' '): "_",
				ord('&'): "and", ord('!'): "",
				ord('#'): "",  ord('*'): "", ord('\''): "", ord('\"'): ""}

includedRename = "."
includedChecksum = "."

excludedRename = "^\.|^\[.*\]$|^\(.*\)$"
excludedChecksum = "[C|c]overs?|[P|p]roof|Sample|^\.|.*\.nfo$|.*\.jpg$|.*\.txt$|.*\.sfv$"

renameFail = [] 
renameSuccess = [] # good idea? Oo

checksumFail = []
checksumSuccess = [] # good idea? Oo

######## ########################
##
##	util
##	
##### #####################
def usage():
	# userIn = None
	# userOut = None
	# verbose = False
	# doSfv = True
	# toUppercase = False
	# toLowercase = False
	# doOverwrite = True
	# doRename = True
	# recursive = False
	# threadCount = 1
	print("scene_renamer.py [-v] [-r] [-l] [-u] [-w] [-s] [-n] [-t #] [-o <output>] -i </input/directory/>")
	print("-h, --help")
	print("-v, --verbose (default: false)")
	print("-r, --recursive (default: false)")
	print("-l, --to-lowercase\t\trename files to lowercase (default: false)")
	print("-u, --to-uppercase\t\trename files to uppercase (default: false)")
	print("-w, --no-overwrite\t\tdon't overwrite existing .sfv files (default: false)")
	print("-s, --no-sfv\t\t\tdon't generate .sfv files (rename only) (default: false)")
	print("-n, --no-rename\t\t\tdon't rename files (sfv only) (default: false)")
	print("-t, --thread-count\t\tnumber # of threads, careful! (default: 1)")
	print("-o, --output\t\t\tspecify output .sfv filename (default: <input>.sfv)")
	print("-i, --input\t\t\tABSOLUTE path to directory to work in (MANDATORY!)")

class CheckFile(threading.Thread):
	def __init__(self, inFile, outFile, poolSema, verbose):
		threading.Thread.__init__(self)
		self.inFile = inFile
		self.outFile = outFile
		self.verbose = verbose
		self.poolSema = poolSema

	def run(self):
		if not os.path.isfile(self.inFile):
			self.poolSema.release()
			return

		prev = 0
		for line in open(self.inFile, "rb"):
			prev = zlib.crc32(line, prev)

		crc32 = str("{0:08x}").format((prev & 0xFFFFFFFF))

		if self.verbose:
			print("done: {}...".format(crc32))

		with open(self.outFile, "a") as out:
			out.write("{} {}\n".format(str(os.path.basename(self.inFile)), crc32))

		self.poolSema.release()

######## ########################
##
##	rename
##
##	TODO: rename "inDir" itself 
##	
##### #####################
def ren(inDir, verbose, recursive, toLowercase, toUppercase):

	for f in os.listdir(inDir):
		try:
			if verbose:
				print("considering for rename: {}".format(os.path.basename(f)))

			# excluded?
			if re.match(excludedRename, os.path.basename(f)):
				if verbose:
					print("excluded!")
				continue

			# included?
			if not re.match(includedRename, os.path.basename(f)):
				if verbose:
					print("not included!")
				continue

			# recursive?
			if os.path.isdir(os.path.join(inDir, f)) and recursive:
				ren(os.path.join(inDir, f), verbose, recursive, toLowercase, toUppercase)

			# do renaming
			result = str(f)
			result = result.translate(replaceChar)
			result = re.sub(r"\s+", "_", result)
			result = re.sub(r"_+", "_", result)
			result = re.sub(r"^[^a-zA-Z0-9]+|[^a-zA-Z0-9\(\)]+$", "", result)

			if toLowercase:
				result = result.lower()
				pass

			if toUppercase:
				result = result.upper()
				pass

			if str(f) == str(result):
				if verbose:
					print("nothing to rename...")
				continue

			if verbose:
				print("renaming in {}: '{}' to '{}'...".format(inDir, os.path.basename(f), result))

			os.rename(os.path.join(inDir, f), os.path.join(inDir, result))
			renameSuccess.append(result)

		except UnicodeEncodeError as uee:
			# just in case...
			print("(renaming) encode error, skipping. ({})".format(uee))
			renameFail.append("{} - {}".format(os.path.join(inDir, f), uee))
			raise

######## ########################
##
##	checksum
##	
##### #####################
def checksum(inDir, outFile, verbose, recursive, overwrite, poolSema):

	if os.path.isfile(os.path.join(inDir, outFile)) and overwrite:
		os.remove(os.path.join(inDir, outFile))

	if verbose:
		print("generating checksums in sfv-file: '{}'".format(outFile))

	for f in os.listdir(inDir):
		try:
			if verbose:
				print("considering checksum for: '{}'".format(f))

			# excluded?
			if re.match(excludedChecksum, f):
				if verbose:
					print("excluded!")
				continue

			# included?
			if not re.match(includedChecksum, f):
				if verbose:
					print("not included!")
				continue
				
			# recursive?
			if os.path.isdir(os.path.join(inDir, f)) and recursive:
				if verbose:
					print("is folder!")
				sfvFile = os.path.join(inDir, f, "{}.sfv".format(f.lower()))
				checksum(os.path.join(inDir, f), sfvFile, verbose, recursive, overwrite, poolSema)
				continue
			try:
				poolSema.acquire()
				CheckFile(os.path.join(inDir, f), os.path.join(inDir, outFile), poolSema, verbose).start()
				checksumSuccess.append(f)
				pass
			except Exception as e:
				raise
				usage()
				sys.exit(2)

		except UnicodeEncodeError as uee:
			# just in case...
			print("(checksum) encode error, skipping. ({})".format(uee))
			checksumFail.append("{} - {}".format(os.path.join(inDir, f), uee))
			raise

######## ########################
##
##	main (parsing, calling...)
##	
##### #####################
def main(argv=None):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hrvo:i:swnlut:", 
			["help", "recursive", "verbose", "output", "input", "no-sfv", 
			"no-overwrite", "no-rename", "to-lowercase", "to-uppercase", "thread-count"])

	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err)) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	userIn = None
	userOut = None
	verbose = False
	doSfv = True
	toUppercase = False
	toLowercase = False
	doOverwrite = True
	doRename = True
	recursive = False
	threadCount = 1

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

		elif o in ("-l", "--to-lowercase"):
			toLowercase = True

		elif o in ("-u", "--to-uppercase"):
			toUppercase = True

		elif o in ("-w", "--no-overwrite"):
			doOverwrite = False

		elif o in ("-t", "--thread-count"):
			threadCount = int(a)

		else:
			assert False, "unhandled option"

	if verbose:
		print("input: {} / output: {} / verbose: {} / sfv: {} / rename: {} / recursive: {} / threads: {} / overwrite: {}"
			.format(userIn, userOut, verbose, doSfv, doRename, recursive, threadCount, doOverwrite))

	## input (-i/--input) is always needed
	if not userIn or not os.path.isdir(userIn):
		print("no input-directory specified, check --help")
		sys.exit()

	######
	## rename
	####
	if doRename:
		ren(userIn, verbose, recursive, toLowercase, toUppercase)

	######
	## sfv
	####
	if doSfv:
		if not userOut or os.path.isdir(userOut):
			outFile = "{}.sfv".format(os.path.basename(os.path.abspath(userIn)))
		else:
			outFile = str(userOut)

		outFile = outFile.lower()
		poolSema = threading.BoundedSemaphore(value=threadCount)
		checksum(userIn, outFile, verbose, recursive, doOverwrite, poolSema)

	if verbose:
		print("")
		print("ALL DONE!")
		print("")
		print("\t\terrors:")
		print("\t\trename: {}".format(len(renameFail)))
		print("\t\tchecksum: {}".format(len(checksumFail)))
		print("")
		print("\t\tsuccess")
		print("\t\trename: {}".format(len(renameSuccess)))
		print("\t\tchecksum: {}".format(len(checksumSuccess)))
		print("")
		print("\t\tcareful:")
		print("\t\t\t1) files are counted per process (renamed and checksummed = 2 files)")
		print("\t\t\t2) already good names are left out")
		pass

######## ########################
##
##	entry point
##	
##### #####################
if __name__ == "__main__":
	# ./rename_and_checksum.py -r -v -i /var/downloads/site/GAMES-PC/The.Sims.3.Seasons-RELOADED/
	sys.exit(main())
