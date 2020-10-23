import sys
import getpass
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


if sys.stdin.isatty():
   print("Enter credentials")
   user = input("Username: ")
   pwd = getpass.getpass("Password: ")
else:
    print("Please make sure you are using a terminal")
    sys.exit(0)


driver = webdriver.Chrome('./chromedriver')
driver.get("https://lms.nust.edu.pk/portal/")

username = driver.find_element_by_xpath('//input[@id="login_username"]')
username.send_keys(user)

password = driver.find_element_by_xpath('//input[@id="login_password"]')
password.send_keys(pwd)

button = driver.find_element_by_xpath('//*[@id="login"]/div[4]/input')
button.click()
