import subprocess
from adb.client import Client as AdbClient
import sys        
        
def getPath(paths):
    '''Function to get path of userdata directory'''
    paths = paths.split('\n')
    path = None
    for x in paths:
        # Search for USERDATA
        if 'USERDATA' in x:
            temp = x.split('->')    # Get path of userdata
            path = temp[-1]

    return path


def getImage():
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

        # Get path of data directory
        tempPath = device.shell('su -c find / -name by-name')
        tempPath = tempPath.replace('\r\n','')
        cmd = 'su -c ls -al ' + tempPath
        path = device.shell(cmd)
        dataPath = getPath(path)
        dataPath = dataPath.strip()
        print(dataPath)
        

def main():
    getImage()

if __name__ == "__main__":
    main()