import subprocess
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sys
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


def main():
    app.run()

    # mountImage()


if __name__ == "__main__":
    main()
