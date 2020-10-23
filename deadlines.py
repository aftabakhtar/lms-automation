from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Chrome('./chromedriver')
driver.get("https://www.python.org/")
driver.quit()