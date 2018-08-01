#!/usr/bin/env python

# SWFFile takes in a directory or a single file and checks whether it is compressed or 
# not compressed, then extracts the embedded links from the swf file(s) and outputs 
# them to all_swf_files.txt

import subprocess
from subprocess import call, check_output, Popen
from glob import glob

dump_file = "dump_swf.txt"
all_file_dump = "all_swf_files.txt"
filename = " "
check_loop = 0
finished_reading_file = False
read_count = 0
count = 0

# trid checks whether a single file is uncompressed or needs to be decompressed 
def trid(file):
	global check_loop
	global filename

	filename = file
	# run TrID on file and get results
	result_string = check_output(["trid", "-v", filename])
	print(("{}\n\n" ).format(result_string))

	# parse result_string - is it compressed?
	for word in result_string.split():
		#print(word)
		if word == "Compressed":
			print("----------------- File is Compressed -----------------\n")
			check_loop = 1
	# checks file to right position based on if it is compressed or not		
	if check_loop == 1: 
		flasm()
	else:
		print("----------------- File is NOT compressed ---------------\n")
		swfDump()

# if file is compressed flasm is called to decompress the file
def flasm():
	global filename
	print("Decompressing...\n")
	# decompress it
	call(["flasm", "-x", filename])

	# chasnge the filetype
	change_file = list(filename)
	print(change_file)
	change_file[-3] = 's'
	filename = "".join(change_file)

	swfDump()

# saves links found to a text file
def swfDump():
	print("Dumping...\n")

	# decompile it
	dump = Popen("swfdump -a {} | grep 'http'".format(filename), shell=True, stdout=subprocess.PIPE)
	stdout = dump.stdout.read()

	# save the decompiled result
	with open(dump_file, "a") as outf:
		outf.write("File:  " + filename +"\n\n" )
		print("Found in swf file:\n")
		for letter in stdout.split(','):
			if "http" in letter:
				print(("{} \n").format(letter))
				outf.write(("{}\n\n").format(letter))
	if finished_reading_file :
		print("Finished!\n\ndump_swf.txt is in terminal directory\n")

def loopFiles():
	global finished_reading_file
	global read_count

	# make in to array
	# read file for passing in value
	with open(all_file_dump, "r") as read_file:
		for line in read_file:
			read_count+=1
			file_line = line.strip("\n")
			print(line.strip("\n"))

			if count == read_count:
				finished_reading_file = True
			trid(file_line)
	
def find(file_dir):
	global count
	print(file_dir)
	with open(all_file_dump, "a") as out_file:
		print("Files Found:\n")

		for line in file_dir:
			count+=1
			out_file.write(("{}\n").format(line))
			print(("{}\n").format(line))
		

def main():
	global finished_reading_file
	# add error detection

	x = int(raw_input("enter 1 for one file or 0 for many: "))
	open(all_file_dump, "w").close()
	if x == 1:
		file = raw_input("file name here: ")
		finished_reading_file = True
		trid(file)
	elif x == 0 :
		all = raw_input("Enter in directory: ")
		file_dir = glob(("{}/*.swf").format(all))
		find(file_dir)
		file_dir = glob(("{}/*.$wf").format(all))
		find(file_dir)
		loopFiles()
	else:
		print("Only 1 or 0 for input!")
		main()

main()