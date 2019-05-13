"""Script ADB backup and restore commands."""

import subprocess
from adb.client import Client as AdbClient

backuploc = '/DataExtraction/Backups/backup.ab'


def menu():
    """Display options displayed when script is run."""
    choice = input('Backup or Restore: ')
    choice = choice.upper()

    if choice == 'B':
        adbfullbackup()

    elif choice == 'R':
        adbrestore()

    else:
        input('''Invalid choice.
              Please type \"B\" or \"R\". Press any key to try again: ''')
        menu()


def adbfullbackup():
    """Back up everything."""
    global backuploc
    adbcmd = './adb backup -apk -shared -all'
    #subprocess.call('adb backup -apk -shared -all  ', shell=True)
    runfullcmd(adbcmd)
    print ("your backup is at location {}". format(backuploc))


def adbrestore():
    """Restore backed up data."""
    global backuploc
    adbcmd = 'adb restore ' + backuploc + 'backup.ab'

    runfullcmd(adbcmd)


def runfullcmd(c):
    """Run the command prompt with the chosen operation(s)."""
    global backuploc
    #p = subprocess.Popen(["echo", "hello world"], stdout=subprocess.PIPE)

    #print ( p.communicate())
    subprocess.call(c, shell=True)

def backupmanage():
    """Move backups around to save previous versions."""
    """
    TODO:
        * File management options for user
        * Backup retention
        * Work with restore command (rename to backup.ab)
    """

def main():
	menu()
