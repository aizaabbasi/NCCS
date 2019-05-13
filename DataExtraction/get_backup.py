# takes your backup.tar.gz and turns it in to folders.
# Aiza Aqeel Abbasi on April 09, 2019


# 1. adb backup and restore
# 2. from .ab to .tar.gz
# 3. from .tar.gz to folders


import argparse 
from functools import partial                                                                     
import shutil                                                                      
import zlib
import tarfile
import backup.py as backupRestore

def get_backup():
	backupRestore.main()


def abdecompresso(data, dest):
	parser = argparse.ArgumentParser("Decompresses an unencrypted android backup file into tar format") 
	parser.add_argument("backup_file", help="The file to decompress")                                   
	parser.add_argument("dest_tar", help="The destination tar file path")                               

	args = parser.parse_args([data, dest])                
	#passing both the backup file and destination path for tar.gz                                                          
	if args.dest_tar is None:
		dest = shutil.mktemp()                                                                          
	else:
		dest = args.dest_tar                                                                            

	print ("Stripping off the first 24 bytes of the backup file")                                        
	dest_file = open(dest, "wb")                                                                        
	orig = open(args.backup_file, "rb")                                                                 
	orig.seek(24)                                                                                       
	print ("Decompressing the file 1024 bytes at a time" )                                                
	decompressor = zlib.decompressobj(zlib.MAX_WBITS)                                                   
	for cur_chunk in iter(partial(orig.read, 1024), b''):
		decompressed_chunk = decompressor.decompress(cur_chunk)
		dest_file.write(decompressed_chunk)                                                             
	dest_file.flush()                                                                                   
	dest_file.close()
                                                                                  
	print ("Done! Resulting tar is here: {}".format(dest))
	#print(dest)                                           
	return tarextracto(dest)

def tarextracto(source):
	try:
		tar = tarfile.open(source)
		tar.extractall(path="/DataExtraction/Backups")
		print(" Done! Resulting directories are here: {}".format(source))
		tar.close()
	except tarfile.ReadError:
       		print("File {} is corrupt".format(source))

def main():
  get_backup()
	b_file = "/Backups/backup.ab"
	des_tar = "/Backups/maintar.tar.gz"
	abdecompresso(b_file, des_tar)

