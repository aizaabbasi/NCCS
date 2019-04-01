import subprocess
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, text, select
import sqlalchemy as db
import sys
from tabulate import tabulate
import subprocess
import numpy as np


def initializeTree():
    tree = {'show': {'contacts': readContacts, 'sms': readSMS}
    }

    return tree

def traverseTree(root, cmd, index):
    for k, v in root.items():
        if index < len(cmd):
            k = cmd[index]
            root = root[k]
            v = root
            if not callable(v):
                index += 1
                traverseTree(root, cmd, index)
            else:
                index += 1
                if index <= len(cmd):
                    v()
    


def readContacts():
    '''Function to read contacts'''
    # Becase SQLAlchemy refused to work
    cmd = ''' sqlite3 contacts.db "select view_data.display_name, phone_lookup.normalized_number
    from phone_lookup, view_data
    where phone_lookup.raw_contact_id = view_data.raw_contact_id;"'''
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
    output = output.decode('utf-8')
    output = output.split('\n')
    contactsList = []
    for x in output:
        x = x.split("|")
        contactsList.append(x)
    
    contactsList = np.unique(contactsList)
    headers = ['Name', 'Number']
    print(tabulate(contactsList, headers=headers, tablefmt='fancy_grid'))

    # engine = create_engine('sqlite:///contacts.db')
    # connection = engine.connect()
    # metadata = db.MetaData()
    # contacts = db.Table('view_data', metadata, autoload=True, autoload_with=engine)
    # select_stmt = select([contacts.c.display_name, contacts.c.data1 + "   " + contacts.c.data2 + "   " + contacts.c.data3 + "   " + contacts.c.data4], distinct=True)
    # result = connection.execute(select_stmt)
    # finalResult = result.fetchall()
    # contactsList = []
    # for x in finalResult:
    #     contactsList.append(x)
    
    # headers = ['Name', 'Data']
    # print(tabulate(contactsList, headers=headers, tablefmt='fancy_grid'))


def readSMS():
    '''Function to read SMS'''
    engine = create_engine('sqlite:///mmssms.db')
    connection = engine.connect()
    metadata = db.MetaData()
    messages = db.Table('messages', metadata, autoload=True, autoload_with=engine)
    select_stmt = select([messages.c.address, messages.c.content, messages.c.date, messages.c.date_sent])
    result = connection.execute(select_stmt)
    finalResult = result.fetchall()
    smsList = []
    for x in finalResult:
        smsList.append(x)


    smsList = smsList[:100]

    tableHeaders = ['Address','Content', 'Date Recieved', 'Data Sent']
    print(tabulate(smsList, headers=tableHeaders, tablefmt='fancy_grid'))

    



def main():
    tree = initializeTree()     # Initialize command tree
    while True:
        # Prompt user for command
        userInput = input("cmd >> ")
        userInput = ' '.join(userInput.split())
        # Check if command is exit
        if userInput == 'exit':
            sys.exit(0)
        else:
            # Traverse command tree according to input
            tempInput = userInput.split()
            try:
                traverseTree(tree, tempInput, 0)
            except Exception as e:
                print("Invalid Command")


if __name__ == "__main__":
    main()
