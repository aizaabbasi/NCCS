# Python code to search vIDEO files in current
# folder (We can change file type/name and path
# according to the requirements.

import os

#This is to save other path
#path="/home/aiza/myPython/mybackup/"
path = "/mnt/android/"

# This is to get the directory that the program
# is currently running in.

#passing path
#dir_path = os.path.dirname(os.path.realpath(path))
dir_path = path

def getFiles(dir_path):
	'''Function to get miscellaneous files'''
	#count for total files
	num=count=0
	c3gpp=cmp4=cmkv=cmpts=cwebM=0

	fileList = []		# This will hold the list of files
## How to Run
	#file_obj = open("allVid_csv_output.txt", "w")

	#csvobj = open("allVid_csv.csv", "w")

	#columnTitleRow = "Path, File Name\n"
	#csvobj.write(columnTitleRow)

	for root, dirs, files in os.walk(dir_path):
	
		for file in files:
	        		# change the extension from '.3GPP to  
			# the one of your choice.
			if file.endswith('.3gpp'):
			
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				c3gpp=c3gpp+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)
			

			elif file.endswith('.mp4'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cmp4=cmp4+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)
		
			elif file.endswith('.mkv'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cmkv=cmkv+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.mpts'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cmpts=cmpts+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.webm'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cwebM=cwebM+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			else:	count=count+1
	return fileList

	#print ("\nTotal files found here : "+str(c3gpp)+ " plus " +str(cmp4)+ " plus " +str(cmkv)+ " plus " +str(cmpts)+ " plus " +str(cwebM)+" equals "+str(num), file=file_obj)

	#print ("\n3GPPs : "+str(c3gpp)+ " MP4s : "+str(cmp4)+ " MKVs : "+str(cmkv)+ " MPTSs : "+str(cmpts)+ " webMs : "+str(cwebM))

	#print ("\n3GPPs : "+str(c3gpp)+ " MP4s : "+str(cmp4)+ " MKVs : "+str(cmkv)+ " MPTSs : "+str(cmpts)+ " webMs : "+str(cwebM), file=file_obj)

	#print ("\nTotal other files found here: "+str(count),file=file_obj)

	#print ("Done with Search. Your file is here "+dir_path+"/Searching/")
	#file_obj.close()
