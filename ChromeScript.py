#Import Libreries
from asyncio.windows_events import NULL
from datetime import date
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
#test
#hello mega update
#-----------------------------------------------------------

#Define a Classes

class OnPremAccounts:
    number = NULL
    name = ""
    producInstances = ""
    syncup = ""
    syncdown = ""
    syncdue = ""
    version = ""
    
    def __init__(number,name,productinstances,syncup,syncdown,syncdue,version):
        self.number = number






#Definition of methods
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
    else:
        if(option == 2):
            return('Last Sync Up to On-Prem')
        else:
            if(option == 3):
                return('Last Down Up to On-Prem')
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

def printOnPremAccountDetails(contador,recordTracker):
    print('        Record Number: ' + str(recordTracker))
    print('Account Name: ' + onPremAccountName(contador))
    print('Product Instances: ' + onPremAccountProductInstance(contador))
    print('Last Sync Up from On-Prem: ' + onPremAccountLastSyncUp(contador))
    print('Last Sync Down to On-Prem: ' + onPremAccountLastSyncDown(contador))
    print('Synchronization Due: ' + onPremAccountSyncDue(contador))
    print('Version: ' + onPremAccountVersion(contador))

def writeOnPremAccountDetails(contador,recordTracker):
    log.write('\n        Record Number: ' + str(recordTracker))
    log.write('\nAccount Name: ' + onPremAccountName(contador))
    log.write('\nProduct Instances: ' + onPremAccountProductInstance(contador))
    log.write('\nLast Sync Up from On-Prem: ' + onPremAccountLastSyncUp(contador))
    log.write('\nLast Sync Down to On-Prem: ' + onPremAccountLastSyncDown(contador))
    log.write('\nSynchronization Due: ' + onPremAccountSyncDue(contador))
    log.write('\nVersion: ' + onPremAccountVersion(contador))



#-----------------------------------------------------------
#Tittle
print('\n\n')
print('\t █▀█ █▄ █ ▄▄ █▀█ █▀█ █▀▀ █▀▄▀█  ▄▀█ █▀▀ █▀▀ █▀█ █ █ █▄ █ ▀█▀ █▀  █▀▄ █▀▀ █   █▀▀ ▀█▀ █▀▀ █▀█')
print('\t █▄█ █ ▀█    █▀▀ █▀▄ ██▄ █ ▀ █  █▀█ █▄▄ █▄▄ █▄█ █▄█ █ ▀█  █  ▄█  █▄▀ ██▄ █▄▄ ██▄  █  ██▄ █▀▄')
print('\t\t\t\t\t\t\t\t\t\t\t 𝕓𝕪 𝕛𝕒𝕗𝕖𝕥𝕙\n\n')
os.system('PAUSE')

log = open('log.txt', 'w')

#Access the Web Page34
options = webdriver.ChromeOptions()
options.add_argument('--log-level 3') 
driver = webdriver.Chrome()

print("--------------")
print("Process: Opening WebPage")
driver.get("https://software.cisco.com/software/smart-licensing/onprem-accounts")
print("Process: COMPLETED")
print("--------------")

#Typyng Email
print("Process: Loging Email")
typeXPATH('jgarroro@cisco.com','//*[@id="userInput"]')
print("Process: COMPLETED")
print("--------------")

#Click Loging
clickXPATH('//*[@id="login-button"]')

#Waiting 1 second for password page to load
time.sleep(1)
#Typing the password and click loging
print("Process: Loging Password")
typeXPATH('Sykescisco2022*','//*[@id="passwordInput"]')
print("Process: COMPLETED")
print("--------------")

#Click Loging
clickXPATH('//*[@id="login-button"]')

#Waiting for user to complete 2FA with a 25 seconds time out
print("Process: Waiting for user to complete 2FA")
try:
    TrustBrowserbutton = waitForElementXpath(25,'//*[@id="trust-browser-button"]')
    TrustBrowserbutton.click()
    print("Process: COMPLETED")
    print("--------------")

except:
    print('*********************** USER AUTHENTICATION TIME OUT ***********************')
    driver.quit()
    sys.exit()

#Wating for OnPrem Accounts WebPage to load by checking if the "next button" is present
print("Process: Loading WebPage")
try:
    nextButton = waitForElementXpath(30,'//*[@id="ui-icon-seek-next"]')
    print("Process: COMPLETED")
    print("-------------------------------------------")
except:
    print('*********************** Loading Page Time Out ***********************')
    driver.quit()
    sys.exit()

