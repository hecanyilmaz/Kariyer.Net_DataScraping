from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
import sys
import os

#Website: kariyer.net

#It's a website where emloyeers find employees. Employeers can give 
#job advertisements. Employees can seek for jobs. In this script,
#you can get a list of jobs by giving the filtered job search url.
#To start the code you can follow the given command.

#python <script_name>.py "<url>"

#Libraries:
#bs4, requests, datetime
#pytz, sys, os

#Constants:
WEBSITE = 'https://www.kariyer.net'
CUR_PATH = os.path.dirname(__file__)
GIVEN_URL = sys.argv[1]

def getTime(time_zone = "Europe/Istanbul"):
    tz = pytz.timezone(time_zone)
    cur_time = datetime.now(tz)
    time = cur_time.strftime("%d-%m-%Y %I %M %p")
    return time

def toPrettyStr(s):
    return s.replace('\n', '').strip(' ')

def findJobs():
    html_text = requests.get(GIVEN_URL).content
    
    soup = BeautifulSoup(html_text, 'lxml')

    try:
        os.mkdir(os.path.join(CUR_PATH, 'Logs'))
    except(FileExistsError):
        #Folder opening called 'Logs'
        pass

    new_path = os.path.join(CUR_PATH, f'Logs\\log_{getTime()}.txt')
    jobs = soup.find_all('a', class_ = 'k-ad-card')

    with open(new_path, 'w', encoding='utf-8') as f:
        for index, job in enumerate(jobs):
            post_time = job.find('span', class_= 'date')
            if post_time  != None:
                
                post_time = toPrettyStr(post_time.text)
                title = toPrettyStr(job.find('div', class_= 'subtitle').text)
                location = toPrettyStr(job.find('span', class_= 'location').text)
                work_model = toPrettyStr(job.find('span', class_= 'work-model').text)
                more_info = WEBSITE + job['href']

                f.write(f"Company Name: {title} \n")
                f.write(f"Location: {location} \n")
                f.write(f"Work Model: {work_model} \n")
                f.write(f"Post Time: {post_time} \n") 
                f.write(f"More Info: {more_info} \n")
                f.write('\n')

    print("File created and saved successfully!")
    f.close()

if __name__ == '__main__':
    findJobs()