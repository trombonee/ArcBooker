import time
from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from datetime import timedelta
from datetime import datetime
import os
import requests

def checkUrl(drivers):
    allGood = True
    currUrl = driverList[0].current_url
    for driver in driverList:
        if driver.current_url != currUrl:
            allGood = False
    return allGood

users = ['Luca', 'Anthony', 'Jarrett', 'Brian']
url = 'https://getactive.gogaelsgo.com/Program/GetProgramDetails?courseId=bacb7416-d62f-4792-a18d-2256faf00375&semesterId=6e595780-a1ad-40a0-9c3f-92d8e303bcd3'

options = webdriver.ChromeOptions()
options.add_argument("--enable-javascript")
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driverList = []
for user in users:
    driverList.append(webdriver.Chrome(options=options))

for driver in driverList:
    driver.get(url)
time.sleep(0.5)

for driver in driverList:
    driver.find_element_by_xpath("//*[@id='gdpr-cookie-accept']").click()
    driver.execute_script("javascript:showLogin('/Program/GetProducts?classification=b2e9f15b-dbaa-4f55-8bb3-6c1ca1c00e32')")
if checkUrl(driverList):
    print(driverList[0].current_url)
else:
    print('error')
time.sleep(0.5)
for driver in driverList:
    driver.find_element_by_css_selector("button.loginOption.btn.btn-lg.btn-block.btn-social.btn-soundcloud").click()
time.sleep(0.5)
if checkUrl(driverList):
    print('login page')
else:
    print('error at login page')


i = 0
for driver in driverList:
    user = users[i]
    try:
        with open(user + '.txt', 'r') as f:
            username, password = [line.rstrip() for line in f]
    except:
        print('trouble getting username/password')

    username_box = driver.find_element_by_id("username")
    username_box.send_keys(username) #Your Username

    password_box = driver.find_element_by_id("password")
    password_box.send_keys(password) #Your password
    driver.find_element_by_xpath("//*[@id='qw-region-content-inner']/div/form/div[3]/button").click()
    i+=1

time.sleep(0.5)
if checkUrl(driverList):
    print('all logged in')
else:
    print('error logging in')

for driver in driverList:
    driver.get(url)

bookDate = str(datetime.date(datetime.now()+timedelta(days=3))) + " 07:30:00" #Preferred workout time

i = 0
for driver in driverList:
    time_slots = driver.find_elements_by_css_selector("button.btn.btn-primary")
    isFound = False
    for time_slot in time_slots:
        info = time_slot.get_attribute("onClick")
        splitInfo = info.split("'")
        try:
            checkIn = str(datetime.strptime(splitInfo[7], '%m/%d/%Y %I:%M:%S %p'))
        except:
            continue
        if checkIn == bookDate:
            time_slot.click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='btnAccept']").click()
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='checkoutButton']").click()
            time.sleep(1)
            driver.find_elements_by_css_selector("button.card-item-2-large")[1].click()
            isFound = True
            break
    if not isFound:
        print('couldnt find time for ' + users[i])
    i+= 1
if checkUrl(driverList):
    print('same result')
else:
    print('error')







