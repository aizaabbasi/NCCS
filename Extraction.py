import subprocess
from subprocess import check_output as co
from subprocess import call
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sqlalchemy
import sys
import re
from flask import Flask, jsonify, request
import os
from DataExtraction import get_image
import json
import readline

app = Flask(__name__)

password = ''

def executeCommand(passwd,command):
    '''Execute sudo command'''
    output = subprocess.check_output('echo {} | sudo -S {}'.format(passwd,command), shell=True)
    output = output.decode('utf-8')
    output = output.split('\n')
    output = output[0]
    output = output.replace('\n','')
    return output 

@app.route('/getPassword', methods=['POST'])
def getPassword():
    response = request.json
    global password
    password = response['password']
    return "OK", 200

@app.route('/makeImage', methods=['GET'])
def makeImage():
    # Get password
    # response = request.json
    # password = response['password']
    get_image.getImage()    # Make image
    mountImage(password)    # Mount image
    return jsonify({'OK': 'OK'})

def mountImage(password):
    '''Function to mount image file'''
    path = os.getcwd()
    mountCommand = "mount -o loop \"" + path + '/android.img\" /mnt/android'
    # if mnt already exists
    unmountCmd = 'umount /mnt/android'
    if os.path.isdir('/mnt/android'):
        # Unmount image
        try:
            subprocess.call('echo {} | sudo -S {}'.format(password, unmountCmd), shell=True)
        except:
            pass
        # Mount image
        try:
            subprocess.call('echo {} | sudo -S {}'.format(password, mountCommand), shell=True)
        except:
            pass
        
    else:       # Create directory
        # Unmount image
        try:
            subprocess.call('echo {} | sudo -S {}'.format(password, unmountCmd), shell=True)
        except:
            pass
        # Mount image
        try:
            subprocess.call('echo {} | sudo -S {}'.format(password, mountCommand), shell=True)
        except:
            pass


