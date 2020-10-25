import sys
import getpass
import datetime
import argparse
from terminaltables import AsciiTable
from selenium import webdriver

parser = argparse.ArgumentParser(description='Automatically fetch deadlines from LMS')
parser.add_argument('--browser', type=str, help='specify the browser i.e --browser=chrome')
parser.add_argument('--driver', type=str, help='specify name of the web driver i.e --driver-naem=chromedriver')

args = parser.parse_args()
BROWSER = None
DRIVER_PATH = None

if args.driver and args.browser:
    f = open(".config", "w")
    f.write(args.browser.lower() + "\n")
    f.write(args.driver.lower())
    f.close()
    BROWSER = args.browser.lower()
    DRIVER_PATH = args.driver.lower()

else:
    with open(".config") as f:
        content = f.readlines()
        DRIVER_PATH = content[1]
        BROWSER = content[0]


if BROWSER == "chrome":
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path="./" + DRIVER_PATH , options=options)

elif BROWSER == "firefox":
    from selenium.webdriver.firefox.options import Options

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=".\\" + DRIVER_PATH)

else:
    print("Incorrect or Unsupported browser specified")
    sys.exit(0)


if sys.stdin.isatty():
   print("Enter credentials")
   user = input("Username: ")
   pwd = getpass.getpass("Password: ")
else:
    print("Please make sure you are using a terminal")
    sys.exit(0)

courses = [['Course', 'Assignment', 'Due Date', 'Done']]
SUBMITTED = "My submission: Submitted for grading, Not graded"

driver.get("https://lms.nust.edu.pk/portal/")

# logging in to the lms
username = driver.find_element_by_xpath('//input[@id="login_username"]')
username.send_keys(user)

password = driver.find_element_by_xpath('//input[@id="login_password"]')
password.send_keys(pwd)

button = driver.find_element_by_xpath('//*[@id="login"]/div[4]/input')
button.click()

# Obtaining the course list
course_list = driver.find_elements_by_xpath('//div[@id="1"]/div[@id="course_list"]/div')

for course in course_list:
    course_name = course.text.split(' BSCS2k18',1)[0]
    course_divs = course.find_elements_by_tag_name("div")
    course_id = course.get_attribute('id')
    if len(course_divs) > 3:
        assignment_title = driver.find_elements_by_xpath('//div[@id="' + course_id + '"]//a[@title="Assignment"]')
        info = driver.find_elements_by_xpath('//div[@id="' + course_id + '"]//div[@class="info"]')
        details = driver.find_elements_by_xpath('//div[@id="' + course_id + '"]//div[@class="details"]')
        names = [i.get_attribute('text') for i in assignment_title]
        info = [i.get_attribute('innerHTML') for i in info]
        due_date = [i for i in info if "Due date" in i]
        details = [i.get_attribute('innerHTML') for i in details]
        
        for i in range(len(names)):
            current_course = []
            current_course += [course_name[6:]]
            name = names[i]
            current_course += [name[:17]]
            date = due_date[i]
            # Friday, 27 November 2020, 11:55 PM
            date = datetime.datetime.strptime(date[10:],"%A, %d %B %Y, %I:%M %p").strftime("%a, %d %b %y, %I:%M%p")
            current_course += [date]
            if details[i] == SUBMITTED:
                detail = u'\u2714'
            else:
                detail = u'\u2716'
            current_course += [detail] 
            courses += [current_course]

if courses == [['Course', 'Assignment', 'Due Date', 'Done']]:
    print("Invalid credentials")
    sys.exit(1)

table = AsciiTable(courses)
print(table.table)
