import subprocess
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sys
from flask import Flask, jsonify
import os

app = Flask(__name__)

def mountImage():
    '''Function to mount image file'''
    path = os.getcwd()
    path = path + '/Data Extraction Scripts/'
    mountCommand = "sudo mount -o loop \"" + path + 'android.img\" /mnt/android'
    # if mnt already exists
    if os.path.isdir('/mnt/android'):
        subprocess.call(mountCommand, shell=True)
    else:       # Create directory
        subprocess.call('sudo mkdir /mnt/android', shell=True)
        subprocess.call(mountCommand, shell=True)


# Add route to get contacts
@app.route('/getContacts', methods=['GET'])
def readContacts():
    '''Function to read contacts'''
    # Because SQLAlchemy refused to work
    cmd = ''' sqlite3 contacts.db "select view_data.display_name, phone_lookup.normalized_number
    from phone_lookup, view_data
    where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''
    # Execute query
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
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
    # app.run()
    mountImage()


if __name__ == "__main__":
    main()
