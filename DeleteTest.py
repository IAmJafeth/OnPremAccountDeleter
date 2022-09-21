from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

os.system('CLS')

driver = webdriver.Chrome()
driver.get("https://software.cisco.com/software/smart-licensing/onprem-accounts")

loginEmail = driver.find_element(By.XPATH, '//*[@id="userInput"]')
loginEmail.send_keys('jgarroro@cisco.com')

next = driver.find_element(By.XPATH, '//*[@id="login-button"]')
next.click()

time.sleep(1)

loginPassword= driver.find_element(By.XPATH, '//*[@id="passwordInput"]')
loginPassword.send_keys('Sykescisco2022*')

loginButton = driver.find_element(By.XPATH, '//*[@id="login-button"]')
loginButton.click()

os.system('CLS')

time.sleep(10)

try:
    YTBbutton = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="trust-browser-button"]'))
    )
    YTBbutton.click()
except:
    driver.quit()

try:
    nextButton = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="ui-icon-seek-next"]'))
    )
    print(nextButton.get_attribute('class'))
except:
    driver.quit()

actionButton = driver.find_element(By.XPATH, '//*[@id="onprem-grid"]/div[4]/div[3]/div/div[1]/div[8]/div')
actionButton.click()
time.sleep(0.5)

removeButton = driver.find_element(By.XPATH, '//*[@id="csw-slickgrid-dropdown"]/ul/li[2]/a')
removeButton.click()