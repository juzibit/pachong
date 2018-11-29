import requests
from bs4 import BeautifulSoup
import numpy as np
import re
import os
import pandas as pd

url = "https://rl.fx678.com/date/20171229.html"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0)' 'Gecko/20100101 Firefox/63.0'}

r = requests.get(url, headers=headers)
html = r.text.encode(r.encoding).decode()
soup = BeautifulSoup(html, "lxml")

table = soup.find('table', id='current_data')
# print(table)
height = len(table.findAll(lambda tag:tag.name == 'tr' and
                           len(tag.findAll('td')) >= 1))
# print(height)
# for row in table.findAll('tr'):
#    print(len(row.findAll('td')), end='\t')

columns = [x.text for x in table.tr.findAll('th')]
# print(columns)
columns =[x.replace('\xa0', '') for x in columns]
# print(columns)

width = len(columns)
df = pd.DataFrame(data = np.full((height,width), '', dtype='U'), columns=columns)
# print(df)
rows = [row for row in table.findAll('tr') if row.find('td')!=None]
# print(rows)

for i in range(len(rows)):
    cells = rows[i].findAll('td')
    if len(cells) == width:
        df.iloc[i] = [cell.text.replace(' ','').replace('\n','') for cell in cells]

        for j in range(len(cells)):
            if cells[j].has_attr('rowspan'):
                z = int(cells[j].attrs['rowspan'])
                df.iloc[i:i+z,j] = [cells[j].text.replace(' ','').replace('\n', '',)]*z
    else:
        w = len(cells)
        df.iloc[i,width-w:] = [cell.text.replace(' ','').replace('\n', '',) for cell in cells]

df.to_excel('test.xlsx')
 # print(df)

