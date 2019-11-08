from bs4 import BeautifulSoup
import requests
import re
import json
import argparse
import sys

# Collect required number of posts
parser = argparse.ArgumentParser()
parser.add_argument("posts", help="Number of posts to display, between 1 & 100",
                    type=int)
args = parser.parse_args()
posts = args.posts
if 1 <= posts <= 100:
    pages = int(posts / 30)+1 #Convert posts to pages to scrape
else:
    sys.exit("Out of range. Please enter a number between 1 & 100")

urlBase = 'https://news.ycombinator.com/news?p='

def scraper(numPages):
    url = urlBase + str(numPages)
    print(url)
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    fThing = content.find_all('tr', attrs={"class": "athing"})
    fSub = content.find_all('td', attrs={"class":"subtext"})
    fRank = content.find_all('td', attrs={"class":"title", "align":"right"})
    num = len(fThing)
    for i in range(num):
        title = fThing[i].find('a', attrs={"class": "storylink"}).text
        try:
            author = fSub[i].find('a', attrs={"class": "hnuser"}).text
        except Exception as e:
            author = 'No author'
        try:
            score = int(re.findall(r"\d+", fSub[idx].find('span', attrs={"class": "score"}).text)[0])
        except Exception as e:
            score = 0
        outPut = {
        "title": title,
        "url": fThing[i].find('a', attrs={"class": "storylink"})['href'],
        "author": author,
        "score": score,
        "rank": int(re.findall(r"\d+", fRank[i].find('span', attrs={"class": "rank"}).text)[0]),
        }
        if not title: title = 'No title' #Title is non empty string
        if len(title) > 256: title = title[:256] #Title is not more than 256 characters
        if not author: author = 'No Author' #Title is non empty string
        if len(author) > 256: author = author[:256] #Title is not more than 256 characters
        jsonContainer.append(outPut)


jsonContainer = []
for i in range(pages):  #run scraper enough times to iterate through pages
    scraper(i+1)
    i +=1

print(posts)

for i in range(posts): #Trim resulting list down to requested number of posts
    if len(jsonContainer) > posts:
        jsonContainer.pop()
        print(i)


with open('HackerNews.json', 'w') as outfile:
    json.dump(jsonContainer, outfile)

with open('HackerNews.json') as json_data:
    jsonData = json.load(json_data)
    print(json.dumps(jsonData, indent=4, sort_keys=True))
