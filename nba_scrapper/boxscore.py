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


def recordBoxscore(year, month, path="../data/boxscore"):
    schedule_table = schedule.getSchedule(year, month)
    schedule_header = schedule.getHeader(year)
    schedule_table.columns = schedule_header
    for _, row in schedule_table.iterrows():
        if row["Date"] == "Playoffs":
            return False
        dateTokens = row["Date"].replace(
            ' ', '_').replace(',', '').split("_")
        date = dateTokens[3] + "_" + \
            dateDict[dateTokens[1]] + "_" + dateTokens[2]
        home = teamDict[row["Home/Neutral"]]
        away = teamDict[row["Visitor/Neutral"]]
        url = row["box_score_text"]
        print("Process " + home + " vs " + away)
        boxscore_home, boxscore_away = getBoxscoreByUrl(url, home, away)
        print("Processed " + home + " vs " + away)
        if not os.path.exists(path):
            os.mkdir(path)
        save(boxscore_home, "csv", path +
             "/boxscore_{}_{}_{}_home.csv".format(date, home, away))
        save(boxscore_away, "csv", path +
             "/boxscore_{}_{}_{}_away.csv".format(date, home, away))
        print("Saved " + home + " vs " + away)


def recordBoxscoreByYear(year):
    monthList = ["october", "november", "december", "january",
                 "february", "march", "april", "may", "june"]
    for month in monthList:
        print("Process Year {} Month {}".format(year, month))
        if recordBoxscore(year, month, "../data/boxscore/{}".format(year)) == False:
            return


def recordBetween(startYear, endYear, format="csv"):
    for year in range(startYear, endYear):
        recordBoxscoreByYear(year)
    return


def save(data, format, path):
    if format == "csv":
        data.to_csv(path, index=None, header=True)


if __name__ == "__main__":
    recordBetween(2016, 2019)
