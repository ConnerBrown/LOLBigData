import pandas as pd
import pprint
import ast

data = pd.read_csv("raw/LeagueofLegends.csv")

data = data[["Year", "bResult", "gamelength", "golddiff", "bKills", "bTowers", "bInhibs", "bDragons", "bBarons", "bHeralds", "rKills", "rTowers", "rInhibs", "rDragons", "rBarons", "rHeralds", "blueTopChamp", "blueJungleChamp", "blueMiddleChamp", "blueADCChamp", "blueSupportChamp", "redTopChamp", "redJungleChamp", "redMiddleChamp", "redADCChamp", "redSupportChamp"]]
data = data[data.Year != 2014]
data = data[data.Year != 2015]

data_cleaned = []

gameID = 0

for index, row in data.iterrows():
    gameID += 1
    line = []
    line.append(gameID)
    length = int(row['gamelength'])
    line.append(length)
    line.append(int(row['Year']))
    line.append(row['bResult'])
    line.append(row['blueTopChamp'])
    line.append(row['blueJungleChamp'])
    line.append(row['blueMiddleChamp'])
    line.append(row['blueADCChamp'])
    line.append(row['blueSupportChamp'])
    line.append(row['redTopChamp'])
    line.append(row['redJungleChamp'])
    line.append(row['redMiddleChamp'])
    line.append(row['redADCChamp'])
    line.append(row['redSupportChamp'])
    gold = ast.literal_eval(row['golddiff'])
    b_kills = ast.literal_eval(row['bKills'])
    b_towers = ast.literal_eval(row['bTowers'])
    b_inhibs = ast.literal_eval(row['bInhibs'])
    b_dragons = ast.literal_eval(row['bDragons'])
    b_barons = ast.literal_eval(row['bBarons'])
    b_heralds = ast.literal_eval(row['bHeralds'])
    r_kills = ast.literal_eval(row['rKills'])
    r_towers = ast.literal_eval(row['rTowers'])
    r_inhibs = ast.literal_eval(row['rInhibs'])
    r_dragons = ast.literal_eval(row['rDragons'])
    r_barons = ast.literal_eval(row['rBarons'])
    r_heralds = ast.literal_eval(row['rHeralds'])
    for i in range(length):
        minute = [i+1] + line[:]
        minute.append(gold[i])
        b_kill_total = 0
        for kill in b_kills:
            if float(kill[0]) <= i:
                b_kill_total += 1
        minute.append(b_kill_total)
        
        b_tower_total = 0
        for tower in b_towers:
            if float(tower[0]) <= i:
                b_tower_total += 1
        minute.append(b_tower_total)
        
        b_inhib_total = 0
        for inhib in b_inhibs:
            if float(inhib[0]) <= i:
                b_inhib_total += 1
        minute.append(b_inhib_total)
        
        b_dragon_total = 0
        for dragon in b_dragons:
            if float(tower[0]) <= i:
                b_tower_total += 1
        minute.append(b_tower_total)
        
        b_baron_total = 0
        for baron in b_barons:
            if float(baron[0]) <= i:
                b_baron_total += 1
        minute.append(b_baron_total)
        
        b_herald_total = 0
        for herald in b_heralds:
            if float(herald[0]) <= i:
                b_herald_total += 1
                if b_herald_total ==3:
                    print(b_heralds)
                    print(line[2])
                    print(line[1])
                    print(line[0])
        minute.append(b_herald_total)

        r_kill_total = 0
        for kill in r_kills:
            if float(kill[0]) <= i:
                r_kill_total += 1
        minute.append(r_kill_total)
        
        r_tower_total = 0
        for tower in r_towers:
            if float(tower[0]) <= i:
                r_tower_total += 1
        minute.append(r_tower_total)
        
        r_inhib_total = 0
        for inhib in r_inhibs:
            if float(inhib[0]) <= i:
                r_inhib_total += 1
        minute.append(r_inhib_total)
        
        r_dragon_total = 0
        for dragon in r_dragons:
            if float(tower[0]) <= i:
                r_tower_total += 1
        minute.append(r_tower_total)
        
        r_baron_total = 0
        for baron in r_barons:
            if float(baron[0]) <= i:
                r_baron_total += 1
        minute.append(r_baron_total)
        
        r_herald_total = 0
        for herald in r_heralds:
            if float(herald[0]) <= i:
                r_herald_total += 1
                if r_herald_total == 3:
                    print(r_heralds)
                    print(line[2])
                    print(line[1])
                    print(line[0])
        minute.append(r_herald_total)

        data_cleaned.append(minute)

headers = ['Minute', 'GameID', 'gamelength', 'Year', 'bResult', 'blueTopChamp', 'blueJungleChamp', 'blueMiddleChamp', 'blueADCChamp', 'blueSupportChamp', 'redTopChamp', 'redJungleChamp', 'redMiddleChamp', 'redADCChamp', 'redSupportChamp', 'golddiff', 'bKills', 'bTowers', 'bInhibs', 'bDragons', 'bBarons', 'bHeralds', 'rKills', 'rTowers', 'rInhibs', 'rDragons', 'rBarons', 'rHeralds']

df_clean = pd.DataFrame(data_cleaned, columns=headers)
df_clean.to_csv("LoL_clean.csv")

