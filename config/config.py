from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def get_driver(OPERATING_SYSTEM, BROWSER_NAME):
    operating_system = OPERATING_SYSTEM
    browser_name = BROWSER_NAME
    driver_path = ''

    chrome_options = webdriver.ChromeOptions()

    if 'CHROME' in browser_name:
        driver_path += 'chromedriver'
    else:
        driver_path += 'geckodriver'

    if 'LINUX' in operating_system:
        driver_path = './' + driver_path
    else:
        driver_path = '.\\' + driver_path + '.exe'

    if 'CHROME' in browser_name and 'LINUX' in operating_system:
        chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-dev-shm-using")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        
    

    if 'chromedriver' in driver_path:
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    else:
        firefox_options = Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(executable_path=driver_path, options=firefox_options)

    return driver
