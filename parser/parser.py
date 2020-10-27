import sys
import datetime
import requests
from lxml import html
from terminaltables import AsciiTable


def parse(user, pwd):
    courses = [['Course', 'Assignment', 'Due Date', 'Done']]
    url = 'https://lms.nust.edu.pk/portal/login/index.php'
    response = requests.post(url, data={'username': user,
                                           'password': pwd,
                                           'rememberusername': '0'})
    if "close" in response.headers['Connection']:
        print("Invalid Credentials")
        sys.exit(0)

    html_source = response.text
    tree = html.fromstring(html=html_source)
    course_list = tree.xpath('//div[@id="1"]/div[@id="course_list"]/div')
    
    for course in course_list:
        course_name = course.xpath('//div[@id="' + course.get('id') +'"]/div[@class="course_title"]/h2/a/text()')[0].split(' BSCS2k18',1)[0]
        assignments_list = course.xpath('//div[@id="' + course.get('id') +'"]/div[@class="activity_info"]//div[@class="name"]/a/text()')
        due_dates = course.xpath('//div[@id="' + course.get('id') +'"]/div[@class="activity_info"]//div[@class="info"]/text()')
        status = course.xpath('//div[@id="' + course.get('id') +'"]/div[@class="activity_info"]//div[@class="details"]/text()')
        due_dates = [str(i) for i in due_dates if "Due date:" in str(i)]

        for i in range(len(assignments_list)):
            current_course = []
            current_course += [str(course_name[6:])]
            assignment_name = str(assignments_list[i])
            current_course += [assignment_name[0:17]]
            date = due_dates[i]
            current_course += [datetime.datetime.strptime(date[10:],"%A, %d %B %Y, %I:%M %p").strftime("%a, %d %b %y, %I:%M%p")]
            
            if str(status[i]) == "My submission: Submitted for grading, Not graded":
                detail = u'\u2714'
            else:
                detail = u'\u2716'
            
            current_course += [detail]
            courses += [current_course]

    table = AsciiTable(courses)
    print(table.table)
