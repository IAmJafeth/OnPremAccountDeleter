#Import Libreries
from asyncio.windows_events import NULL
from datetime import date
from functools import total_ordering
from operator import truediv
from pickle import FALSE, TRUE
from turtle import down, up
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import sys
from selenium.webdriver.remote.remote_connection import LOGGER
from datetime import datetime
import chromedriver_binary
from getpass import getpass
import re

#-----------------------------------------------------------

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

#Define a Classes

class OnPremAccounts:
    number = 0
    name = ""
    producInstances = ""
    syncup = ""
    syncdown = ""
    syncdue = ""
    version = ""

    def __init__(self,number,name,productinstances,syncup,syncdown,syncdue,version):
        self.number = number
        self.name = name
        self.productInstances = productinstances
        self.syncup = syncup
        self.syncdown = syncdown
        self.syncdue = syncdue
        self.version = version
    
    def printDetails(self):
        print('        Record Number: ' + str(self.number))
        print('Account Name: ' + self.name)
        print('Product Instances: ' + self.producInstances)
        print('Last Sync Up from On-Prem: ' + self.syncup)
        print('Last Sync Down to On-Prem: ' + self.syncdown)
        print('Synchronization Due: ' + self.syncdue)
        print('Version: ' + self.version)

    def writeDetails(self,log):
        log.write('\n        Record Number: ' + str(self.number))
        log.write('\nAccount Name: ' + self.name)
        log.write('\nProduct Instances: ' + self.producInstances)
        log.write('\nLast Sync Up from On-Prem: ' + self.syncup)
        log.write('\nLast Sync Down to On-Prem: ' + self.syncdown)
        log.write('\nSynchronization Due: ' + self.syncdue)
        log.write('\nVersion: ' + self.version)

#Definition of methods
def progressBar(part, total, lenght=30):
    frac = part/total
    completed = int(frac * lenght)
    missing = lenght - completed
    bar = f"[{'#'*completed}{'-'*missing}]{frac:.2%}"
    return bar


def findElementXPATH (xpath):
    return(driver.find_element(By.XPATH, xpath))

def clickXPATH (xpath):
    x = findElementXPATH (xpath)
    x.click()

def waitForElementXpath (seconds,xpath):
    return(WebDriverWait(driver, seconds).until(EC.presence_of_element_located((By.XPATH, xpath))))

def typeXPATH (text,xpath):
    x = findElementXPATH ( xpath)
    x.send_keys(text)

def extractYear(text):
    if(text == ''):
        return(9999)
    x = ''
    for i in range (4):
        x +=str(text[i])
    return (int(x))

def compareNumsGT(number1,number2):
    return(number1>number2)

def compareYearsGT(year,dateText):
    return(compareNumsGT(year,extractYear(dateText)))

def syncString(option):
    if(option == 1):
        return('Synchronization Due')
    elif(option == 2):
        return('Last Sync Up to On-Prem')
    elif(option == 3):
        return('Last Down Up to On-Prem')
    elif(option == 0):
        return('Not scanned yet')
    else:
        return('>ERROR<')

def noRecordsWarning(syncdate,option,log):

    if(extractYear(syncdate) == 9999):
        print("WARNING ^^^^^^^^^^  NO " + syncString(option).upper() + " ON RECORDS ^^^^^^^^^^ WARNING")
        return(True)
    else:
        return(False)

def syncDueWarning(syncdate,year,option,log):

    if(compareYearsGT(year,syncdate)):
        print("WARNING ^^^^^^^^^^ THE " + syncString(option).upper() + " WAS DONE BEFORE " + str(year) + " ^^^^^^^^^^ WARNING")
        return(True)
    else:
        return(False)

def checkIsDigit(input_str):
    if input_str.strip().isdigit():
        return True
    else:
        return False

def checkEmail(email):
    if(re.fullmatch(regex, email)):
        return True

    print(">>Invalid Email<<\n")
    return False


def onPremAccountName(contador):
    accountName = findElementXPATH ('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[1]/a')
    return(accountName.text)

def onPremAccountProductInstance(contador):
    productInstances = findElementXPATH ('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[2]')
    return(productInstances.text)

def onPremAccountLastSyncUp(contador):
    lastSyncUp = findElementXPATH ('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[3]')
    return(lastSyncUp.text)

