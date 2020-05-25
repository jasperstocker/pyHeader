import os, os.path
from pathlib import Path;
import shutil
import io
import platform
from datetime import datetime
import re


projectDir = Path("test/") # path to all your C# scripts
versionFile = Path("test/") / "myVersionScript.cs" # path to a script with your version constant in - you might not have this though...
headerFile = r"header.txt" # the path to the main header content to paste at the top of your scripts
ignoreFile = r"ignore.txt" # a list of folders and files to ignore in this process. you'll want to add libraries to this
publicKeyFile = r"public.txt" # a key to apply to your headers - ideal to use to search usage of private files hosted on public servers

headerStart = '#region ScriptHeader\n' # the region name to surround the header - this will allow us to delete older versions and replace the content if we rerun
headerEnd = '#endregion\n'
oldHeader = '#region copyright\n' # any old header regions you want to remove...

def recursive_generation(src):
	"""
	Cycle through all the files and generate the header file from the text in txt
	"""	
	
	for item in os.listdir(src):
	
		if item.endswith(".meta"): #ignore unity meta files
			continue
	
		file_path = os.path.join(src, item)

		# if item is a *.cs file, copy it if newer
		if os.path.isfile(file_path) and file_path.endswith(".cs"):
			
			#store this before we mess with the file!
			modifiedTime = os.path.getmtime(file_path)
			
			#read file
			original = open(file_path, mode='r', encoding='utf-8-sig')
			originalContent = original.readlines()
			original.close()
			
			#remove whitespace
			while originalContent[0] == '' or originalContent[0] == '\n':
				del originalContent[0]
			
			#find header
			headerEndIndex = -1
			
			if originalContent[0] == headerStart:
				length = len(originalContent) 
				for i in range(length):
					line = originalContent[i]
					if line == headerEnd:	
						headerEndIndex = i
						break
						
			
			#find old header
			if originalContent[0] == oldHeader:
				length = len(originalContent) 
				for i in range(length):
					line = originalContent[i]
					if line == headerEnd:	
						headerEndIndex = i
						break
			
			#delete header
			if headerEndIndex != -1:
				while headerEndIndex > -1:
					del originalContent[0]
					headerEndIndex += -1
			
			#remove whitespace
			while originalContent[0] == '' or originalContent[0] == '\n':
				del originalContent[0]
			
			ignore = False
			for ignoreItem in ignoreList:
				if ignoreItem in file_path:
					ignore = True
								
			output = originalContent
			header = generate_header(file_path, modifiedTime)
			
			if not ignore:
				#add header
				output = header + originalContent
			
			newContent=open(file_path, mode='w', encoding='utf-8-sig')
			newContent.writelines(output)
			newContent.close()
			
			#reset the modified time
			os.utime(file_path, (modifiedTime, modifiedTime))
			
			operation = "+h " if not ignore else "-- "
			print(operation + file_path)
						
		# else if item is a folder, recurse 
		elif os.path.isdir(file_path):
			recursive_generation(file_path)

def generate_header(path, modifiedTime):
	file = open(headerFile, mode='r', encoding='utf-8-sig') 
	headerContent = file.readlines() 
	file.close()
	headerContent.insert(0, headerStart)
	headerContent.append('\n')
	
	creationTime = creation_date(path)
	
	headerContent.append('// \n')
	headerContent.append('// \n')
	headerContent.append('// Public Key: '+publicKey+'\n')
	headerContent.append('// Last updated on: '+format_timestamp(modifiedTime)+'\n')
	headerContent.append('// BuildR Version: '+get_version()+'\n')
	headerContent.append('// \n')
	
	headerContent.append(headerEnd)
	headerContent.append('\n')
	headerContent.append('\n')
	return headerContent
	
def creation_date(path):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def format_timestamp(time):
	return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
	
def get_version():
	output = '3.0.x'
	
	file = open(versionFile, 'r') 
	versionFileLines = file.read().split('\n')
	file.close();
	
	for item in versionFileLines:
		if "public const string VERSION" in item:
			parts = item.split()
			partLength = len(parts) 
			output = parts[partLength-1]
			break
			
	output = re.sub('[!@#$"f:;]', '', output)
	
	return output


file = open(ignoreFile, 'r') 
ignoreList = file.read().split('\n')
file.close();

version = get_version()

file = open(publicKeyFile, 'r') 
publicKey = file.read().split('\n')[0]
file.close();


recursive_generation(projectDir)

print("Version: "+version)
print("Public Key: "+publicKey)
print("COMPLETE")

