import requests
from bs4 import BeautifulSoup
import pprint
import re
import csv

with open("bugs_idempiere.html", "r") as f:
    soup = BeautifulSoup(f, "html5lib")

# returns ResultSet, no \n
issues = soup.find_all("tr", class_="issuerow")

#regex for date
regexdate = re.compile(r"(\d\d/.{3}/\d\d).+")

f = open("bugsresults.csv", "w", newline="")
writer = csv.writer(f)

for issuerow in issues:
    rowd = []

    #issuekey
    rowd.append(issuerow.contents[3].text.strip("\n "))
    #issuetype
    rowd.append(issuerow.contents[7].text.strip("\n "))
    #status
    rowd.append(issuerow.contents[9].text.strip("\n "))
    #resolution
    rowd.append(issuerow.contents[13].text.strip("\n "))
    #created
    rowd.append(regexdate.match(issuerow.contents[21].text.strip("\n ")).group(1))
    #resolutiondate
    rowd.append(regexdate.match(issuerow.contents[27].text.strip("\n ")).group(1))
    writer.writerow(rowd)

f.close()
