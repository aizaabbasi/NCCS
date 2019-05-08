# Python code to search .jpg files in current
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
	cpng=cjpg=cbmp=cgif=cwebp=0

	fileList = []		# This will hold the list of files

## How to Run

	#file_obj = open("all_csv_output.txt", "w")

	#csvobj = open("all_csv.csv", "w")

	#columnTitleRow = "Path, File Name\n"
	#csvobj.write(columnTitleRow)

	for root, dirs, files in os.walk(dir_path):
	
		for file in files:
	        		# change the extension from '.jpg to  
			# the one of your choice.
			if file.endswith('.jpg'):
			
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cjpg=cjpg+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)
			

			elif file.endswith('.png'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cpng=cpng+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)
		
			elif file.endswith('.bmp'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cbmp=cbmp+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.gif'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cgif=cgif+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.webp'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cwebp=cwebp+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			else:	count=count+1
	return fileList

	#print ("\nTotal files found here : "+str(cpng)+ " plus " +str(cjpg)+ " plus " +str(cbmp)+ " plus " +str(cgif)+" equals "+str(num)+ " plus " +str(cwebp), file=file_obj)

	#print ("\nPNGs : "+str(cpng)+ " JPEGs : "+str(cjpg)+ " BMPs : "+str(cbmp)+ " GIFs : "+str(cgif)+ " webPs : "+str(cwebp))

	#print ("\nPNGs : "+str(cpng)+ " JPEGs : "+str(cjpg)+ " BMPs : "+str(cbmp)+ " GIFs : "+str(cgif)+ " webPs : "+str(cwebp), file=file_obj)

	#print ("\nTotal other files found here: "+str(count),file=file_obj)

	#print ("Done with Search. Your file is here "+dir_path+"/Searching/")
	#file_obj.close()
