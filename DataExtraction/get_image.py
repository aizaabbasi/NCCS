import subprocess
from adb.client import Client as AdbClient
import sys        
import re
import os
import threading
import time
        
def getByNamePath(paths):
    '''Function that prevents error on finding by-name'''
    paths = paths.split('\n')
    finalPath = None
    for x in paths:
        if 'by-name' in x:
            finalPath = x

    return finalPath

def getSDCardPath(paths):
    '''Get SD Card path'''
    paths = paths.split('\n')
    finalPath = None
    for x in paths:
        if x == '/sdcard':
            finalPath = x

    return finalPath


def getPath(paths, findPath):
    '''Function to get path of userdata directory'''
    paths = paths.split('\n')
    path = None
    for x in paths:
        # Search for USERDATA
        if findPath in x:
            temp = x.split('->')    # Get path of userdata
            path = temp[-1]

    return path

def getPartitionSize(partitions, userPartition):
    '''Function to get size of userdata partition'''
    partitions = partitions.split('\n')
    desiredPartition = None
    partitionSize = 0
    for part in partitions:
        if userPartition in part:
            desiredPartition = part
            desiredPartition = ' '.join(desiredPartition.split()) # Combine multiple spaces into one space
            desiredPartition = desiredPartition.split(' ')
            partitionSize = desiredPartition[2]     # Size is at third place

    return partitionSize

def getProgress(partitionSize):
    '''Function to get file writing progress'''
    # Get path of img file
    path = os.getcwd()
    filePath = path + '/android.img'
    fileSize = os.path.getsize(filePath)        # Get size of img file
    partitionSize = int(partitionSize)
    fileSize = int(fileSize)/1024               # Converting to KBs
    print("\n")
    # Keep running till file writing is not complete
    while fileSize < partitionSize:
        fileSize = os.path.getsize(filePath)        # Get size of img file
        fileSize = int(fileSize)/1024
        perc = (fileSize/partitionSize) * 100   # Get percentage
        perc = round(perc)
        perc = str(perc)
        print("Progress: " + perc + "%", end='\r')

    print("\nDone")

def executeCommand(dataPath, ansi_escape):
    '''Function to execute shell commands'''
    # Get root access
    rootProcess = subprocess.Popen("adb -d shell", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    rootProcess.stdin.write('su \n'.encode('utf-8'))
    # dd command
    ddCmd = 'dd if=' + dataPath + ' | busybox nc -l -p 8888 \n'
    try:
        ddCmd = ansi_escape.sub('',ddCmd)
    except:
        pass
    rootProcess.stdin.write(ddCmd.encode('utf-8'))
    stdout, stderr = rootProcess.communicate()
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    
def getDevice():
    # Start adb
    subprocess.call('adb start-server', shell=True)
    # Connect to adb
    client = AdbClient(host="127.0.0.1", port=5037)
    # Get devices
    devices = client.devices()
    if not len(devices) > 0:
        print('Error in connecting device')
        sys.exit(0)
    else:
        devices = devices[0]
        serialNumber = devices.get_serial_no()
        device = client.device(serialNumber)
        return device
    
def getImage(device):
    # Get path of data directory
    try:
        tempPath = device.shell('su -c find / -name by-name')
        tempPath = getByNamePath(tempPath)
        tempPath = tempPath.replace('\r','')
        cmd = 'su -c ls -al ' + tempPath
        path = device.shell(cmd)
        dataPath = getPath(path, 'USERDATA')
        dataPath = dataPath.strip()
        # print(dataPath)
    except Exception as e:
        print('Error getting user data directory')
        print(e)
        sys.exit(0)

    try:
        # Get partition size
        tempPartition = dataPath.split('/')
        userPartition = tempPartition[-1]                       # Get user data partition
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        userPartition = ansi_escape.sub('',userPartition)       # Remove ANSI
        partitions = device.shell('cat /proc/partitions')       # Get all partitions
        partitionSize = getPartitionSize(partitions,userPartition)
    except Exception as e:
        print('Error getting partitions')
        print(e)
        sys.exit(0)

    try:
        # Kill dd
        device.shell('su -c pkill -9 dd')

        # Kill nc
        device.shell('su -c pkill -9 nc')

        # Open ports for forwarding
        subprocess.Popen('adb forward tcp:8888 tcp:8888', shell=True)

        # Make dd file
        threading.Thread(target=executeCommand, args=(dataPath, ansi_escape,)).start()
        time.sleep(0.5)

        # Write img file to forensic system
        ncCmd = 'nc 127.0.0.1 8888 > android.img'
        subprocess.Popen(ncCmd, shell=True)
        time.sleep(0.2)            

        # Get file writing progress
        getProgress(partitionSize)

    except Exception as e:
        print(e)
        sys.exit(0)       

def getSDCard(device):
    '''Function to copy SD Card contents'''
    # Get path of sdcard directory
    try:
        tempPath = device.shell('su -c find / -name sdcard')
        tempPath = tempPath.replace('\r','')
        tempPath = getSDCardPath(tempPath)
        cmd = 'adb pull ' + tempPath
        subprocess.call(cmd, shell=True)    # Pull sd card directory
    except Exception as e:
        print('SD Card directory not found')
        print(e)
