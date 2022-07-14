import requests
from bs4 import BeautifulSoup
import re
import sys

STARTDATE = sys.argv[1]
ENDDATE = sys.argv[2]
ops = []
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

#The following function will fill the ops list with the postnumber of all ops than have the specified subject and were created on the specified month/year
def getThreads(subject, start, end):
    i = 0
    while True:
        i+=1
        URL = "https://archive.alice.al/vt/search/subject/" + subject + "/start/" + start +"/end/" + end + "/page/" + str(i)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.findAll(title="Reply to this post")
        if len(results) == 0:
            break
        for element in results:
            ops.append(element.text)

def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, ' ', raw_html)
  cleanertext = ''.join(i for i in cleantext if not i.isdigit())
  cleanertext = cleanertext.replace("'"," ")
  cleanertext = cleanertext.lower()
  return cleanertext

def extractText(threadNumber):
    URL = 'https://archive.alice.al/vt/thread/' + threadNumber
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.findAll("div", {"class": "text"})
    with open(STARTDATE + '-' + ENDDATE + '.txt', 'a') as file:
        for element in results:
            try:
                file.write(cleanhtml(element.decode_contents()))
                file.write('\n')
            except:
                print('Passu')
                pass
getThreads('wactor', STARTDATE, ENDDATE)
getThreads('sopa', STARTDATE, ENDDATE)
getThreads('ワクター', STARTDATE, ENDDATE)

ops = list(dict.fromkeys(ops))

x = 1
for thread in ops:
    print('Downloading thread #' + str(x) + ' of ' + str(len(ops)))
    extractText(thread)
    x += 1


