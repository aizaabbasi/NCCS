import sys
import requests
import json
from tabulate import tabulate
import numpy as np

def initializeTree():
    tree = {'show': {'contacts': readContacts, 'sms': readSMS},
            'make':{'image':makeImage}
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
    contactsList = []
    # Get response from URL
    response = requests.get('http://127.0.0.1:5000/getContacts')
    # Get JSON response
    contacts = json.loads(response.content)
    # Get contacts
    contacts = contacts['contacts']
    for contact in contacts:
        for name, number in contact.items():
            if not [name,number] in contactsList:       # Only add unique contacts
                contactsList.append([name,number])

    # Table part
    headers = ['Name', 'Number']
    print(tabulate(contactsList, headers=headers, tablefmt='fancy_grid'))


def readSMS():
    smsList = []
    # Get response from URL
    response = requests.get('http://127.0.0.1:5000/getSMS')
    # Get JSON response
    sms = json.loads(response.content)
    sms = sms['sms']
    for x in sms:
        smsList.append([x['Address'],x['Content'],x['Date'],x['Sent']])

    headers = ['Address', 'Content', 'Date Received', 'Date Sent']
    print(tabulate(smsList, headers=headers, tablefmt='fancy_grid'))

def makeImage():
    '''Send request to make android image'''
    headers = {'Content-type': 'application/json'}
    url = 'http://127.0.0.1:5000/makeImage'
    response = requests.post(url, headers=headers)
    print(response)


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
                print(e)

if __name__ == "__main__":
    main()