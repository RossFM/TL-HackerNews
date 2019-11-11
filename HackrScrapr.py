from bs4 import BeautifulSoup
import requests
import re
import json
import argparse
import sys

# Collect required number of posts
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("--posts", help="Number of posts to display, between 1 & 100",
                        type=int)
    args = parser.parse_args()
    posts = args.posts

    if 1 <= posts <= 100:
        pages = int(posts / 30)+1 #Convert posts to pages to scrape
    else:
        sys.exit("Out of range. Please enter a number between 1 & 100")
except Exception as e:
    sys.exit('-h for help')

urlBase = 'https://news.ycombinator.com/news?p='

#URL validator, courtesy of Django
regex = re.compile(
    r'^(?:http|ftp)s?://' # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
    r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def scraper(numPages): #Main scraper function
    url = urlBase + str(numPages) #Generate correct url with page number
    if re.match(regex, url):
        print('Valid URL. Working...')
    else:
        sys.exit('URL error')
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")

    #BeautifulSoup find functions for sections
    fThing = content.find_all('tr', attrs={"class": "athing"})
    fSub = content.find_all('td', attrs={"class":"subtext"})
    fRank = content.find_all('td', attrs={"class":"title", "align":"right"})

    num = len(fThing)
    for i in range(num):
        #Scrape data from relevant sections
        try:
            title = fThing[i].find('a', attrs={"class": "storylink"}).text
        except Exception as e:
            title = 'No title'

        try:
            link = fThing[i].find('a', attrs={"class": "storylink"})['href']
        except Exception as e:
            link = 'No URL link'

        try:
            author = fSub[i].find('a', attrs={"class": "hnuser"}).text
        except Exception as e:
            author = 'No author'

        try:
            score = int(re.findall(r"\d+", fSub[i].find('span', attrs={"class": "score"}).text)[0])
        except Exception as e:
            score = 0

        try:
            comments = int(re.findall(r"\d+", fSub[i].select('a')[-1].text)[0])
        except Exception as e:
            comments = 0

        try:
            rank = int(re.findall(r"\d+", fRank[i].find('span', attrs={"class": "rank"}).text)[0])
        except Exception as e:
            rank = 0

        outPut = { #Formatting of list
        "title": title,
        "url": link,
        "author": author,
        "points": score,
        "comments": comments,
        "rank": rank,
        }
        if not title: title = 'No title' #Title is non empty string
        if len(title) > 256: title = title[:256] #Title is not more than 256 characters
        if not author: author = 'No Author' #Author is non empty string
        if len(author) > 256: author = author[:256] #Author is not more than 256 characters
        #Points, comments, rank are >= 0
        if score < 0: score = 0
        if comments < 0: comments = 0
        if rank < 0: rank = 0
        jsonContainer.append(outPut)


jsonContainer = []
for i in range(pages):  #run scraper enough times to iterate through pages
    scraper(i+1)
    i +=1

for i in range(len(jsonContainer)): #Trim resulting list down to requested number of posts
    if len(jsonContainer) > posts:
        jsonContainer.pop()

with open('HackerNews.json', 'w') as outfile: #Write jsonContainer to file in Json format
    json.dump(jsonContainer, outfile)

with open('HackerNews.json') as json_data: #Read file back through command line
    jsonData = json.load(json_data)
    print(json.dumps(jsonData, indent=4, sort_keys=False))
