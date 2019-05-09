# Python code to search audio files in current
# folder (We can change file type/name and path
# according to the requirements.

import os
import matplotlib.pyplot as plt
import yaml

#This is to save other path
# path="/home/aiza/myPython/mybackup/"
path = "/mnt/android/"

# This is to get the directory that the program
# is currently running in.

#passing path
# dir_path = os.path.dirname(os.path.realpath(path))
dir_path = path

#count for total files

def readExtensionsFile(file_type):
	path = os.getcwd()          		# Get current working directory
	path = path + '/extensions.yaml'  	# Get path of help file
	extensions = []
    # Open and print help file
	with open(path,'r') as stream:
		try:
			extensions = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)

	return extensions[file_type]

def getFiles(dir_path, graph_path, file_type):
	'''Function to get audio files'''

	fileList = []		
	extensions = readExtensionsFile(file_type)		# Read extensions from file
	countsDict = {}							# Dictionary that hold count of each type of file
	# Initialize dictionary with 'ext:0'
	for ext in extensions:
		countsDict.update({ext:0})
	
	for root, dirs, files in os.walk(dir_path):
		
		for file in files:
			# Iterate through each extension
			for ext in extensions:
				# Check if file ends with the supplied extension
				if file.endswith(ext):
					dic = { root : str(file)} 				# Dictionary
					countsDict[ext] = countsDict[ext] + 1	# Increment count of file type

					for key in dic.keys():
						path = key
						filename = dic[key]
						row = path + "/" + filename + "\n"
						fileList.append(row)

	# Calculate total amount of files
	total = 0
	for key, value in countsDict.items():
		total += value

	# Calculate percentage of each file
	labels = []
	sizes = []
	for ext, freq in countsDict.items():
		perc = calculatePercentage(freq, total)
		sizes.append(perc)
		label = ext + " " + str(perc) + ' %'
		labels.append(label)

	# sizes = [str(cmp3), str(cwma), str(cxmf), str(cogg),str(cm4a),str(cwav)]
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue','blue', 'pink']
	explode = []
	# Set explode values
	for x in labels:
		explode.append(0.3)

	explodeTuple = tuple(explode)

	# explode = (0.1, 0, 0, 0,0,0)  # explode 1st slice
 
	# Plot
	patches, _ = plt.pie(sizes)
 
	plt.axis('equal')
	# plt.show()
	plt.legend(patches, labels, loc='upper right')		# Legend
	plt.savefig(graph_path)								# Save figure
	return fileList

def calculatePercentage(number, total):
	'''Calculate percentage'''
	perc = (number/total) * 100
	perc = round(perc,2)
	return perc
