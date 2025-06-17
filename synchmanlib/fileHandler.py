import os
import itertools
from zipfile import ZipFile

config = {
	'autoRepair' : None,
	'log' : None,
	'updateBackup' : None,
	'backupFrequency' : None,
	'backupMax' : None
}

#add docstrings to all

def readConfig(configFile):
	try:
		with open(configFile, 'r') as file:
			content = file.readlines()
			for line in content:
				if ':' in line:
					splitLine = line.strip().replace(' ', '').split(':') # Cleans the split strings.
					if splitLine[0] in config.keys():
						config[splitLine[0]] = splitLine[1] # Updates dictionary value

	except FileNotFoundError as fe: # make these more specific
		print(f'filenotfound')
	except PermissionError as pe:
		print(f'premissionerror')
	except Exception as e:
		print(f'exception')

def buildStructure(dir=os.getcwd()): # add error handling
	output = {}
	for (root, dirs, files) in os.walk(dir, topdown=True):
		fileStruct = dirs.copy()
		fileStruct.extend(files)
		output[f'{root}'] = fileStruct
	return output

def checkDir(dir, knownStructure):
	missing = []
	extra = []
	errors = []
	for (root, dirs, files) in os.walk(dir, topdown=True):
		if root in knownStructure:
			knownDirComp = knownStructure.get(root, None)
			totalContents = files.copy()
			totalContents.extend(dirs)
			# print(root)
			# print(f'kdc: {knownDirComp}')
			# print(f'TC: {totalContents}')
			if len(totalContents) == len(knownDirComp):
				pass #idk do something for logging ig
			elif len(totalContents) < len(knownDirComp): # v make sure that extra files not in knownDir isn't being filled in as missing
				for i, (actual, expected) in enumerate(itertools.zip_longest(totalContents, knownDirComp, fillvalue='Missing')):
					if actual == 'Missing':
						missing.append(expected)
		elif not root in knownStructure:
			print(f'Not root, root: {root}')
			extra.append(root)
	if len(missing) == 0:
		return (True, extra, errors)
	elif len(missing) > 0: # Make results more consistent
		#do extra log stuff
		return(False, missing, extra, errors)

def makeBackup(dir, name): # Add error handling
	filePaths = []
	# Get paths
	for root, dirs, files in os.walk(dir, topdown=True):
		for fileName in files:
			path = os.path.join(root, fileName)
			filePaths.append(path)
		for directory in dirs:
			path = os.path.join(root, directory)
			filePaths.append(path)
	
	print(f'paths: {filePaths}')
	with ZipFile(f'{name}.zip', 'w') as zip:
		for file in filePaths:
			zip.write(file)