#Caputre Numbers for the Parameters with Data Validation
while(True):

    print('  Select the Criteria to Flag the On-Prem Account')
    print('       ************************************')
    print('       *   1- Synchronization Due         *')
    print('       *   2- Last Sync Up to On-Prem     *')
    print('       *   3- Last Sync Down to On-Prem   *')
    print('       ************************************')

    while(True):
        optionSTR = str(input('Select one option: '))

        if(optionSTR.upper() == 'EXIT' ):
            print('> Program Aborted <')
            sys.exit()

        if(checkIsDigit(optionSTR)):
            option = int(optionSTR)
            if(option == 1 or option == 2 or option == 3):
                break
            else:
                print('> INPUT ERROR: Select a valid number (1,2,3) <')
        else:
            print('> INPUT ERROR: Select a valid number (1,2,3) <')

    records = getOnPremOnRecords('//*[@id="slick-pager-status"]')
    print("-------------------------------------------")
    print("On-Prem accounts on records detected: " + str(records) )
    print("-------------------------------------------")
    print('- - - - - - - S̲E̲T̲ P̲A̲R̲A̲M̲E̲T̲E̲R̲S̲ - - - - - - - -')
    while(True):
        yearsSTR = str(input('Introduce the ' + syncString(option) + ' Year limit: '))

        if(optionSTR.upper() == 'EXIT' ):
            print('> Program Aborted <')
            sys.exit()

        if(checkIsDigit(yearsSTR)):
            years = int(yearsSTR)
            if(years>date.today().year or years < 2018):
                print('> INPUT ERROR: Add a valid year (2018 - Current Year) <')
            else:
                break
        else:
            print('> INPUT ERROR: Add a valid number <')
    
    

    print('-------------------------------------------')
    print('- - - - - - D̲A̲T̲A̲ C̲O̲N̲F̲I̲R̲M̲A̲T̲I̲O̲N̲ - - - - - - -')
    print('The script will review ' + str(records) + ' On-Prem Accounts')
    print('and will flag all the accounts with ' + syncString(option).upper() + ' before ' + str(years))
    print('- - - - - - - - - - - - - - - - - - - - - - ')
    
    while(True):
        confirmation = input('Is the information correct? [y/n]: ')

        if(confirmation.upper() == 'EXIT' ):
            print('> Program Aborted <')
            sys.exit()

        if(confirmation == 'y' or confirmation == 'Y' or confirmation == 'N' or confirmation == 'n'):
            break
        else:
            print('> INPUT ERROR: Please input a valid Answer <')
    
    if(confirmation == 'y' or confirmation == 'Y'):
        break
    else:
        os.system('CLS')
        print('^^ Please write new values for the parameters ^^')


#Cycle through the OnPrem Accounts Grid Using two loops
#The outside loop cycle through the Pages and the Inside loop cycle through the rows
norecords= 0
warnings = 0
recordTracker = 1
page = 0
exitWhile = False

log.write('\t\t\t On-Prem Account Deleter Log - By Jafeth \n Date: ' + str(date.today()) + '\n Time: ' + str(datetime.now().strftime("%H:%M:%S")) + '\n')

while True:

    contador = 1
    print('###### PAGE: ' +str(page + 1) + ' ######')

    while contador <= 10:

        if(option == 1):
            onPremYear = onPremAccountSyncDue(contador)
        elif(option == 2):
            onPremYear = onPremAccountLastSyncUp(contador)
        else:
            onPremYear = onPremAccountLastSyncDown(contador)
        

        print('-----------------------------------')
        printOnPremAccountDetails(contador,recordTracker)


        if(noRecordsWarning(onPremYear,option,log)):
            log.write('\n-----------------------------------')
            
            writeOnPremAccountDetails(contador,recordTracker)

            log.write("\nWARNING ^^^^^  NO " + syncString(option).upper() + " ON RECORDS ^^^^^ WARNING")
            log.write('\n-----------------------------------')
            norecords += 1

        if(syncDueWarning(onPremYear,years,option,log)):
            log.write('\n-----------------------------------')

            writeOnPremAccountDetails(contador,recordTracker)

            log.write("\nWARNING ^^^^^ The " + syncString(option).upper() + " WAS DONE BEFORE " + str(years) + " ^^^^^ WARNING")
            log.write('\n-----------------------------------')
            warnings+=1

        print('-----------------------------------')

        #Check if the counters reached the OnPrem on records
        if(recordTracker == records):
            break

        contador += 1
        recordTracker += 1
        
    if(recordTracker == records):
        break

    page += 1
    nextButton.click()

    try:
        spinner = WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="spinner-backdrop"]'))
        )

    except:
        \
        print('*********************** Loading Page Time Out ***********************')
        driver.quit()
        sys.exit()

print('\nTotal Of Servers with ' + syncString(option) + ' Outdated: ', warnings)
log.write('\nTotal Of Servers with ' + syncString(option) + ' Outdated: ' + str(warnings))

print('Total Of Servers with no ' + syncString(option) + ' records: ', norecords)
log.write('\nTotal Of Servers with no ' + syncString(option) + ' records: ' + str(norecords))
log.close()
print('\n*********************** Process Completed ***********************')