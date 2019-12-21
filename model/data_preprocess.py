import pandas as pd
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

## save true abstract game


def save_abstract_game(schedules, boxscores, path="./training_date.csv"):
    abstract_games = {}
    for k, v in schedules.items():
        for i, row in v.iterrows():
            if row["Date"] == "Playoffs":
                continue
            tt = row["Date"].split(", ")
            dt = tt[1].split(" ")
            date = tt[2]+"_"+dateDict[dt[0]]+"_"+dt[1]
            if date in boxscores:
                home = teamDict[row["Home/Neutral"]]
                away = teamDict[row["Visitor/Neutral"]]
                matchup = home+"_"+away
                diff = row["Diifference"]
                abstract_game = {}
                home_data = boxscores[date][matchup]["home"]
                away_data = boxscores[date][matchup]["away"]
                for k1, row in home_data.iterrows():
                    for k2, v in row.items():
                        key = "home_"+k1+"_"+k2
                        abstract_game[key] = v
                for k1, row in away_data.iterrows():
                    for k2, v in row.items():
                        key = "away_"+k1+"_"+k2
                        abstract_game[key] = v
                abstract_game["diff"] = diff
                abstract_games[date+"_"+matchup] = abstract_game
    train_data = pd.DataFrame(abstract_games).transpose()
    train_data.to_csv(path)