def onPremAccountLastSyncDown(contador):
    lastSyncDown = findElementXPATH ('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[4]')
    return(lastSyncDown.text)

def onPremAccountSyncDue(contador):
    syncDue = findElementXPATH('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[5]')
    return(syncDue.text)

def onPremAccountVersion(contador):
    version = findElementXPATH ('//*[@id="onprem-grid"]/div[4]/div[3]/div/div[' + str(contador) + ']/div[6]')
    return(version.text)

def getXpathText(xpath):
    x = findElementXPATH(xpath)
    return x.text

def getOnPremOnRecords(xpath):
    enter = False
    recordSTR = ''
    string = getXpathText(xpath)
    for element in range(0, len(string)):

        if(enter):
            if checkIsDigit(string[element]):
                recordSTR += string[element]
            else:
                record = int(recordSTR)
                return record

        if(string[element] == '('):
            enter = True



#-----------------------------------------------------------
#Tittle
print('\n\n')
print('\t █▀█ █▄ █ ▄▄ █▀█ █▀█ █▀▀ █▀▄▀█  ▄▀█ █▀▀ █▀▀ █▀█ █ █ █▄ █ ▀█▀ █▀  █▀▄ █▀▀ █   █▀▀ ▀█▀ █▀▀ █▀█')
print('\t █▄█ █ ▀█    █▀▀ █▀▄ ██▄ █ ▀ █  █▀█ █▄▄ █▄▄ █▄█ █▄█ █ ▀█  █  ▄█  █▄▀ ██▄ █▄▄ ██▄  █  ██▄ █▀▄')
print('\t\t\t\t\t\t\t\t\t\t\t 𝕓𝕪 𝕛𝕒𝕗𝕖𝕥𝕙\n\n')
os.system('PAUSE')

print('\n>>DO NOT CLOSE THE GOOGLE CHROME WINDOW<<\n')

logoptions = webdriver.ChromeOptions()
logoptions.add_argument('--log-level 3') 
driver = webdriver.Chrome()

records = 'Not synchronized'
accountPassword = ''
accountEmail = ''
nextButton = ''
option = 0



log = open('log.txt', 'w')
accountsetup = False
accountsscanned = False
passwordChanged = False
alreadyLogin = False
accounts = []

time.sleep(4)

