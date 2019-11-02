from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import math
import schedule
import os

teamDict = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BRK',
    'Charlotte Hornets': 'CHO',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHO',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}

dateDict = {
    "Oct": "10",
    "Nov": "11",
    "Dec": "12",
    "Jan": "1",
    "Feb": "2",
    "Mar": "3",
    "Apr": "4",
    "May": "5",
    "Jun": "6"
}


def getTeams():
    url = "https://www.basketball-reference.com/teams/"
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    active = soup.find("table", {"id": "teams_active"})
    teamList = []
    for tr in active.findAll('tr', {"class": "full_table"}):
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
    active = soup.find("table", {"id": "teams_active"})
    teamList = []
    for tr in active.findAll('tr', {"class": "full_table"}):
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
        if th.getText() == "Starters":
            header.append("Players")
        else:
            header.append(th.getText())
    return header


def getBoxscoreByUrl(url, home, away):
    try:
        header = getHeader(url)
        html = urlopen(url)
    except:
        print("URL does not exist! In getBoxscoreByUrl")
    else:
        soup = BeautifulSoup(html, features="html5lib")
        homeDiv = soup.find('table', {"id": "box-{}-game-basic".format(home)})
        awayDiv = soup.find('table', {"id": "box-{}-game-basic".format(away)})
        homeRows = homeDiv.find("tbody").findAll("tr")
        awayRows = awayDiv.find("tbody").findAll("tr")
        homeStats = []
        awayStats = []

        for i in range(0, len(homeRows)):
            if homeRows[i].get("class"):
                continue
            statsItem = []
            for th in homeRows[i].findAll('th'):
                statsItem.append(th.getText())
            for td in homeRows[i].findAll('td'):
                statsItem.append(td.getText())
            if statsItem[0] != "Reserves" and statsItem[1] != "Did Not Play" and statsItem[1] != "Did Not Dress":
                homeStats.append(statsItem)

        for i in range(0, len(awayRows)):
            if awayRows[i].get("class"):
                continue
            statsItem = []
            for th in awayRows[i].findAll('th'):
                statsItem.append(th.getText())
            for td in awayRows[i].findAll('td'):
                statsItem.append(td.getText())
            if statsItem[0] != "Reserves" and statsItem[1] != "Did Not Play" and statsItem[1] != "Did Not Dress":
                awayStats.append(statsItem)

        homeStats = pd.DataFrame(homeStats, columns=header)
        awayStats = pd.DataFrame(awayStats, columns=header)
        return homeStats, awayStats


def getBoxscore(year, month, saveToDisk=False, path="../data/boxscore"):
    schedule_table = schedule.getSchedule(year, month)
    schedule_header = schedule.getHeader(year)
    schedule_table.columns = schedule_header
    boxscore_list = []
    for _, row in schedule_table.iterrows():
        dateTokens = row["Date"].replace(
            ' ', '_').replace(',', '').split("_")
        date = dateTokens[3] + "_" + \
            dateDict[dateTokens[1]] + "_" + dateTokens[2]
        home = teamDict[row["Home/Neutral"]]
        away = teamDict[row["Visitor/Neutral"]]
        url = row["box_score_text"]
        print(home + " vs " + away)
        boxscore_home, boxscore_away = getBoxscoreByUrl(url, home, away)
        print(boxscore_home)
        print(boxscore_away)
        if saveToDisk == True:
            if not os.path.exists(path):
                os.mkdir(path)
            save(boxscore_home, "csv", path +
                 "/boxscore_{}_{}_{}_home.csv".format(date, home, away))
            save(boxscore_away, "csv", path +
                 "/boxscore_{}_{}_{}_away.csv".format(date, home, away))
        boxscore = [boxscore_home, boxscore_away]
        boxscore_list.append(boxscore)
    return boxscore_list


def getBoxscoreByYear(year, saveToDisk=False, path="../data/boxscore"):
    monthList = ["october", "november", "december", "january",
                 "february", "march", "april", "may", "june"]
    yearlyBoxscores = []
    for month in monthList:
        yearlyBoxscores.extend(getBoxscore(year, month, saveToDisk, path))
    if saveToDisk == False:
        return yearlyBoxscores


def recordBetween(startYear, endYear, format="csv"):
    for year in range(startYear, endYear):
        getBoxscoreByYear(year, True)


def save(data, format, path):
    if format == "csv":
        data.to_csv(path, index=None, header=True)


if __name__ == "__main__":
    recordBetween(2015, 2020)
