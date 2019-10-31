from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def getScheduleHeader(year):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_games.html".format(
        year)
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    soup.findAll('tr', limit=2)
    header = []
    for th in soup.findAll('tr', limit=2)[0].findAll('th'):
        t = th.getText()
        if t == "PTS":
            t = th.get("aria-label")
        header.append(t)
    return header


def getSchedule(year, month):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(
        year, month)
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    rows = soup.findAll('tr')
    schedule = []
    for i in range(1, len(rows)):
        scheduleItem = []
        for th in rows[i].findAll('th'):
            scheduleItem.append(th.getText())
        for td in rows[i].findAll('td'):
            scheduleItem.append(td.getText())
        schedule.append(scheduleItem)
    return pd.DataFrame(schedule)


def getYearlySchedule(year):
    monthList = ["october", "november", "december", "january",
                 "february", "march", "april", "may", "june"]
    header = getScheduleHeader(year)
    monthlySchedule = []
    for month in monthList:
        monthlySchedule.append(getSchedule(year, month))
    schedule = pd.concat(monthlySchedule, ignore_index=True)
    schedule.columns = header
    schedule.drop(["Start (ET)", "\xa0", "Attend.",
                   "Notes"], inplace=True, axis=1)
    return schedule


def reorganize(schedule):
    schedule["Home Points"] = pd.to_numeric(schedule["Home Points"])
    schedule["Visitor Points"] = pd.to_numeric(schedule["Visitor Points"])
    diff = schedule["Home Points"] - schedule["Visitor Points"]
    schedule.drop(["Home Points", "Visitor Points"], inplace=True, axis=1)
    columnsTitles = ["Date", "Home/Neutral", "Visitor/Neutral"]
    schedule = schedule.reindex(columns=columnsTitles)
    schedule["Diifference"] = diff
    return schedule


def save(data, format, path):
    if format == "csv":
        data.to_csv(path, index=None, header=True)


def recordBetween(startYear, endYear, format="csv"):
    for year in range(startYear, endYear):
        print("Processing year %d" % year)
        schedule = reorganize(getYearlySchedule(year))
        path = "./nbaSchedule{}.csv".format(year)
        save(schedule, format, path)


if __name__ == "__main__":
    recordBetween(2015, 2020)
