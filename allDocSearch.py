# Python code to search DOCS files in current
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


def getFiles(dir_path, graph_path):
	'''Function to get miscellaneous files'''
	num=count=0
	cdoc=cdocx=cpdf=cpptx=cxlsx=cepub=0

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
			if file.endswith('.doc'):
				
				dic = { root : str(file)} #dictionary
				
				# print (dic, file=file_obj)
				num=num+1
				cdoc=cdoc+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row = path + "/" + filename + "\n"
					fileList.append(row)
					# csvobj.write(row)

			elif file.endswith('.docx'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cdocx=cdocx+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)
		
			elif file.endswith('.pdf'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cpdf=cpdf+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.pptx'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cpptx=cpptx+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			elif file.endswith('.xlsx'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cxlsx=cxlsx+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					# csvobj.write(row)
	
			elif file.endswith('.epub'):
		
				dic = { root : str(file)} #dictionary
			
				#print (dic, file=file_obj)
				num=num+1
				cepub=cepub+1

				for key in dic.keys():
					path = key
					filename = dic[key]
					row =path + "/" + filename + "\n"
					fileList.append(row)
					#csvobj.write(row)

			else:	count=count+1
	# return fileList


	#print ("\nTotal files found here : "+str(cdoc)+ " plus " +str(cdocx)+ " plus " +str(cpdf)+ " plus " +str(cpptx)+ " plus " +str(cxlsx)+ " plus " +str(cepub)+" equals "+str(num), file=file_obj)

	#print ("\nDOCs : "+str(cdoc)+ " DOXs : "+str(cdocx)+ " PDFs : "+str(cpdf)+ " PPTs : "+str(cpptx)+ " XLSs : "+str(cxlsx)+ " ePUBs : "+str(cepub))

	#print ("\nDOCs : "+str(cdoc)+ " DOXs : "+str(cdocx)+ " PDFs : "+str(cpdf)+ " PPTs : "+str(cpptx)+ " XLSs : "+str(cxlsx)+ " ePUBs : "+str(cepub), file=file_obj)

	#print ("\nTotal other files found here: "+str(count),file=file_obj)

	#print ("Done with Search. Your file is here "+dir_path+"/Searching/")
	#file_obj.close()
