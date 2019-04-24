import sys
import requests
import json
from tabulate import tabulate
import numpy as np
from yaspin import yaspin
import time
from yaspin.spinners import Spinners
import yaml
import os
from pprint import pprint
from datetime import datetime
from getpass import getpass
import readline
import webbrowser
import urllib.parse

def initializeTree():
    tree = {'show': 
                {'contacts': readContacts,
                 'sms': readSMS,
                 'help': showHelp,
                 'logs': showLogs,
                 'locations': showLocations,
                 'facebookuser':getFacebookUserName,
                 'facebookContacts':getFacebookContacts
                 },
            'make':
                {'image':makeImage
                }
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
                return traverseTree(root, cmd, index)
            else:
                index += 1
                if index <= len(cmd):
                    v()

def getResponse(path):
    '''Get response from server'''
    url = 'http://127.0.0.1:5000/' + path
    response = requests.get(url)
    finalResponse = json.loads(response.content)
    return finalResponse

def showHelp():
    '''Display help'''
    path = os.getcwd()          # Get current working directory
    path = path + '/help.yaml'  # Get path of help file
    help = None
    # Open and print help file
    with open(path,'r') as stream:
        try:
            help = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    helpList = []
    for k,v in help.items():
        helpList.append([k,v])

    headers = ['Command', 'Description']
    print(tabulate(helpList, headers=headers, tablefmt='rst'))

def getFacebookUserName():
    '''Get Facebook User Name'''
    contactsList = []
    # Get response from URL
    contacts = getResponse('getFacebookUserName')
    # Get contacts
   
    url = 'https://www.facebook.com/'+str(contacts)

    print (url)
    webbrowser.open(url)
    
    print (contacts)
    
def getFacebookContacts():
    '''Get Facebook User Friends List'''

    contactsList = []
    # Get response from URL
    contacts = getResponse('getFacebookContacts')
    print (contacts)
    # Get contacts
    for x in contacts['friendslist']:
        contactsList.append([str(x['Display Name']),str(x['First Name']),str(x['Last Name'])])
        #contactsList.append(x)
    print (contactsList)    
    
    headers = ['Display_Name','First Name', 'Last Name']
    print(tabulate(contactsList, headers=headers, tablefmt='fancy_grid'))
    
def readContacts():
    '''Get list of contacts'''
    contactsList = []
    # Get response from URL
    contacts = getResponse('getContacts')
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
    '''Get list of text messages'''
    smsList = []
    # Get response from URL
    sms = getResponse('getSMS')
    sms = sms['sms']
    for x in sms:
        smsList.append([x['Address'],x['Content'],datetime.fromtimestamp(x['Date']/1e3),datetime.fromtimestamp(x['Sent']/1e3)])

    headers = ['Address', 'Content', 'Date Received', 'Date Sent']
    print(tabulate(smsList, headers=headers, tablefmt='fancy_grid'))

def showLogs():
    '''Get list of call logs'''
    callLogsList = []
    # Get response from url
    response = getResponse('getLogs')
    callLogs = response['calllogs']
    for x in callLogs:
        callLogsList.append([x['Name'],x['Number'],datetime.fromtimestamp(x['Date']/1e3),str(x['Duration']) + 's'])

    headers = ['Name', 'Number', 'Date', 'Duration']
    print(tabulate(callLogsList, headers=headers, tablefmt='fancy_grid'))

def showLocations():
    '''Get list of whatsapp locations'''
    locationsList = []
    # Get response from url
    response = getResponse('getWhatsappLocations')
    locations = response['locations']
    for x in locations:
        locationsList.append([x['Latitude'],x['Longitude']])

    # Get response from second URL
    response2 = getResponse('getLocations')
    locations2 = response2['locations']
    for x in locations2:
        locationsList.append([x['Latitude'],x['Longitude']])

    headers = ['Latitude', 'Longitude']
    print(tabulate(locationsList, headers=headers, tablefmt='fancy_grid'))


def makeImage():
    '''Send request to make android image'''
    headers = {'Content-type': 'application/json'}
    spinner = yaspin(Spinners.simpleDots, text='Creating Image')
    spinner.start()
    response = getResponse('makeImage')
    print()
    # print(response)
    spinner.stop()

def getPassword():
    '''Get root password'''
    headers = {'Content-type': 'application/json'}
    url = 'http://127.0.0.1:5000/getPassword'
    password = getpass('Root Password: ')
    data = {'password':password}
    response = requests.post(url, json.dumps(data), headers=headers)
    # print(response)


def main():
    getPassword()
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