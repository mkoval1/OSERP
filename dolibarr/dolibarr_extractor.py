#!/usr/bin/env python
import requests
import json
import re
import csv
from pprint import pprint
import time


par = {"state":"closed"}
start_url = "https://api.github.com/repositories/1957456/issues?state=closed&page=1&per_page=100"
re_next = re.compile(r'(<.+){0,1}<(https://.*)>; rel="next"')
re_last = re.compile(r'(<.+){0,1}<(https://.*)>; rel="last"')
re_page = re.compile(r"\&page=\d{1,3}")

def requesturl(url):
    print("Requesting: ", url)
    r = requests.get(url, params=par)
    if "200" not in r.headers["Status"]:
        print("------------ RESPONSE: ", r.headers["Status"], "--------------")
        print("###############", time.asctime(time.localtime()), "###############")
        exit()

    return r


def extract(r):
    jlist = json.loads(r.text)
    csvrow = []
    for entry in jlist:
        csvrow.append([entry["number"], getlabel(entry["labels"]), entry["state"], entry["created_at"], entry["closed_at"]])

    return csvrow


def writetofile(csvlist):
    with open("results.csv", "a") as f:
        fwriter = csv.writer(f, delimiter=",")
        fwriter.writerows(csvlist)

    print("Writing to file... Done.")


def getlabel(labels):
    try:
        name = labels[0]["name"]
        return name
    except IndexError:
        return "[]"


def main():
    cnt = 1
    csvlist = []
    print("###############", time.asctime(time.localtime()), "###############")
    r = requesturl(start_url)
    lastu = re.search(re_last, r.headers["Link"]).group(2)
    print("Last URL: ", lastu)
    while re.search(re_next, r.headers["Link"]).group(2) != lastu:
        if r.text != "[]":
            print("Appending data for page: ", cnt)
            csvlist = csvlist + extract(r)
            r = requesturl(re.search(re_next, r.headers["Link"]).group(2))
            writetofile(csvlist)
            maxpage = str(re.search(re_page, lastu))
            remaining = str(int(maxpage) - cnt)
            est = str(int(remaining) * 120 / 60)
            print("Waiting... %s out of %s remaining. %s minutes until done", % (remaining, maxpage, est))

        else:
            print("EMPTY RESPONSE, ABORTING")
            print("###############", time.asctime(time.localtime()), "###############")
            exit()

        cnt+= 1
        time.sleep(120)


main()