if __name__ == "__main__":
    ## true abstract team on each game
    schedules = {}
    boxscores = {}
    players = {}

    for year in range(2015, 2020):
        print(year)
        schedules_data = pd.read_csv(
            "../data/schedule/schedule_{}.csv".format(year))
        players_data = pd.read_csv(
            "../data/player/nba_player_stats_{}.csv".format(year)).set_index('Player')
        schedules[year] = schedules_data
        players[year] = players_data.to_dict('dict')
        print(players_data)

        for filename in os.listdir('../data/boxscore/{}'.format(year)):
            tokens = filename.split("_")
            date = tokens[1]+"_"+tokens[2]+"_"+tokens[3]
            matchup = tokens[4]+"_"+tokens[5]
            team_type = tokens[6].split(".")[0]
            if date not in boxscores:
                boxscores[date] = {}

            if matchup not in boxscores[date]:
                boxscores[date][matchup] = {}

            if team_type not in boxscores[date][matchup]:
                boxscore_data = pd.read_csv(
                    '../data/boxscore/{}/{}'.format(year, filename)).drop(["FG%", "3P%", "FT%"], axis=1)
                for i, row in boxscore_data.iterrows():
                    if row['Players'] not in players[year]['Height']:
                        continue
                    boxscore_data.at[i,
                                    'Height'] = players[year]['Height'][row['Players']]
                    boxscore_data.at[i,
                                    'Weight'] = players[year]['Weight'][row['Players']]
                    boxscore_data.at[i,
                                    'Players'] = players[year]['Pos'][row['Players']]
                abstract_team = {
                    "C": {'Height': 0, 'Weight': 0, 'MP': 0, '2P': 0, '2PA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 'ORB': 0, 'DRB': 0, 'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, "PTS": 0},
                    "PF": {'Height': 0, 'Weight': 0, 'MP': 0, '2P': 0, '2PA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 'ORB': 0, 'DRB': 0, 'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, "PTS": 0},
                    "SF": {'Height': 0, 'Weight': 0, 'MP': 0, '2P': 0, '2PA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 'ORB': 0, 'DRB': 0, 'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, "PTS": 0},
                    "SG": {'Height': 0, 'Weight': 0, 'MP': 0, '2P': 0, '2PA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 'ORB': 0, 'DRB': 0, 'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, "PTS": 0},
                    "PG": {'Height': 0, 'Weight': 0, 'MP': 0, '2P': 0, '2PA': 0, '3P': 0, '3PA': 0, 'FT': 0, 'FTA': 0, 'ORB': 0, 'DRB': 0, 'AST': 0, 'STL': 0, 'BLK': 0, 'TOV': 0, 'PF': 0, "PTS": 0},
                }
                for i, row in boxscore_data.iterrows():
                    try:
                        t = row["MP"].split(":")
                        if t[0] == "Player Suspended" or t[0] == "Not With Team":
                            continue
                        time = (int(t[0])*60 + int(t[1]))/60.0
                        h = row["Height"].split("-")
                    except:
                        print(date, matchup, team_type)
                        print(boxscore_data)
                    else:
                        if row["Players"] == 'SG-PG':
                            row["Players"] = "PG"
                        if row["Players"] == 'SF-PF':
                            row["Players"] = "SF"
                        if row["Players"] == 'SG-SF':
                            row["Players"] = "SG"
                        if row["Players"] == "PF-C":
                            row["Players"] = "PF"
                        if row["Players"] == 'SG-PF':
                            row["Players"] = "SF"
                        abstract_team[row["Players"]
                                    ]['Height'] += (int(h[0])*12+int(h[1]))*time
                        abstract_team[row["Players"]
                                    ]['Weight'] += int(row["Weight"][0:3])*time
                        abstract_team[row["Players"]]['MP'] += time
                        abstract_team[row["Players"]
                                    ]['2P'] += row["FG"] - row["3P"]
                        abstract_team[row["Players"]
                                    ]['2PA'] += row["FGA"] - row["3PA"]
                        abstract_team[row["Players"]]['3P'] += row["3P"]
                        abstract_team[row["Players"]]['3PA'] += row["3PA"]
                        abstract_team[row["Players"]]['FT'] += row["FT"]
                        abstract_team[row["Players"]]['FTA'] += row["FTA"]
                        abstract_team[row["Players"]]['ORB'] += row["ORB"]
                        abstract_team[row["Players"]]['DRB'] += row["DRB"]
                        abstract_team[row["Players"]]['AST'] += row["AST"]
                        abstract_team[row["Players"]]['STL'] += row["STL"]
                        abstract_team[row["Players"]]['BLK'] += row["BLK"]
                        abstract_team[row["Players"]]['TOV'] += row["TOV"]
                        abstract_team[row["Players"]]['PF'] += row["PF"]
                        abstract_team[row["Players"]]['PTS'] += row["PTS"]
                for k, v in abstract_team.items():
                    if v["MP"] == 0:
                        continue
                    v['Height'] = v['Height'] / v['MP']
                    v['Weight'] = v['Weight'] / v['MP']
                boxscores[date][matchup][team_type] = pd.DataFrame(
                    abstract_team).transpose()
        print("done")
    print("all done")
    save_abstract_game(schedules, boxscores, "accurate_data.csv")

    ## true average abstract team on each game
    schedules = {}
    boxscores = {}
    players = {}

    for year in range(2015,2020):
        print(year)
        schedules_data = pd.read_csv("../data/schedule/schedule_{}.csv".format(year))
        players_data = pd.read_csv("../data/player/nba_player_stats_{}.csv".format(year)).set_index('Player')
        schedules[year] = schedules_data
        players[year] = players_data.to_dict('dict')

        for filename in os.listdir('../data/boxscore/{}'.format(year)):
            tokens = filename.split("_")
            date = tokens[1]+"_"+tokens[2]+"_"+tokens[3] 
            matchup = tokens[4]+"_"+tokens[5]
            team_type = tokens[6].split(".")[0]
            if date not in boxscores:
                boxscores[date] = {}
            
            if matchup not in boxscores[date]:
                boxscores[date][matchup] = {} 
                
            if team_type not in boxscores[date][matchup]:
                boxscore_data = pd.read_csv('../data/boxscore/{}/{}'.format(year, filename)).drop(["FG%","3P%","FT%"], axis=1)
                names = boxscore_data["Players"]
                
                for i, row in boxscore_data.iterrows():
                    if row['Players'] not in players[year]['Height']:
                        continue
                    boxscore_data.at[i, 'Height'] = players[year]['Height'][row['Players']]
                    boxscore_data.at[i,'Weight'] = players[year]['Weight'][row['Players']]
                    boxscore_data.at[i,'Players'] = players[year]['Pos'][row['Players']]
                abstract_team = {
                    "C" :{'Height':0,'Weight':0,'MP':0,'2P':0,'2PA':0,'3P':0,'3PA':0,'FT':0,'FTA':0,'ORB':0,'DRB':0,'AST':0,'STL':0,'BLK':0,'TOV':0,'PF':0,"PTS":0},
                    "PF":{'Height':0,'Weight':0,'MP':0,'2P':0,'2PA':0,'3P':0,'3PA':0,'FT':0,'FTA':0,'ORB':0,'DRB':0,'AST':0,'STL':0,'BLK':0,'TOV':0,'PF':0,"PTS":0},
                    "SF":{'Height':0,'Weight':0,'MP':0,'2P':0,'2PA':0,'3P':0,'3PA':0,'FT':0,'FTA':0,'ORB':0,'DRB':0,'AST':0,'STL':0,'BLK':0,'TOV':0,'PF':0,"PTS":0},
                    "SG":{'Height':0,'Weight':0,'MP':0,'2P':0,'2PA':0,'3P':0,'3PA':0,'FT':0,'FTA':0,'ORB':0,'DRB':0,'AST':0,'STL':0,'BLK':0,'TOV':0,'PF':0,"PTS":0},
                    "PG":{'Height':0,'Weight':0,'MP':0,'2P':0,'2PA':0,'3P':0,'3PA':0,'FT':0,'FTA':0,'ORB':0,'DRB':0,'AST':0,'STL':0,'BLK':0,'TOV':0,'PF':0,"PTS":0},
                }
                for i, row in boxscore_data.iterrows():
                    try:
                        t = row["MP"].split(":")
                        if t[0] == "Player Suspended" or t[0] == "Not With Team":
                            continue
                        time = (int(t[0])*60 + int(t[1]))/60.0
                        total_time = players[year]['MP'][names[i]]
                        h = row["Height"].split("-")
                    except:
                        print(date, matchup, team_type)
                        print(boxscore_data)
                    else:
                        if row["Players"]== 'SG-PG':
                            row["Players"] = "PG"
                        if row["Players"]== 'SF-PF':
                            row["Players"] = "SF"
                        if row["Players"]== 'SG-SF':
                            row["Players"] = "SG"
                        if row["Players"]== "PF-C":
                            row["Players"] = "PF"
                        if row["Players"]== 'SG-PF':
                            row["Players"] = "SF"
                        abstract_team[row["Players"]]['Height'] += (int(h[0])*12+int(h[1]))*time
                        abstract_team[row["Players"]]['Weight'] += int(row["Weight"][0:3])*time
                        abstract_team[row["Players"]]['MP'] += time
                        abstract_team[row["Players"]]['2P'] += players[year]['2P'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['2PA'] += players[year]["2PA"][names[i]]*time/total_time
                        abstract_team[row["Players"]]['3P'] += players[year]["3P"][names[i]]*time/total_time
                        abstract_team[row["Players"]]['3PA'] += players[year]['3PA'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['FT'] += players[year]['FT'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['FTA'] += players[year]['FTA'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['ORB'] += players[year]['ORB'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['DRB'] += players[year]['DRB'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['AST'] += players[year]['AST'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['STL'] += players[year]['STL'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['BLK'] += players[year]['BLK'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['TOV'] += players[year]['TOV'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['PF'] += players[year]['PF'][names[i]]*time/total_time
                        abstract_team[row["Players"]]['PTS'] += players[year]['PTS'][names[i]]*time/total_time
                        
                for k,v in abstract_team.items():
                    if v["MP"] == 0:
                        continue
                    v['Height'] = v['Height']/ v['MP']
                    v['Weight'] = v['Weight']/ v['MP']
                boxscores[date][matchup][team_type] = pd.DataFrame(abstract_team).transpose()  
                ##print(boxscores[date][matchup][team_type])
        print("done")
    print("all done")
    save_abstract_game(schedules, boxscores, "average_data.csv")
