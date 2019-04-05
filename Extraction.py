import subprocess
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sys
from flask import Flask, jsonify, request
import os
from DataExtraction import get_image
import json

app = Flask(__name__)

password = ''

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
    # get_image.getImage()    # Make image
    mountImage(password)    # Mount image
    return "OK", 200

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
    findCommand = "find /mnt -name contacts2.db"
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
    findCommand = "find /mnt -name mmssms.db"
    smsPath = subprocess.check_output('echo {} | sudo -S {}'.format(password,findCommand), shell=True)
    smsPath = smsPath.decode('utf-8')
    # Copy file
    copyCommand = 'cp ' + smsPath + " " + os.getcwd()
    copyProc = subprocess.call('echo {} | sudo -S {}'.format(password,copyCommand), shell=True)
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


    smsList = smsList[:3]     # Limit to 100 SMS
    return jsonify({'sms':smsList})     # Return JSON

def main():
    app.run()
    # mountImage()


if __name__ == "__main__":
    main()
