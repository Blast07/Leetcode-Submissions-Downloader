from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from getpass import getpass
import time
import json

"""
	before running this script make sure you have installed selenium
	and placed the driver(chromedriver or geckodriver) in system path.
"""

USER_ID = ""
PASSWORD = ""

LOGIN_URL = "https://leetcode.com/accounts/login/"
PROBLEMS_URL = "https://leetcode.com/problemset/all/?status=Solved"
SUBMISSION_URL = "view-source:https://leetcode.com/api/submissions/"

#if your file type is not mentioned, then you can add yourself here in this dictionary
FILE_EXTENSION = {"cpp": "cpp", "java":"java", "python":"py", "py":"py"} 

DELAY = 10 #if your internet is slow then increase this value, else decrease; mostly 10 will work fine

#opts = Options()
#opts.set_headless()

class OpenBrowser:
	def __init__(self, flag):
		self.flag = flag 

	def __enter__(self):
		if self.flag == 1:

			opt = FirefoxOptions() 
			opt.set_headless()
			self.browser = Firefox(options = opt)
			return Firefox(options = opt)
		else:
			opt = ChromeOptions()
			opt.headless = True
			self.browser = Chrome(options = opt)
			return Chrome(options = opt)
			
			
	
	def __exit__(self):
		self.browser.close()


def getSubmissions(flag):
	#with Firefox(options = opts) as browser:
	print("Opening Browser")
	with OpenBrowser(flag) as browser:
		print("Opened Browser")
		browser.get(LOGIN_URL) 
		print("Opened Leetcode")
		
		time.sleep(DELAY)
		
		username_textbox = browser.find_element_by_id("id_login")
		password_textbox = browser.find_element_by_id("id_password")
		login_button = browser.find_element_by_id("signin_btn")
		
		username_textbox.send_keys(USER_ID)
		password_textbox.send_keys(PASSWORD)
		login_button.click();
	
		time.sleep(DELAY)
		print("logged in")
	
		browser.get(PROBLEMS_URL)
		time.sleep(DELAY)
		print("Getting all solved problems")
	
		xpath_all = "//select[@class='form-control']/option[text()='all']"
		browser.find_element_by_xpath(xpath_all).click()
		time.sleep(DELAY)
	
		xpath_problems = "//div[@class='table-responsive question-list-table']/table/tbody[1]/tr/td[3]/div/a"
		links = browser.find_elements_by_xpath(xpath_problems)
		problems = [link.get_attribute("data-slug") for link in links]
	
		print("Getting submissions:")
		for problem in problems:
	
			browser.get(SUBMISSION_URL + problem)	
			pre = browser.find_element_by_tag_name("pre").text
			time.sleep(3) #increase this value if you get error something like:"no element named pre found"
			data = json.loads(pre)
	
			for submission in data["submissions_dump"]:
				lang = submission["lang"]
	
				if submission["status_display"] == "Accepted":
					with open(f"{problem}.{FILE_EXTENSION[lang]}", 'w') as file1:
						file1.write(submission["code"])
						print(f"Done {problem}")
					break
	
	
	
	print(40*'#')
	print("Got all submissions")


if __name__ == "__main__":
	USER_ID = input("User id/email:").strip()
	PASSWORD = getpass() 
	flag = int(input("Enter 1 for firefox(geckodriver), 0 for chrome(chromedriver):").strip())
	getSubmissions(flag)
	




