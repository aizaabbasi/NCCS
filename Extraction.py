import subprocess
from subprocess import check_output as co
from subprocess import call
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sqlalchemy
import sys
from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
from DataExtraction import get_image2
import json
import readline
from flask_table import Table, Col
import numpy as np
from gmplot import gmplot
from datetime import datetime
import datetime

import time
from flask_socketio import SocketIO, emit
import yaml
import re
import getpass
import allAudSearch as ad
import allVidSearch as vd
import allDocSearch as ds
import allPicSearch as ps
import urllib
import csv
from nested_lookup import nested_lookup, get_occurrence_of_key, get_occurrence_of_value

# Contacts table
class ContactsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    name = Col('Name')
    number = Col('Number')

# SMS table
class SMSTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    number = Col('Number')
    content = Col('Content')
    dateReceived = Col('Date Received')
    dateSent = Col('Date Sent')

# SMS table
class CallLogsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    name = Col('Name')
    number = Col('Number')
    date = Col('Date')
    duration = Col('Duration (s)')

# Facebook Contacts table
class FacebookContactsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    first_name = Col('First Name')
    last_name = Col('Last Name')
    display_name = Col('Display Name')

# Whatsapp Contacts table
class WhatsappContactsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    display_name = Col('Display Name')
    number = Col('Number')
    status = Col('Status')

# Whatsapp Messages table
class WhatsappMessagesTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    number = Col('Contact ID')
    

    status = Col('Status')
    timestamp = Col('Timestamp')
    text = Col('Text')
    
    
    
    media_type = Col('Media Type')
    media_size = Col('Media Size')
    media_name = Col('Media Name')
    media_caption = Col('Media Caption')
    

# Whatsapp Groups table
class WhatsappGroupsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    display_name = Col('Display Name')
    group_name = Col('Group Name')
    timestamp = Col('Timestamp')
    text = Col('Text')


# Synced Accounts table
class SyncAccountsTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    accountsName = Col('Accounts Name')


# Synced Accounts table
class DeviceInfoTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    deviceInfo = Col('Device Information')

