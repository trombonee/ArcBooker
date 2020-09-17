import time
from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions
from datetime import timedelta
from datetime import datetime
import tkinter

class ArcBooker():
	def __init__(self):
		url = "https://getactive.gogaelsgo.com/Program/GetProducts?classification=b2e9f15b-dbaa-4f55-8bb3-6c1ca1c00e32"
		options = webdriver.ChromeOptions()
		options.add_argument("--enable-javascript")
		options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		self.driver = webdriver.Chrome(chrome_options=options)

		self.driver.get(url)
		self.driver.execute_script("javascript:showLogin('/Program/GetProducts?classification=b2e9f15b-dbaa-4f55-8bb3-6c1ca1c00e32')")
		print(self.driver.current_url)
		time.sleep(1)
		self.driver.find_element_by_css_selector("button.loginOption.btn.btn-lg.btn-block.btn-social.btn-soundcloud").click()
		print(self.driver.current_url)
		time.sleep(2)

		username_box = self.driver.find_element_by_id("username")
		username_box.send_keys("") #Your Username

		password_box = self.driver.find_element_by_id("password")
		password_box.send_keys("") #Your password

		self.driver.find_element_by_xpath("//*[@id='qw-region-content-inner']/div/form/div[3]/button").click()
		time.sleep(1)
		print(self.driver.current_url)

		workoutZones = self.driver.find_elements_by_css_selector("h4.TitleText-SP")
		for zone in workoutZones:
			print(zone.text)
			if zone.text == "L2 Conditioning Zone - Dumbbell Free Weights": #Preferred workout zone
				print("Correct zone found")
				zone.click()
				break

		bookDate = str(datetime.date(datetime.now()+timedelta(days=3))) + " 08:30:00" #Preferred workout time

		print("Attempting to book on " + bookDate)

		time_slots = self.driver.find_elements_by_css_selector("button.btn.btn-primary.pull-left")
		print("There are " + str(len(time_slots)) + " timeslots")
		isFound = False
		for time_slot in time_slots:
			info = time_slot.get_attribute("onClick")
			splitInfo = info.split("'")
			checkIn = str(datetime.strptime(splitInfo[7], '%m/%d/%Y %I:%M:%S %p'))
			checkOut = str(datetime.strptime(splitInfo[9], '%m/%d/%Y %I:%M:%S %p'))
			print("From " + checkIn + " to " + checkOut)
			if checkIn == bookDate:
				print("Prefered time available, booking now")
				time_slot.click()
				time.sleep(1)
				self.driver.find_element_by_xpath("//*[@id='btnAccept']").click()
				self.driver.find_element_by_xpath("//*[@id='checkoutButton']")
				isFound = True
				break
		
		if not isFound:
			print("Time not found please try another")
			

if __name__ == "__main__":
	r = ArcBooker()