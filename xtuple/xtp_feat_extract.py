from bs4 import BeautifulSoup
import requests
import re
import sys

for fhtml in sys.argv:
    if fhtml != sys.argv[0] and fhtml != sys.argv[1]:
        print(fhtml)
        with open(fhtml) as f:
            soup = BeautifulSoup(f, "lxml")

        csv = ""
        date = ""
        restable = soup.find_all("tbody")
        tlinks = restable[0].find_all("a")

        for i in range(len(tlinks)):
            r = requests.get(tlinks[i]['href'])
            soup = BeautifulSoup(r.text, "lxml")
            tab_his = soup.find_all("tbody")
            tab_his = tab_his[len(tab_his)-1] #letze Tabelle der Seite
            date_new = re.search(r'\d\d/\d\d/\d\d', tab_his.contents[0].contents[0].text).group(0)
            date_new = date_new[0:2] + "-" + date_new[3:5] + "-" + date_new[6:9]
            for child in tab_his.children:
                status = re.search(r'(\d\d/\d\d/\d\d) (\d\d:\d\d) (.*Resolved|.*Fixed)', child.contents[0].text + " " + child.contents[3].text)
                if status is not None:
                    date = status.group(1)
                    csv = date[0:2] + "-" + date[3:5] + "-" + date[6:8]
                    print("{0},{1},{2}".format(tlinks[i].text, date_new, csv))
                    break

