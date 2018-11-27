from bs4 import BeautifulSoup
import requests
import re

for i in range(8):
    url ="https://sourceforge.net/p/compiere/bugs/search/?q=status%3Aclosed-fixed+or+status%3Aclosed-works-for-me&limit=250&page=" + str(i)

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html5lib")
    results = soup.find("tbody")

#print("id: " + results.contents[1].contents[1].contents[0].text)
#print("created: " + re.search(r"\d\d\d\d-\d\d-\d\d", results.contents[1].contents[11].contents[1].text).group(0))
#print("created: " + re.search(r"\d\d\d\d-\d\d-\d\d", results.contents[1].contents[13].contents[1].text).group(0))

    for i in range(1,len(results.contents),2):
        print(results.contents[i].contents[1].contents[0].text + ";" +
re.search(r"\d\d\d\d-\d\d-\d\d", results.contents[i].contents[11].contents[1].text).group(0) + ";" +
re.search(r"\d\d\d\d-\d\d-\d\d", results.contents[i].contents[13].contents[1].text).group(0))
