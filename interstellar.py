from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import quote
from lxml import html
import re
import csv

url = 'https://ru.wikipedia.org/wiki/' + quote('Интерстеллар')
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
ref = list()
nameArr = list()
spansWithDate = list()
nameDate = list()


line = soup.find('table',{'class': 'wikitable sortable'}).find('tbody').find_all('tr')
for tr in line:
    tds = tr.find_all('td')
    for td in tds:
        a = td.find('a')
        if (a):
            nameArr.append(a['title'])
            ref.append('https://ru.wikipedia.org' + a['href'])
            
for a in ref:
    pageA = urlopen(a)
    soupA = BeautifulSoup(pageA, 'html.parser')
    spansWithDate.append(soupA.find('span', {'class': 'bday'}))
    
spansStrWithDate = str(spansWithDate)
dateArr = re.findall(r'\d{4}-\d{2}-\d{2}', spansStrWithDate)
for i, j in zip(nameArr, dateArr):
    nameDate.append([i, j])
    
print('Актеры, играющие команду астронавтов:')
for i in nameDate:
    print (i[0] + ': ' + i[1])