# Add route to get contacts
@app.route('/getContacts', methods=['GET'])
def readContacts():
    '''Function to read contacts'''
    findCommand = "find /mnt/android -name contacts2.db"
    contactsPath = subprocess.check_output('echo {} | sudo -S {}'.format(password,findCommand), shell=True)
    contactsPath = contactsPath.decode('utf-8')
    # Because SQLAlchemy refused to work
    # cmd = 'sqlite3 ' +  contactsPath + '''select view_data.display_name, phone_lookup.normalized_number
    # from phone_lookup, view_data
    # where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''

    print ("****************")
    
    cmd = '''sqlite3 contacts.db "select view_data.display_name, phone_lookup.normalized_number
    #from phone_lookup, view_data
    #where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''
    # Execute query
    output = subprocess.check_output('echo {} | sudo -S {}'.format(password, cmd), shell=True)
    # Get output of query
    output = output.decode('utf-8')
    output = output.split('\n')

    # Get contacts and append to list
    contactsList = []
    for x in output:
        x = x.split("|")
        try:
            tempContact = {x[0]:x[1]}
            contactsList.append(tempContact)
        except:
            pass
    
    # Convert contacts list to JSON
    return jsonify({'contacts':contactsList})
    

    
@app.route('/getSMS', methods=['GET'])
def readSMS():
    '''Function to read SMS'''
    findCommand = "find /mnt/android -name mmssms.db"
    # smsPath = subprocess.check_output('echo {} | sudo -S {}'.format(password,findCommand), shell=True)
    smsPath = executeCommand(password, findCommand)
    # Copy file
    copyCommand = 'cp ' + smsPath + ' \"' + os.getcwd() + '\"'
    # subprocess.call('echo {} | sudo -S {}'.format(password,copyCommand), shell=True)
    executeCommand(password, copyCommand)
    # Connect to database
    engine = create_engine('sqlite:///mmssms.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    # Get table data
    messages = db.Table('messages', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.address, messages.c.content, messages.c.date, messages.c.date_sent])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    smsList = []
    for x in finalResult:
        tempSms = {'Address':x.address, 'Content':x.content, 'Date':x.date,'Sent':x.date_sent}
        smsList.append(tempSms)


    smsList = smsList[:3]     # Limit to x number of SMS
    return jsonify({'sms':smsList})     # Return JSON

@app.route('/getLogs', methods=['GET'])
def getCallLogs():
    '''Get call logs'''
    findCmd = 'find /mnt/android -name calllog.db'
    logsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + logsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    # Connect to database
    engine = create_engine('sqlite:///calllog.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    # Get table data
    messages = db.Table('calls', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.name, messages.c.number, messages.c.date, messages.c.duration])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    callLogsList = []
    for x in finalResult:
        tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        callLogsList.append(tempLog)

    return jsonify({'calllogs':callLogsList})     # Return JSON

@app.route('/getWhatsappLocations', methods=['GET'])
def getCallLocations():
    '''Get whatsapp locations'''
    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    # Connect to database
    engine = create_engine('sqlite:///msgstore.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    # Get table data
    messages = db.Table('messages', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.latitude, messages.c.longitude])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    locationsList = []
    for x in finalResult:
        if (x.latitude != 0) or (x.longitude != 0):
            tempLoc = {'Latitude':x.latitude,'Longitude':x.longitude}
            locationsList.append(tempLoc)

    return jsonify({'locations':locationsList})     # Return JSON

@app.route('/getLocations', methods=['GET'])
def getLocations():
    '''Get whatsapp locations'''
    findCmd = 'find /mnt/android -name gmm_sync.db'
    locationsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    # Connect to database
    engine = create_engine('sqlite:///gmm_sync.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    # Get table data
    messages = db.Table('sync_item_data', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.latitude_e6, messages.c.longitude_e6])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    locationsList = []
    for x in finalResult:
        if (x.latitude_e6 != 0) or (x.longitude_e6 != 0):
            tempLoc = {'Latitude':(x.latitude_e6/1e6),'Longitude':(x.longitude_e6/1e6)}
            locationsList.append(tempLoc)

    return jsonify({'locations':locationsList})     # Return JSON


@app.route('/getFacebookUserName', methods=['GET'])
def getFacebookUserName():
    findCmd = 'find /mnt/android -name app_gatekeepers'
    locationsPath = executeCommand(password,findCmd)
    copyCommand = 'cp -r ' + locationsPath +     ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    
    y = os.getcwd()
    print (y,"****************")
    
    copyCommand = 'chown aizazsharif:aizazsharif ' + os.getcwd() + '/app_gatekeepers/users/'  +  ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    
    copyCommand = 'ls '+ os.getcwd()+'/app_gatekeepers/users/'
    x=executeCommand(password, copyCommand)

    print (x)

    #x = z.split(os.sep)[-1]    
    
    return x

@app.route('/getFacebookContacts', methods=['GET'])
def getFacebookContacts():
    findCmd = 'find /mnt/android -name contacts_db2'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    chownCommand = 'chown aizazsharif:aizazsharif contacts_db2'  +  ' \"' + os.getcwd() + '\"'
    executeCommand(password, chownCommand)
    
    
    # Connect to database
    engine = create_engine('sqlite:///contacts_db2')   
    connection = engine.connect()
    metadata = db.MetaData()
    
    # Get table data
    rows = db.Table('contacts', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.first_name, rows.c.last_name,rows.c.display_name ])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    friendslist = []
    for x in finalResult:
        if (x.first_name != 0) or (x.last_name != 0) or (x.display_name != 0):
            tempLoc = {'First Name':(x.first_name),'Last Name':(x.last_name),'Display Name':(x.display_name)}
            friendslist.append(tempLoc)
    
    return jsonify({'friendslist':friendslist})     # Return JSON

    #return locationsPath

@app.route('/getWhatsappContacts', methods=['GET'])
def getWhatsappContacts():

    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    chownCommand = 'chown aizazsharif:aizazsharif msgstore.db'  +  ' \"' + os.getcwd() + '\"'
    executeCommand(password, chownCommand)
    
    
    # Connect to database
    engine = create_engine('sqlite:///msgstore.db')   
    connection = engine.connect()
    metadata = db.MetaData()

    # Get table data
    rows = db.Table('messages', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.key_remote_jid, rows.c.key_from_me ,rows.c.timestamp, rows.c.data, rows.c.media_mime_type, rows.c.media_size, rows.c.media_name, rows.c.media_caption ])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    friendslist = []


    for x in finalResult:
        if (x.key_remote_jid != 0) or (x.key_from_me) or (x.timestamp!=0) or (x.data != 0) or (x.media_mime_type != 0)or (x.media_size != 0)or (x.media_name != 0)or (x.media_caption != 0):
            tempLoc = {'Contact ID':(x.key_remote_jid),'Status':(x.key_from_me) , 'Timestamp':(x.timestamp), 'Text':(x.data),'Media Type':(x.media_mime_type),
                'Media Size':(x.media_size),'Media Name':(x.media_name),'Media Caption':(x.media_caption)}
            friendslist.append(tempLoc)
    friendslist=friendslist[:100]
    return jsonify({'contactlist':friendslist})     # Return JSON

@app.route('/getWhatsappGroups', methods=['GET'])
def getWhatsappGroups():
    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    chownCommand = 'chown aizazsharif:aizazsharif msgstore.db'  +  ' \"' + os.getcwd() + '\"'
    executeCommand(password, chownCommand)
    
    # Get table data
    db = sqlalchemy.create_engine('sqlite:///msgstore.db')
    sql_cmd = sqlalchemy.text('''SELECT chat_list.key_remote_jid, chat_list.subject, chat_list.creation, messages_quotes.data
    FROM chat_list
    INNER JOIN messages_quotes ON chat_list.key_remote_jid = messages_quotes.key_remote_jid''')
    finalResult = db.execute(sql_cmd).fetchall()  
    friendslist = []
    
    for x in finalResult:
        if (x.key_remote_jid != 0) or (x.subject) or (x.creation!=0) or (x.data != 0):
            tempLoc = {'Contact ID':(x.key_remote_jid),'Group Name':(x.subject) , 'Timestamp':(x.creation), 'Text':(x.data)}
            friendslist.append(tempLoc)
    friendslist=friendslist[:50]
    return jsonify({'contactlist':friendslist})     # Return JSON

@app.route('/getSyncedAccounts', methods=['GET'])
def getSyncedAccounts():
    ALLACC = co(['adb', 'shell', 'dumpsys', 'account']).decode('UTF-8')
    all_acc = re.compile('Account {name=', re.DOTALL).finditer(ALLACC)
    ACCOUNTS = []
    
    
    for acc in all_acc:
        hit_pos = acc.start()
        tacc = ALLACC[hit_pos+14:]
        end_pos = tacc.index('}')
        acc0 = tacc[:end_pos].replace(' type=', '').split(',')
        acc = acc0[1]+": "+acc0[0]
        ACCOUNTS.append(acc)
    return (jsonify({'accounts':ACCOUNTS}))

@app.route('/getDeviceInfo', methods=['GET'])
def getDeviceInfo():   
    device=[]

    
    # Check permissions
    QPERM = co(['adb', 'shell', 'id']).decode('UTF-8')
    if 'root' in QPERM:
        PERM = 'root'
    else:
        QPERMSU = co(['adb', 'shell', 'su', '-c', 'id']).decode('UTF-8')
        if 'root' in QPERMSU:
            PERM = 'root(su)'
        else:
            PERM = 'shell(non-rooted)'
    print(" Shell permissions: " + PERM)
    device.append(" Shell permissions: " + PERM)
     
    # Make & Model
    BUILDPROP = co(['adb', 'shell', 'cat', '/system/build.prop']).decode('UTF-8')
    for manuf in BUILDPROP.split('\n'):
        if 'ro.product.manufacturer' in manuf:
            DEVICE_MANUF = manuf.strip().split('=')[1]
    for model in BUILDPROP.split('\n'):
        if 'ro.product.model' in model:
            DEVICE_MODEL = model.strip().split('=')[1]
    try:
        print(" Device model: %s %s" % (DEVICE_MANUF, DEVICE_MODEL))
    except:
        pass

    device.append(" Device model: %s %s" % (DEVICE_MANUF, DEVICE_MODEL))    
    
    # Build ID
    for buildid in BUILDPROP.split('\n'):
        if 'ro.build.display.id' in buildid:
            BUILD_ID = buildid.strip().split('=')[1]
    try:
        print(" Build number: " + BUILD_ID)
    except:
        pass

    device.append(" Build number: " + BUILD_ID)


    # Wifi
    DUMPSYS_W = co(['adb', 'shell', 'dumpsys', 'wifi']).decode('UTF-8')
    try:
        wifi_beg = DUMPSYS_W.index('MAC:')+5
        wifi_end = DUMPSYS_W[wifi_beg:].index(',')
        if wifi_end == 17:
            WIFI_MAC = DUMPSYS_W[wifi_beg:wifi_beg+wifi_end].lower()
            try:
                print(" Wi-fi MAC: " + WIFI_MAC)
            except:
                pass
    except:
        pass

    device.append(" Wi-fi MAC: " + WIFI_MAC)
    

    # IMEI
    IMEI = co(['adb', 'shell', 'service', 'call','iphonesubinfo','16',
    '|','busybox','awk','-F','\"\'\"','\'{print $2}\'','|','busybox','sed'
        ,'\'s/[^0-9A-F]*//g\'','|','busybox','tr','-d','\'\n\'','&&','echo']).decode('UTF-8')
    IMEI=IMEI.strip("\r\n")
    try:
        print(" IMEI: " + IMEI)
    except:
        pass 
    device.append(" IMEI: " + IMEI)
    return (jsonify({'device':device}))



    
def main():
    app.run()

    # mountImage()


if __name__ == "__main__":
    main()
