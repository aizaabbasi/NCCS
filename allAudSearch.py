# Python code to search audio files in current
# folder (We can change file type/name and path
# according to the requirements.

import os

#This is to save other path
# path="/home/aiza/myPython/mybackup/"
path = "/mnt/android/"
# This is to get the directory that the program
# is currently running in.

#passing path
# dir_path = os.path.dirname(os.path.realpath(path))
dir_path = path

#count for total files

def getFiles(dir_path):
	'''Function to get miscellaneous files'''
	num=count=0
	cmp3=cwma=cxmf=cogg=cm4a=cwav=0

	fileList = []		# This will hold the list of files
## How to Run
	# file_obj = open("allAud_csv_output.txt", "w")

	# csvobj = open("allAud_csv.csv", "w")

	# columnTitleRow = "Path, File Name\n"
	# csvobj.write(columnTitleRow)

	for root, dirs, files in os.walk(dir_path):
		
		for file in files:
				# change the extension from '.DOC to  
			# the one of your choice.
			if file.endswith('.mp3'):
				
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cmp3=cmp3+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row = path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)

			elif file.endswith('.wma'):
			
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cwma=cwma+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "," + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)
			
			elif file.endswith('.xmf'):
			
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cxmf=cxmf+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)

			elif file.endswith('.ogg'):
			
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cogg=cogg+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)

			elif file.endswith('.m4a'):
			
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cm4a=cm4a+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)
		
			elif file.endswith('.wav'):
			
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cwav=cwav+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)

			else:	count=count+1

	return fileList


	# print ("\nTotal files found here : "+str(cmp3)+ " plus " +str(cwma)+ " plus " +str(cxmf)+ " plus " +str(cogg)+ " plus " +str(cm4a)+ " plus " +str(cwav)+" equals "+str(num), file=file_obj)

	# print ("\nMP3s : "+str(cmp3)+ " WMAs : "+str(cwma)+ " XMFs : "+str(cxmf)+ " OGGs : "+str(cogg)+ " M4As : "+str(cm4a)+ " WAVs : "+str(cwav))

	# print ("\nMP3s : "+str(cmp3)+ " WMAs : "+str(cwma)+ " XMFs : "+str(cxmf)+ " OGGs : "+str(cogg)+ " M4As : "+str(cm4a)+ " WAVs : "+str(cwav), file=file_obj)

	# print ("\nTotal other files found here: "+str(count),file=file_obj)

	# print ("Done with Search. Your file is here "+dir_path+"/Searching/")
	# file_obj.close()
