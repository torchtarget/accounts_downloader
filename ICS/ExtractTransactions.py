##! /usr/bin/python3
from bs4 import BeautifulSoup

with open('/tmp/test.html') as fp:
    soup = BeautifulSoup(fp, "html.parser")
print(soup.title)

data = []
table = soup.find('table', attrs={'class': 'expander-table'})
rows = table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele.replace(',', '') for ele in cols])
with open("/tmp/test6.csv", "w") as output_file:
    for dataline in data:
        output_file.write("%s" % dataline)
print (data[23])