# Audio Files Table
class AudioFiles(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    audioFiles = Col('Files')

# Chrome Bookmarks Table
class ChromeBookmarksTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    timestamp = Col('Timestamp')
    name = Col('Name')
    url = Col('Url')

# Chrome Login Table
class ChromeLoginTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    url = Col('Url')
    username = Col('Username')
    password = Col('Password')
    times_used=Col('Times Used')

# Chrome Login Table
class ChromeLoginHistory(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    url = Col('Url')
    title = Col('Title')
    last_visit_time = Col('Last Visit Time')

# Autofill Profile Table
class AutofillProfileTable(Table):
    classes = ['table', 'table-striped', 'table-bordered', 'table-hover', 'table-condensed']
    autofill = Col('Autofill Profile')

app = Flask(__name__)
socketio = SocketIO(app)

password = None
device = None
dataPath = None
partitions = None
userPartition = None
partitionSize = 0


def executeCommand(passwd,command):
    '''Execute sudo command'''
    command = command.replace('\n','')
    output = subprocess.check_output('echo {} | sudo -S {}'.format(passwd,command), shell=True)
    output = output.decode('utf-8')
    output = output.split('\n')
    output = output[0]
    output = output.replace('\n','')
    return output 

def cleanFirefox():
    '''
    command = 'rm ~/.mozilla/firefox/*.default/cookies.sqlite' 
    print (command)
    executeCommand("aizaz", command)

    command = 'rm ~/.mozilla/firefox/*.default/*.sqlite ~/.mozilla/firefox/*default/sessionstore.js' 
    print (command)
    executeCommand("aizaz", command)

    
    '''
    command = 'rm -r ~/.cache/mozilla/firefox/*.default/*' 
    print (command)
    executeCommand(password, command)


@app.route('/getPassword', methods=['POST'])
def getPassword():
    '''Get root password from user'''
    '''
    response = request.json
    global password
    password = response['password']
    return "OK", 200
    '''
    global password
    password = request.form['password']
    data = {'password':password}
    # write password file
    with open('password.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
    return render_template("sidebar.html")
    
def readPasswordFile():
    '''Read password from file'''
    global password
    with open("password.yaml", 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    password = data['password']
    return password
    
@app.route('/getImageSize', methods=['GET'])
def getImageSize():
    '''Get size of partitions'''
    global device, dataPath, partitions, userPartition
    device, dataPath, partitions, userPartition = get_image2.getPartitions()
    global partitionSize
    partitionSize = get_image2.getPartitionSize(partitions,userPartition)
    return jsonify(partitionSize)    
    

@app.route('/makeImage', methods=['GET'])
def makeImage():
    '''Make android device image'''
    # Get password
    # response = request.json
    # password = response['password']
    get_image2.makeImage(device, dataPath, userPartition)    # Make image
    return jsonify({'OK': 'Done'})

@socketio.on('getProgress')
def getProgress():
    '''Function to get file writing progress'''
    # Get path of img file
    path = os.getcwd()
    filePath = path + '/android.img'
    fileSize = os.path.getsize(filePath)        # Get size of img file
    global partitionSize
    partitionSize = int(partitionSize)
    fileSize = int(fileSize)/1024               # Converting to KBs
    # print("\n")
    # Keep running till file writing is not complete
    # while fileSize < partitionSize:
    fileSize = os.path.getsize(filePath)        # Get size of img file
    fileSize = int(fileSize)/1024
    perc = (fileSize/partitionSize) * 100   # Get percentage
    # perc = round(perc)
    # perc = str(perc)
    perc = ("%.1f" % perc)
    # print("Progress: " + perc + "%", end='\r')
    emit('progress', {'data': perc})

    # print("\nDone")

@app.route('/mountImage', methods=['GET'])
def mountDeviceImage():
    '''Mount image'''
    mountImage(password)
    return jsonify({'OK': 'Done'})

def mountImage(password):
    '''Function to mount image file'''
    path = os.getcwd()
    mountPath = path + "/static/mounted/"
    if not os.path.isdir(mountPath):
        os.mkdir(mountPath)
    mountCommand = "mount -o loop \"" + path + '/android.img\" \"' + mountPath + '\"'
    # if mnt already exists
    unmountCmd = 'umount \"' + mountPath + '\"'
    if os.path.isdir(mountPath):
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
            subprocess.call('echo {} getPassword| sudo -S {}'.format(password, unmountCmd), shell=True)
        except:
            pass
        # Mount image
        try:
            subprocess.call('echo {} | sudo -S {}'.format(password, mountCommand), shell=True)
        except:
            pass

def takeOwnership(filename):
    '''Take ownership of file'''
    user = getpass.getuser()
    group = subprocess.check_output('id -gn', shell=True)
    group = group.decode('utf-8')
    group = group.replace('\n','')
    cmd = 'chown ' + user + ":" + group + " " + filename
    executeCommand(password, cmd)

# Add route to get contacts
@app.route('/getContacts', methods=['GET'])
def readContacts():
    '''Function to read contacts'''
    findCommand = "find /mnt/android -name contacts2.db"
    contactsPath = subprocess.check_output('echo {} | sudo -S {}'.format(password,findCommand), shell=True)
    contactsPath = (contactsPath.decode('utf-8')).split('\n')
    contactsPath = contactsPath[0]
    copyCommand = 'cp ' + contactsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    # Take ownership
    takeOwnership('contacts2.db')
    # Because SQLAlchemy refused to work
    # cmd = 'sqlite3 ' +  contactsPath + '''select view_data.display_name, phone_lookup.normalized_number
    # from phone_lookup, view_data
    # where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''


    cmd = "select distinct view_data.display_name, phone_lookup.normalized_number from phone_lookup, view_data where phone_lookup.raw_contact_id = view_data.raw_contact_id order by view_data.display_name; \n"

    # Execute query
    # output = subprocess.check_output('echo {} | sudo -S {}'.format(password, cmd), shell=True)
    process = subprocess.Popen("sqlite3 contacts2.db", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.stdin.write(cmd.encode('utf-8'))
    process.stdin.write(cmd.encode('utf-8'))
    stdout = process.communicate()[0]
    output = stdout.decode('utf-8')
    # Get output of query
    output = output.split('\n')

    filterList = []

    # Get contacts and append to list
    contactsList = []
    for x in output:
        x = x.split("|")
        try:
            filterStr = x[0] + "~" + x[1]
            # tempContact = {x[0]:x[1]}
            if not (filterStr in filterList):
                tempContact = dict(name=x[0],number=x[1])
                contactsList.append(tempContact)

            filterList.append(filterStr)
        except:
            pass

    filterList = []
    # Convert contacts list to JSON
    # print (contactsList)
    # return jsonify({'contacts':contactsList})
    table = ContactsTable(contactsList)
    # print (table)
    # return render_template('contacts.html',contactsList=table)
    return jsonify(table)
        
@app.route('/getSMS', methods=['GET'])
def readSMS():
    '''Function to read SMS (For Android 5.0)'''
    findCommand = "find /mnt/android -name mmssms.db"
    # smsPath = subprocess.check_output('echo {} | sudo -S {}'.format(password,findCommand), shell=True)
    smsPath = executeCommand(password, findCommand)
    # Copy file
    copyCommand = 'cp ' + smsPath + ' \"' + os.getcwd() + '\"'
    # subprocess.call('echo {} | sudo -S {}'.format(password,copyCommand), shell=True)
    executeCommand(password, copyCommand)

    # Take ownership
    takeOwnership('mmssms.db')

    # Connect to database
    engine = create_engine('sqlite:///mmssms.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    
    # Get table data
    messages = db.Table('sms', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.address, messages.c.body, messages.c.date, messages.c.date_sent],
    group_by=[messages.c.address],
    order_by=[messages.c.address])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    #print (finalResult)
    smsList = []
    for x in finalResult:
        # tempSms = {'Address':x.address, 'Content':x.body, 'Date':x.date,'Sent':x.date_sent}
        tempSms = dict(number=x[0],content=x[1],dateReceived=datetime.fromtimestamp(x[2]/1e3),dateSent=datetime.fromtimestamp(x[3]/1e3))
        smsList.append(tempSms)


    # smsList = smsList[:50]     # Limit to x number of SMS
    table = SMSTable(smsList)
    return jsonify(table)       # Return table
    # return jsonify({'sms':smsList})     # Return JSON
    
@app.route('/getLogs', methods=['GET'])
def getCallLogs():
    '''Get call logs'''
    findCmd = 'find /mnt/android -name calllog.db'
    logsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + logsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # Take ownership
    takeOwnership('calllog.db')
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
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(name=x[0],number=x[1],date=datetime.fromtimestamp(x[2]/1e3),duration=x[3])
        callLogsList.append(tempLog)

    table = CallLogsTable(callLogsList)
    return jsonify(table)
    # return jsonify({'calllogs':callLogsList})     # Return JSON
    

@app.route('/getWhatsappLocations', methods=['GET'])
def getCallLocations():
    '''Get whatsapp locations'''
    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # Take ownership
    takeOwnership('msgstore.db')
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
            # tempLoc = {'Latitude':x.latitude,'Longitude':x.longitude}
            tempLoc = (x.latitude, x.longitude)
            locationsList.append(tempLoc)

    lats, longs = zip(*locationsList)

    gmap = gmplot.GoogleMapPlotter(33.6007, 73.0679, 13)    # Initialize map
   
    gmap.heatmap(lats, longs)                # Make map
    gmap.draw('static/WhatsappMap.html')     # Save map

    return jsonify({'status':'OK'})
    # return jsonify({'locations':locationsList})     # Return JSON

@app.route('/getLocations', methods=['GET'])
def getLocations():
    '''Get locations'''
    findCmd = 'find /mnt/android -name gmm_sync.db'
    locationsPath = executeCommand(password,findCmd)
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    takeOwnership('gmm_sync.db')
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
    print (finalResult)
    locationsList = []
    for x in finalResult:
        if (x.latitude_e6 != 0) or (x.longitude_e6 != 0):
            # tempLoc = {'Latitude':(x.latitude_e6/1e6),'Longitude':(x.longitude_e6/1e6)}
            tempLoc = (x.latitude_e6/1e6, x.longitude_e6/1e6)
            locationsList.append(tempLoc)

    lats,longs = zip(*locationsList)
    # Place map
    gmap = gmplot.GoogleMapPlotter(33.6007, 73.0679, 13)       # Initialize map
   
    gmap.heatmap(lats, longs)           # Make map
    gmap.draw('static/map.html')        # Save map

    return jsonify({'status':'OK'})
    # return jsonify({'locations':locationsList})     # Return JSON

@app.route("/")
def index():
    global password
    try:
        password = readPasswordFile()
        print(password)
        if password == None:
            return render_template("login.html")
        else:
            return render_template('sidebar.html')
    except:
        return render_template('login.html')


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
    #takeOwnership('/app_gatekeepers/users/')
    
    copyCommand = 'ls ' + os.getcwd() + '/app_gatekeepers/users/'
    x=executeCommand(password, copyCommand)

    print (x)

    #x = z.split(os.sep)[-1]    
    url = 'https://www.facebook.com/'+str(x)
    print (url)
    return url

@app.route('/getFacebookContacts', methods=['GET'])
def getFacebookContacts():
    findCmd = 'find /mnt/android -name contacts_db2'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # chownCommand = 'chown aizazsharif:aizazsharif contacts_db2'  +  ' \"' + os.getcwd() + '\"'
    # executeCommand(password, chownCommand)
    takeOwnership('contacts_db2')
    
    
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
    '''
    friendslist = []
    for x in finalResult:
        if (x.first_name != 0) or (x.last_name != 0) or (x.display_name != 0):
            tempLoc = {'First Name':(x.first_name),'Last Name':(x.last_name),'Display Name':(x.display_name)}
            friendslist.append(tempLoc)
    
    return jsonify({'friendslist':friendslist})     # Return JSON
    '''
    callLogsList = []
    for x in finalResult:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(first_name=x[0],last_name=x[1],display_name=x[2])
        callLogsList.append(tempLog)

    table = FacebookContactsTable(callLogsList)
    return jsonify(table)

@app.route('/getWhatsappContacts', methods=['GET'])
def getWhatsappContacts():
    findCmd = 'find /mnt/android -name wa.db'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # chownCommand = 'chown aizazsharif:aizazsharif wa.db'  +  ' \"' + os.getcwd() + '\"'
    # executeCommand(password, chownCommand)
    
    takeOwnership('wa.db')

    # Get table data
    db = sqlalchemy.create_engine('sqlite:///wa.db')
    
    sql_cmd = sqlalchemy.text('''select display_name,number,status from wa_contacts where is_whatsapp_user='1';''')
    finalResult = db.execute(sql_cmd).fetchall()  
    print (finalResult)
    friendslist = []
    
    for x in finalResult:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(display_name=x[0],number=x[1],status=x[2])
        friendslist.append(tempLog)

    table = WhatsappContactsTable(friendslist)
    return jsonify(table)

    ''' 
    for x in finalResult:
        if (x.display_name != 0) or (x.number) or (x.status!=0):
           tempLoc = {'Display Name':(x.display_name),'Number':(x.number) , 'Status':(x.status)}
           friendslist.append(tempLoc)
    friendslist=friendslist[:50]
    return jsonify({'contactlist':friendslist})     # Return JSON    
    #return locationsPath
    '''

@app.route('/getWhatsappMessages', methods=['GET'])
def getWhatsappMessages():
 
    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # chownCommand = 'chown aizazsharif:aizazsharif msgstore.db'  +  ' \"' + os.getcwd() + '\"'
    # executeCommand(password, chownCommand)
    
    takeOwnership('msgstore.db')
    
    # Connect to database
    engine = create_engine('sqlite:///msgstore.db')   
    connection = engine.connect()
    metadata = db.MetaData()
    
    # Get table data
    rows = db.Table('messages', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.key_remote_jid , rows.c.key_from_me ,rows.c.timestamp, rows.c.data , rows.c.media_mime_type, rows.c.media_size, rows.c.media_name, rows.c.media_caption ])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    finalResult=finalResult[2:50]
    Result = []
    friendslist=[]
    print (finalResult)
    
    for x in finalResult:
        tempLog = dict(number=x[0] ,status=x[1],timestamp=x[2],text=x[3]
        ,media_type=x[4],
        media_size=x[5],media_name=x[6],media_caption=x[7])
        Result.append(tempLog)

    table = WhatsappMessagesTable(Result)
    print (table)
    return jsonify(table)


    '''
    for x in finalResult:
        if (x.key_remote_jid != 0):
            tempLoc = {'Contact ID':(x.key_remote_jid)}
            friendslist.append(tempLoc)
    
    return jsonify({'contactlist':friendslist})     # Return JSON
    '''
     
@app.route('/getWhatsappGroups', methods=['GET'])
def getWhatsappGroups():
    findCmd = 'find /mnt/android -name msgstore.db'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)

    # chownCommand = 'chown aizazsharif:aizazsharif msgstore.db'  +  ' \"' + os.getcwd() + '\"'
    # executeCommand(password, chownCommand)
    
    takeOwnership('msgstore.db')

    # Get table data
    db = sqlalchemy.create_engine('sqlite:///msgstore.db')
    sql_cmd = sqlalchemy.text('''SELECT chat_list.key_remote_jid, chat_list.subject, chat_list.creation, messages_quotes.data
    FROM chat_list
    INNER JOIN messages_quotes ON chat_list.key_remote_jid = messages_quotes.key_remote_jid''')
    finalResult = db.execute(sql_cmd).fetchall()  
    finalResult=finalResult[:50]
    Result = []

    for x in finalResult:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(display_name=x[0],group_name=x[1],timestamp=x[2],text=x[3])
        Result.append(tempLog)

    table = WhatsappGroupsTable(Result)
    return jsonify(table)

    
    '''    
    for x in finalResult:
        if (x.key_remote_jid != 0) or (x.subject) or (x.creation!=0) or (x.data != 0):
            tempLoc = {'Contact ID':(x.key_remote_jid),'Group Name':(x.subject) , 'Timestamp':(x.creation), 'Text':(x.data)}
            friendslist.append(tempLoc)
    friendslist=friendslist[:50]
    return jsonify({'contactlist':friendslist})     # Return JSON
    '''


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
    friendslist=[]
    for x in ACCOUNTS:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(accountsName=x)
        friendslist.append(tempLog)

    table = SyncAccountsTable(friendslist)
    return jsonify(table)

    
    '''
    print (len(ACCOUNTS))    
    return (jsonify(ACCOUNTS))
    '''

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
    #cmd = "adb shell service call iphonesubinfo 1 | awk -F \"'\" '{print $2}' | sed '1 d' | tr -d '.' | awk '{print}' ORS="
    #IMEI = (co(cmd, shell=True)).decode('utf-8')
    IMEI = co(['adb', 'shell', 'service', 'call','iphonesubinfo','16',
     '|','busybox','awk','-F','\"\'\"','\'{print $2}\'','|','busybox','sed'
         ,'\'s/[^0-9A-F]*//g\'','|','busybox','tr','-d','\'\n\'','&&','echo']).decode('UTF-8')
    IMEI=IMEI.strip("\r\n")
    try:
        print(" IMEI: " + IMEI)
    except:
        pass 
    device.append(" IMEI: " + IMEI)
    
    friendslist=[]
    for x in device:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(deviceInfo=x)
        print (x)
        friendslist.append(tempLog)

    table = DeviceInfoTable(friendslist)
    return jsonify(table)

    #return (jsonify({'device':device}))

@app.route('/getAudioFiles', methods=['GET'])
def audioSearch():
    '''Return list of audio files'''
    # audioList = []  # This will have all the files
    audioFileList = ad.getFiles('/mnt/android')    # Call the function to get files
    
    # Iterate over the list of files to convert them to table format
    # for x in audioFileList:
    #     tempFile = dict(audioFiles=x)    # Add to dictionary
    #     audioList.append(tempFile)          # Add dictionary to list

    # table = AudioFiles(audioList)           # Cast to table
    # return jsonify(table)                   # Return table
    # print(audioFileList)
    return jsonify(audioFileList)

@app.route('/getVideoFiles', methods=['GET'])
def videoSearch():
    '''Return list of video files'''
    # videoList = []  # This will have all the files
    videoFileList = vd.getFiles('/mnt/android')    # Call the function to get files
    
    # Iterate over the list of files to convert them to table format
    # for x in videoFileList:
    #     tempFile = dict(videoFiles=x)    # Add to dictionary
    #     videoList.append(tempFile)          # Add dictionary to list

    # table = videoFiles(videoList)           # Cast to table
    # return jsonify(table)                   # Return table
    # print(videoFileList)
    return jsonify(videoFileList)


@app.route('/getDocuments', methods=['GET'])
def docSearch():
    '''Return list of documents'''
    # docList = []  # This will have all the files
    docFileList = ds.getFiles('/mnt/android')    # Call the function to get files
    
    # Iterate over the list of files to convert them to table format
    # for x in docFileList:
    #     tempFile = dict(docFiles=x)    # Add to dictionary
    #     docList.append(tempFile)          # Add dictionary to list

    # table = DocFiles(docList)           # Cast to table
    # return jsonify(table)                   # Return table
    # print(docFileList)
    return jsonify(docFileList)

@app.route('/getPictures', methods=['GET'])
def picSearch():
    '''Return list of pictures'''
    # picList = []  # This will have all the files
    picFileList = ps.getFiles('/mnt/android')    # Call the function to get files
    
    # Iterate over the list of files to convert them to table format
    # for x in picFileList:
    #     tempFile = dict(picFiles=x)    # Add to dictionary
    #     picList.append(tempFile)          # Add dictionary to list

    # table = picFiles(picList)           # Cast to table
    # return jsonify(table)                   # Return table
    # print(picFileList)
    return jsonify(picFileList)


def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result

def date_from_webkit(webkit_timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    print (epoch_start + delta)
    return epoch_start + delta
     

@app.route('/getChromeBookmarks', methods=['GET'])
def getChromeBookmarks():
    findCmd = 'find /mnt/android -name Bookmarks'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"***********")

   
    copyCommand = 'cp ' + locationsPath + ' \"' + os.getcwd() + '\"'
    executeCommand(password, copyCommand)
    textfile = open('result','w')

    takeOwnership('Bookmarks')
    filee=open('Bookmarks','r')
    for line in filee.readlines():
        textfile.write(line)
        if "folder" in line:
            textfile.writelines(',')
            textfile.write('\n "url": "None" ')
    textfile.close()    
    with open('result') as data_file:    
        data = json.load(data_file)
    children=list(find('children', data))

    
    date_added=nested_lookup('date_added', children)
    name=nested_lookup('name', children)
    url=nested_lookup('url', children)
    print ("date_added :",len(date_added))
    print ("name :",len(name))
    print ("url :",len(url))
    #print (json.dumps(children, indent=2, sort_keys=True))

    for i in range(len(date_added)):
        print (date_added[i], " ", name[i]," ",url[i])
        date_added[i]=date_from_webkit(date_added[i])
    friendslist=[]
    for i in range(len(date_added)):
        tempLog = dict(timestamp=date_added[i],name=name[i],url=url[i])
        
        friendslist.append(tempLog)

    table = ChromeBookmarksTable(friendslist)
    return jsonify(table)


@app.route('/getChromeLogin', methods=['GET'])
def getChromeLogin():
    findCmd = 'find /mnt/android -name Login\ Data'
    locationsPath = executeCommand(password,findCmd)
    
    
    copyCommand = 'cp ' + locationsPath[:-10] + "Login\ Data" +" " + os.getcwd()    
    executeCommand(password, copyCommand)

    chownCommand = 'chown aizazsharif:aizazsharif Login\ Data'
    executeCommand(password, chownCommand)

    # Connect to database
    engine = create_engine('sqlite:///Login Data')   
    connection = engine.connect()
    metadata = db.MetaData()
    
    rows = db.Table('logins', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.action_url , rows.c.username_value ,rows.c.password_value, rows.c.times_used])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    #finalResult=finalResult[:50]
    
    Result = []

    for x in finalResult:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(url=x[0],username=x[1],password=(x[2][:2].decode("utf-8")+"..."),times_used=x[3])
        Result.append(tempLog)

    table = ChromeLoginTable(Result)
    return jsonify(table)
    
    #return "yes"

@app.route('/getChromeHistory', methods=['GET'])
def getChromeHistory():
    findCmd = 'find /mnt/android -name History'
    locationsPath = executeCommand(password,findCmd)
    print (locationsPath,"**************")
    
    copyCommand = 'cp ' + locationsPath +" " + os.getcwd()    
    executeCommand(password, copyCommand)
    takeOwnership('History')
    
    # Connect to database
    engine = create_engine('sqlite:///History')   
    connection = engine.connect()
    metadata = db.MetaData()
    
    rows = db.Table('urls', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.url , rows.c.title ,rows.c.last_visit_time])
    # Execute query
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    finalResult=finalResult[:20]
    
    Result = []

    for x in finalResult:
        # tempLog = {'Name':x.name,'Number':x.number,'Date':x.date,'Duration':x.duration}
        tempLog = dict(url=str(x[0])[:25],title=x[1],last_visit_time=date_from_webkit(x[2]))
        Result.append(tempLog)

    table = ChromeLoginHistory(Result)
    return jsonify(table)
    
    
@app.route('/getChromeWebData', methods=['GET'])
def getChromeWebData():
    #findCmd = 'find /mnt/android -name Web\ Data'
    locationsPath = '/mnt/android/data/com.android.chrome/app_chrome/Default/'
    #locationsPath = executeCommand(password,findCmd)
    
    
    copyCommand = 'cp ' + locationsPath + "Web\ Data" +" " + os.getcwd()    
    executeCommand(password, copyCommand)

    chownCommand = 'chown aizazsharif:aizazsharif Web\ Data'
    executeCommand(password, chownCommand)

    # Connect to database
    engine = create_engine('sqlite:///Web Data')   
    connection = engine.connect()
    metadata = db.MetaData()
     
    autofill = [] 
    #For autofill email
    rows = db.Table('autofill_profile_emails', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.email ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("Email : "+str(x) )

    #For autofill names
    rows = db.Table('autofill_profile_names', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.first_name,rows.c.last_name ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("Name : "  +str(x[0]) + " " + str(x[1]) )
 

    #For autofill phone number
    rows = db.Table('autofill_profile_phones', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.number ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("Phone Number : "+str(x) )
 
    #For autofill profiles
    rows = db.Table('autofill_profiles', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.city ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("City : "+str(x) )

    rows = db.Table('autofill_profiles', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.zipcode ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("Zipcode : "+str(x) )
  
    rows = db.Table('autofill_profiles', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([rows.c.country_code ])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    
    for x in finalResult:

        autofill.append("Country Code : "+str(x) )
 
    
    
    print (autofill)
    
    info=[]
    for x in autofill:
        tempLog = dict(autofill=x)
        info.append(tempLog)

    table = AutofillProfileTable(info)
    
    return jsonify(table)


def main():
    
    try:
        cleanFirefox()
    except Exception as e:
        print(e)
        
    socketio.run(app)
    
if __name__ == "__main__":
    main()
