#!/usr/bin/env python3

#Title: Clone.py
#Author: Trace Gardner
#Description: This script asks the user for the name of the file that they would like to clone. This value can be the whole file path or just a section of the file path. The script takes that input and locates the file(s) that have the inputed value in the file path. The user then selects the file from a list of files that matched the value inputed and that files becomes the file that is cloned. The program then asks for a location that the user would like to save the file to. The program validates that the desired replication location exists and if the whole, or a part, of the path does not exist, it is created.
#NOTE: This script only works on a Linux-based system

import os
import shutil
import subprocess

#This is a function that takes one arguement: section. "section" is a list of parts that comprise the path to a file or directory in the file system. The values in the list are what you would find between the "/" in the file path. This function is used to check that the path to the cloned file, which was given by the user. It checks if the file exists and creates the whole path or parts of the path when necessary.
def check_clone_location (section):
	a_string = ''
	for x in range(1,len(section)):
		a_string= a_string + '/' + section[x]
		if os.path.exists(a_string) == True:
			if os.path.isdir(a_string) == True:
				print("The directory exists.")
			else:
				if os.path.isfile(a_string) == True:
					print("The file exists.")
		else:
			print("The path does not exist...creating the path now.")
			if len(a_string.split('.')) > 1:
				f = open(a_string, 'x')
				print("The file ", a_string, " has been created.")
			else:
				os.mkdir(a_string)

#This is a function that takes one arguement: section. "section" is a list of parts that comprise the path to a file or directory in the file system. The values in the list are what you would find between the "/" in the file path. This function is used to check that the path to the original file, which was given by the user. It checks if the file exists and creates the whole path or parts of the path when necessary.	
def check_orig_location(section):
	a_string = ''
	ERROR = 2
	for x in range(1,len(section)):
		a_string= a_string + '/' + section[x]
		if os.path.exists(a_string) == True:
			if os.path.isdir(a_string) == True:
				print("The directory exists.")
				ERROR = 0
			else:
				if os.path.isfile(a_string) == True:
					print("The file exists.")
					ERROR = 0
				else:
					ERROR = 1
		else:
			ERROR = 2
	return ERROR
	
#This function replicates the Bash command "locate". Then this function is called, it takes the filename arguement and searched the file system for all instances where the filename is apart of either the path or the filename itself.
def find_files(filename):
	command = ['locate', filename]
	
	output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
	output = output.decode()
	
	search_results = output.split('\n')
	
	return search_results

#This function asks the user for the name of the file that they wish to clone. After the prompt, the function calls the function find_files(filename). See function documentation to see what find_files(filename) does when called. After the function call to find_files, the function determines the stopping values for the for loop interations. The function then lists the files that were returned from find_files(filename). The user filters through each "page" until they find the file they were looking for and returns that value.
def select_file():
	start = 0
	yes = ['y', "yes", "Yes", "YEs", "YES"] #Strings that are acceptable responses to if the file was in the list.
	desired_file = input("Please enter the file you wish to clone. **For best resutls, please enter as much of the path as possible** ")

	search = find_files(desired_file)

#This nested if statment is used to determine how many times the for loops below executes. The max_value is used in the outer for loop to determine how many cycles it goes through and the end variable is for the inner for loop which displays the list of files. This value sets how many files are shown "per" page.
	if(len(search) > 50):
		if((len(search) % 50) == 0.0):
			max_value = len(search)/50
			end = 50
		else:
			max_value = int(len(search)/50)
			end = 50
			remainder = len(search) % 50
	else:
		max_value = 1
		end = len(search)-1

	for x in range(0, max_value):
		for y in range(start, end):
			print(y, search[y])
		response = input("Is the file you want to clone in this list? ")
		if response in yes:
			break
		else:
			if x == max_value - 1:
				print("Check your file name and try again")
				exit(1)
			start = end
			if(x == max_value - 2):
				end = end + 50 + remainder
			else:
				end = end + 50

	choice = eval(input("Please enter the coorisponding number of the file you wish to clone: "))
	file_found = (search[choice])
	return file_found
			
#Script begin
original_file_path = select_file()

original_path_segments = original_file_path.split('/')
ERROR_Value = check_orig_location(original_path_segments)

if ERROR_Value > 0:
	print("Error with the given path!")
	exit(1)

cloned_file_path = input("Where would you like to save the cloned file? Be sure to include the path. ")

cloned_path_segments = cloned_file_path.split('/')
check_clone_location(cloned_path_segments)

shutil.copy(original_file_path, cloned_file_path)

print("Clone completed")
