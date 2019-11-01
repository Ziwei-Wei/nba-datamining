from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import math
import nba_schedule_scrapper as schedule

uuu = "https://www.basketball-reference.com/boxscores/201810160BOS.html"


def getTeams():
    url = "https://www.basketball-reference.com/teams/"
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    teamList = []
    for tr in soup.findAll('tr'):
        for th in tr.findAll('th'):
            target = th.find("a")
            if target:
                target = target.get("href")
                item = []
                item.append(th.find("a").getText())
                item.append(target.strip("/teams"))
                teamList.append(item)
    return pd.DataFrame(teamList, columns=["Name", "Abbr"])


def getTeamsDict():
    url = "https://www.basketball-reference.com/teams/"
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    teamList = []
    for tr in soup.findAll('tr'):
        for th in tr.findAll('th'):
            target = th.find("a")
            if target:
                target = target.get("href")
                item = []
                item.append(th.find("a").getText())
                item.append(target.strip("/teams"))
                teamList.append(item)
    teamDict = dict(teamList)
    return teamDict


def getHeader(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    soup.findAll('tr')
    header = []
    for th in soup.findAll('tr', limit=2)[1].findAll('th'):
        header.append(th.getText())
    return header


def getBoxscore(url, home, away):
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    homeDiv = soup.find('table', {
        "class": "sortable stats_table", "id": "box-{}-game-basic".format(home)})
    awayDiv = soup.find('table', {
        "class": "sortable stats_table", "id": "box-{}-game-basic".format(away)})
    homeRows = homeDiv.find("tbody").findAll("tr")
    awayRows = awayDiv.find("tbody").findAll("tr")
    homeStats = []
    awayStats = []

    for i in range(0, len(homeRows)):
        statsItem = []
        for th in homeRows[i].findAll('th'):
            statsItem.append(th.getText())
        for td in homeRows[i].findAll('td'):
            statsItem.append(td.getText())
        homeStats.append(statsItem)

    for i in range(0, len(awayRows)):
        statsItem = []
        for th in awayRows[i].findAll('th'):
            statsItem.append(th.getText())
        for td in awayRows[i].findAll('td'):
            statsItem.append(td.getText())
        awayStats.append(statsItem)

    homeStats = pd.DataFrame(homeStats)
    awayStats = pd.DataFrame(awayStats)
    return homeStats, awayStats


def save(data, format, path):
    if format == "csv":
        data.to_csv(path, index=None, header=True)


if __name__ == "__main__":
    print(getTeamsDict())
    header = getHeader(uuu)
    print(header)
    home, away = getBoxscore(uuu, "PHI", "BOS")
    print(home)
    print(away)
