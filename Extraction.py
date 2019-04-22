import subprocess
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sys
from flask import Flask, jsonify, request, render_template, redirect, url_for
import os
from DataExtraction import get_image
import json
import readline
from flask_table import Table, Col
import numpy as np
from gmplot import gmplot

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

app = Flask(__name__)

password = 'asim'

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
    global password
    password = request.form['password']
    print(password)
    return render_template("sidebar.html")
    


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
            subprocess.call('echo {} getPassword| sudo -S {}'.format(password, unmountCmd), shell=True)
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
    cmd = '''sqlite3 contacts.db "select view_data.display_name, phone_lookup.normalized_number
    from phone_lookup, view_data
    where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''
    # Execute query
    output = subprocess.check_output('echo {} | sudo -S {}'.format(password, cmd), shell=True)
    # Get output of query
    output = output.decode('utf-8')
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
    # return jsonify({'contacts':contactsList})
    table = ContactsTable(contactsList)
    # return render_template('contacts.html',contactsList=table)
    return jsonify(table)

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
        # tempSms = {'Address':x.address, 'Content':x.content, 'Date':x.date,'Sent':x.date_sent}
        tempSms = dict(number=x[0],content=x[1],dateReceived=x[2],dateSent=x[3])
        smsList.append(tempSms)


    smsList = smsList[:50]     # Limit to x number of SMS
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
        tempLog = dict(name=x[0],number=x[1],date=x[2],duration=x[3])
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
    '''Get locations'''
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
            # tempLoc = {'Latitude':(x.latitude_e6/1e6),'Longitude':(x.longitude_e6/1e6)}
            tempLoc = (x.latitude_e6/1e6, x.longitude_e6/1e6)
            locationsList.append(tempLoc)

    lats,longs = zip(*locationsList)
    # Place map
    gmap = gmplot.GoogleMapPlotter(33.6007, 73.0679, 13)
   

    gmap.heatmap(lats, longs)
    # gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=40, marker=False)
    gmap.draw('templates/map.html')

    return jsonify({'status':'OK'})
    # return jsonify({'locations':locationsList})     # Return JSON

@app.route("/")
def index():
    return render_template("login.html")

def main():
    app.run()
    # mountImage()


if __name__ == "__main__":
    main()
