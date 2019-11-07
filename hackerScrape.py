from bs4 import BeautifulSoup
import requests
import re

url = 'https://news.ycombinator.com/'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
for posts in content.findAll('table', attrs={"class": "itemlist"}):
    outPut = {
    "title": posts.find('a', attrs={"class": "storylink"}).text,
    "url": posts.find('a', attrs={"class": "storylink"})['href'],
    "author": posts.find('a', attrs={"class": "hnuser"}).text,
    "score": re.findall(r"\d+", posts.find('span', attrs={"class": "score"}).text),
    "comments": posts.find('a', string=re.compile("comments")).text,
    "Rank": re.findall(r"\d+", posts.find('span', attrs={"class": "rank"}).text),
    }

print (outPut)
