#-*-coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import quote
from lxml import html
import re
import csv
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return connection

def create_table(connect, create_table_sql):
    try:
        c = connect.cursor()
        c.execute('PRAGMA encoding="UTF-8";')
        c.execute(create_table_sql)
    except Error as e:
        print(e)

sql_create_table = """ CREATE TABLE IF NOT EXISTS bdate (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        bday text NOT NULL,
                                        UNIQUE ("name") ON CONFLICT IGNORE
                                    ); """


def create_bday_elem(connection, elem):
    sql = ''' INSERT INTO bdate(name,bday)
                VALUES(?,?) '''
    cur = connection.cursor()
    cur.execute(sql, elem)
    return cur.lastrowid

db = "pythonsqlite.db"
connect = create_connection(db)
if connect:
    create_table(connect, sql_create_table)
else:
    print("Error! cannot create the database connection.")
    
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

for i in nameDate:
    if connect:
        create_bday_elem(connect, i)

if connect:
    connect.commit()
    connect.close()

