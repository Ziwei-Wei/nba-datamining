from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import math


def getHeader(year, type="totals"):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(
        year, type)
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html5lib")
    soup.findAll('tr', limit=2)
    header = []
    for th in soup.findAll('tr', limit=2)[0].findAll('th'):
        header.append(th.getText())
        if th.getText() == "Player":
            header.append("Height")
            header.append("Weight")
    return header


def getStats(year, num=math.inf, type="totals"):
    url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(
        year, type)
    try:
        html = urlopen(url)
    except:
        print("URL does not exist!")
    else:
        soup = BeautifulSoup(html, features="html5lib")
        rows = soup.findAll('tr')
        stats = []
        if num >= len(rows):
            num = len(rows)
        for i in range(1, num):
            statsItem = []
            for th in rows[i].findAll('th'):
                statsItem.append(th.getText())
            for td in rows[i].findAll('td'):
                statsItem.append(td.getText())
                if td.get("data-stat") == "player":
                    playerUrl = td.find("a").get('href')
                    height = ""
                    weight = ""
                    if playerUrl:
                        playerHtml = urlopen(
                            "https://www.basketball-reference.com" + playerUrl)
                        playerSoup = BeautifulSoup(
                            playerHtml, features="html5lib")
                        height = playerSoup.find(
                            "span", itemprop="height").text
                        weight = playerSoup.find(
                            "span", itemprop="weight").text
                    statsItem.append(height)
                    statsItem.append(weight)

            stats.append(statsItem)
        res = pd.DataFrame(stats)
        res = res[res[1] != "Player"]
        return res


def getYearlyStat(year, num=math.inf, type="totals"):
    header = getHeader(year, type)
    stats = getStats(year, num, type)
    stats.columns = header
    return stats


def reorganize(stats):
    stats.drop(["Rk", "G", "GS", "FG", "FGA", "FG%", "2P%", "3P%", "FT%", "eFG%",
                "TRB"], inplace=True, axis=1)
    numeric = ["MP", "3P", "3PA", "2P", "2PA", "FT", "FTA",
               "ORB", "DRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    for tag in numeric:
        stats[tag] = pd.to_numeric(stats[tag])
    numericStats = stats.groupby(['Player'], as_index=False)["MP", "3P", "3PA", "2P", "2PA",
                                                             "FT", "FTA", "ORB", "DRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"].sum().drop("Player", 1)
    res = pd.concat([stats["Player"], stats["Pos"],
                     stats["Height"], stats["Weight"], numericStats], axis=1)
    return res


def save(data, format, path):
    if format == "csv":
        data.to_csv(path, index=None, header=True)


def recordBetween(startYear, endYear, format="csv"):
    for year in range(startYear, endYear):
        print("Processing year %d" % year)
        stats = reorganize(getYearlyStat(year))
        path = "./nba_player_stats_{}.csv".format(year)
        save(stats, format, path)


if __name__ == "__main__":
    header = getHeader(2019)
    print(header)
    stats = getYearlyStat(2019, 10)
    print(stats.head(10))
    stats = reorganize(stats)
    print(stats.head(10))