while(True):
    while(True):

        print('\n                       Main Menu        ')
        print('       ************************************     Total of OnPrem Accounts on Records: ' + str(records))
        print('       *   1- Setup password and email    * ')
        print('       *   2- Scan OnPremAccounts         * ')
        print('       *   3- Clean OnPremAccounts        * ')
        print('       *   Type EXIT to abort the program * ')
        print('       ************************************\n' )

        while(True):
                menuoptionSTR = str(input('Select one option: '))

                if(menuoptionSTR.upper() == 'EXIT' ):
                    print('> Program Aborted <')
                    driver.quit()
                    log.close()
                    sys.exit()

                if(checkIsDigit(menuoptionSTR)):
                    menuoption = int(menuoptionSTR)
                    if(menuoption == 1 or menuoption == 2 or menuoption == 3):
                        break
                    else:
                        print('> INPUT ERROR: Select a valid number (1,2,3) <')
                else:
                    print('> INPUT ERROR: Select a valid number (1,2,3) <')


        if(menuoption == 1):
            print('\n\t\t Account Setup')

            while(True):
                accountEmail = str(input("Enter your email: "))
                if(checkEmail(accountEmail)):
                    break

            accountPassword = getpass()
            print("\n> CREDENTIALS SAVED <\n")
            accountsetup = True
            passwordChanged = True

        elif(menuoption == 2):
            if(not accountsetup):
                print("\n>>Please Configure an Email and Password First<<")
            elif(passwordChanged and alreadyLogin):
                print("\n>>RESTART THE SCRIPT DUE TO CREDENTIALS CHANGE<<")
                log.close()
                sys.exit()

            else:
                print("\n--------------")
                print("Process: Opening WebPage")
                try:
                    driver.get("https://software.cisco.com/software/smart-licensing/onprem-accounts")
                except:
                    print("\n>>> WEBPAGE TIMEOUT <<<")
                    print('> RETURNING TO MAIN MENU <')
                    break
                print("Process: COMPLETED")
                print("--------------")

                if(not alreadyLogin):

                    try:
                        typeXPATH(accountEmail,'//*[@id="userInput"]')
                    except:
                        print("\n>>> WEBPAGE TIMEOUT <<<")
                        print('> RETURNING TO MAIN MENU <')
                        break
                    
                    print("Process: Loging Email")
                    
                    try:
                        clickXPATH('//*[@id="login-button"]')
                    except:
                        print("\n>>> WEBPAGE TIMEOUT <<<")
                        print('> RETURNING TO MAIN MENU <')
                        break

                    

                    #Waiting 1 second for password page to load
                    time.sleep(1)
                    #Typing the password and click loging
                    try:
                        typeXPATH(accountPassword,'//*[@id="passwordInput"]')
                    except:
                        print("\n>>> EMAIL ERROR: Check the Email Configuratione <<<")
                        print('> RETURNING TO MAIN MENU <')
                        break
                    
                    print("Process: COMPLETED")
                    print("--------------")

                    #Click Loging
                    print("Process: Loging Password")
                    try:
                        clickXPATH('//*[@id="login-button"]')
                    except:
                        print("\n>>> WEBPAGE TIMEOUT <<<")
                        print('> RETURNING TO MAIN MENU <')
                        break
                    
                    print("Process: COMPLETED")
                    print("--------------")
                    
                    #Waiting for user to complete 2FA with a 25 seconds time out
                    print("Process: Waiting for user to complete 2FA")

                    try:
                        TrustBrowserbutton = waitForElementXpath(25,'//*[@id="trust-browser-button"]')
                    except:
                        print("\n>>> PASSWORD ERROR: Check the Password that was configured <<<")
                        print('> RETURNING TO MAIN MENU <')
                        break
                    
                    print("Process: COMPLETED")
                    print("--------------")

                    
                    try:
                        TrustBrowserbutton.click()
                    except:
                        print('\n>>> USER AUTHENTICATION TIME OUT <<<')
                        print('> RETURNING TO MAIN MENU <')
                        break

                    print("Process: COMPLETED")
                    print("--------------")

                passwordChanged = False
                alreadyLogin = True

                #Wating for OnPrem Accounts WebPage to load by checking if the "next button" is present
                print("Process: Loading WebPage")
                try:
                    nextButton = waitForElementXpath(30,'//*[@id="ui-icon-seek-next"]')
                    print("Process: COMPLETED")
                    print("--------------\n")
                except:
                    print('\n>>> Loading Page Time Out <<<')
                    print('> RETURNING TO MAIN MENU <')
                    break

                print('Do you want to display the On-Prem Account Details During the Scan?')
                print(' y = Print Details                     n = Show Progress Bar Only\n')
                print('  Type EXIT to abort the program')
                print('  Type CANCEL to return to the MAIN MENU\n')

                while(True):
                    confirmation = input('\nSelection [y/n]: ')

                    if(confirmation.upper() == 'EXIT' ):
                        print('> Program Aborted <')
                        log.close()
                        sys.exit()

                    if(confirmation.upper() == 'CANCEL' ):
                        print('\n> RETURNING TO MAIN MENU <')
                        break

                    if(confirmation == 'y' or confirmation == 'Y' or confirmation == 'N' or confirmation == 'n'):
                        break
                    else:
                        print('> INPUT ERROR: Please input a valid Answer <')

                if(confirmation.upper() == 'CANCEL' ):
                    break
            
                if(confirmation == 'y' or confirmation == 'Y'):
                    displayDetails = True
                else:
                    displayDetails = False  

                records = getOnPremOnRecords('//*[@id="slick-pager-status"]')

                recordTracker = 1
                page = 0

                print('\n Total of On-Premm Accounts: ' + str(records))
                print('Scanning On-Prem Accounts')
                
                while True:

                    contador = 1

                    while contador <= 10:

                        accounts.append(OnPremAccounts(recordTracker,onPremAccountName(contador),onPremAccountProductInstance(contador),onPremAccountLastSyncUp(contador),onPremAccountLastSyncDown(contador),onPremAccountSyncDue(contador),onPremAccountVersion(contador)))
                        
                        if(not displayDetails):
                            print('Account Number: ' + str(recordTracker) + ' ' + progressBar(recordTracker,records), end='\r')
                        else:
                            print('-----------------------------------')
                            accounts[recordTracker - 1].printDetails()
                            print('-----------------------------------')


                        if(recordTracker == records):
                            break
                        contador += 1
                        recordTracker += 1
                        
                    if(recordTracker == records):
                        print('\n*********************** Process Completed ***********************\n')
                        accountsscanned = True
                        break

                    page += 1
                    nextButton.click()

                    try:
                        spinner = WebDriverWait(driver, 30).until(
                        EC.invisibility_of_element_located((By.XPATH, '//*[@id="spinner-backdrop"]'))
                        )

                    except:
                        print('\n>>> Loading Page Time Out <<<')
                        print('> RETURNING TO MAIN MENU <')
                        break

        elif(menuoption == 3):
            if(not accountsscanned):
                print("\n>>Please Complete a On-Prem Accounts Scan First<<")
            else:
                print('  Select the Criteria to Flag the On-Prem Account\n')
                print('  1- Synchronization Due     ')
                print('  2- Last Sync Up to On-Prem ')
                print('  3- Last Sync Down to On-Prem\n')
                print('  Type EXIT to abort the program')
                print('  Type CANCEL to return to the MAIN MENU\n')


                while(True):
                    optionSTR = str(input('Select one option: '))

                    if(optionSTR.upper() == 'EXIT' ):
                        print('> Program Aborted <')
                        driver.quit()
                        log.close()
                        sys.exit()

                    if(optionSTR.upper() == 'CANCEL' ):
                        print('\n> RETURNING TO MAIN MENU <')
                        break

                    if(checkIsDigit(optionSTR)):
                        option = int(optionSTR)
                        if(option == 1 or option == 2 or option == 3):
                            break
                        else:
                            print('> INPUT ERROR: Select a valid number (1,2,3) <')
                    else:
                        print('> INPUT ERROR: Select a valid number (1,2,3) <')

                if(optionSTR.upper() == 'CANCEL' ):
                    break

                print("\n----------------------------")
                print('    Setup Parameters\n')
                while(True):
                    yearsSTR = str(input('Introduce the ' + syncString(option) + ' Year limit: '))

                    if(optionSTR.upper() == 'EXIT' ):
                        print('> Program Aborted <')
                        driver.exit()
                        log.close()
                        sys.exit()

                    if(checkIsDigit(yearsSTR)):
                        years = int(yearsSTR)
                        if(years>date.today().year or years < 2018):
                            print('> INPUT ERROR: Add a valid year (2018 - Current Year) <\n')
                        else:
                            break
                    else:
                        print('> INPUT ERROR: Add a valid number <\n')

                #Cycle through the OnPrem Accounts Grid Using two loops
                #The outside loop cycle through the Pages and the Inside loop cycle through the rows
                norecords= 0
                warnings = 0
                log.write('\t\t\t On-Prem Account Deleter Log - By Jafeth \n Date: ' + str(date.today()) + '\n Time: ' + str(datetime.now().strftime("%H:%M:%S")) + '\n')

                for i in accounts:

                    if(option == 1):
                        onPremYear = i.syncdue
                    elif(option == 2):
                        onPremYear = i.syncup
                    else:
                        onPremYear = i.syncdown
                    

                    print('-----------------------------------')
                    i.printDetails()


                    if(noRecordsWarning(onPremYear,option,log)):
                        log.write('\n-----------------------------------')
                        
                        i.writeDetails(log)

                        log.write("\nWARNING ^^^^^  NO " + syncString(option).upper() + " ON RECORDS ^^^^^ WARNING")
                        log.write('\n-----------------------------------')
                        norecords += 1

                    if(syncDueWarning(onPremYear,years,option,log)):
                        log.write('\n-----------------------------------')

                        i.writeDetails(log)

                        log.write("\nWARNING ^^^^^ The " + syncString(option).upper() + " WAS DONE BEFORE " + str(years) + " ^^^^^ WARNING")
                        log.write('\n-----------------------------------')
                        warnings+=1

                    print('-----------------------------------')

                        #Check if the counters reached the OnPrem on records

                print('\nTotal Of Servers with ' + syncString(option) + ' Outdated: ', warnings)
                log.write('\nTotal Of Servers with ' + syncString(option) + ' Outdated: ' + str(warnings))

                print('Total Of Servers with no ' + syncString(option) + ' records: ', norecords)
                log.write('\nTotal Of Servers with no ' + syncString(option) + ' records: ' + str(norecords))
                
                print('\n*********************** Process Completed ***********************')