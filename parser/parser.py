import re
import sys
import datetime
import requests
from lxml import html
from terminaltables import AsciiTable


def parse(user, pwd):
    courses = [['Course', 'Assignment', 'Due Date', 'Done']]
    login_url = 'https://lms.nust.edu.pk/portal/login/index.php?login'

    s = requests.Session()
    

    response = s.get(login_url)
    # cookie = response.cookies.get_dict()
    pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern, response.text)
    token = re.findall("\w{32}", token[0])

    payload = {'username': user, 'password': pwd, 'anchor': '', 'logintoken': token[0]}

    response = s.post(login_url, data=payload)

    html_source = response.text
    tree = html.fromstring(html=html_source)
    if 'Log in to the site' in str(tree.xpath('//head/title/text()')):
        print("Invalid Credentials")
        sys.exit(0)


    upcoming_url = 'https://lms.nust.edu.pk/portal/calendar/view.php?view=upcoming'
    response = s.get(upcoming_url)
    html_source = response.text
    tree = html.fromstring(html=html_source)
    href_links = tree.xpath('//a[@class="card-link"]')
    href_links = [i.get('href') for i in href_links]
    
    print('Fetching data, please wait...\n')
    
    for link in href_links:
        course_description = []
        response = s.get(link)
        html_source = response.text
        tree = html.fromstring(html=html_source)
        course_name = str(tree.xpath('//div[@class="page-header-headings"]/h1/text()'))
        assignment_title = tree.xpath('//div[@role="main"]/h2/text()')
        table_information = tree.xpath('//table[@class="generaltable"]//td/text()')

        if 'This is attempt' in table_information[0]:
            submission_status = table_information[1]
            due_date = table_information[3]
        else:
            submission_status = table_information[0]
            due_date = table_information[2]

        course_description += [course_name[8:-13]]
        course_description += [assignment_title[0][0:17]]
        course_description += [datetime.datetime.strptime(due_date,"%A, %d %B %Y, %I:%M %p").strftime("%a, %d %b %y, %I:%M%p")]
        
        if str(submission_status) == 'Submitted for grading':
            submission_status = u'\u2714'
        else:
            submission_status = u'\u2716'

        course_description += [submission_status]
        courses += [course_description]

    table = AsciiTable(courses)
    print(table.table)
