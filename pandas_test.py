import pandas as pd
import ast

data = pd.read_csv("raw/LeagueofLegends.csv")

data = data[["Year", "bResult", "gamelength", "golddiff", "bKills", "bTowers", "bInhibs", "bDragons", "bBarons", "bHeralds", "rKills", "rTowers", "rInhibs", "rDragons", "rBarons", "rHeralds", "blueTopChamp", "blueJungleChamp", "blueMiddleChamp", "blueADCChamp", "blueSupportChamp", "redTopChamp", "redJungleChamp", "redMiddleChamp", "redADCChamp", "redSupportChamp"]]
data = data[data.Year != 2014]
data = data[data.Year != 2015]

data_cleaned = []

for index, row in data.iterrows():
    line = []
    line.append(int(row['Year']))
    line.append(row['bResult'])
    line.append(row['blueTopChamp'])
    line.append(row['blueJungleChamp'])
    line.append(row['blueMiddleChamp'])
    line.append(row['blueADCChamp'])
    line.append(row['redSupportChamp'])
    line.append(row['redTopChamp'])
    line.append(row['redJungleChamp'])
    line.append(row['redMiddleChamp'])
    line.append(row['redADCChamp'])
    line.append(row['redSupportChamp'])
    length = int(row['gamelength'])
    line.append(length)
    gold = ast.literal_eval(row['golddiff'])
    b_kills = ast.literal_eval(row['bKills'])
    b_towers = ast.literal_eval(row['rTowers'])
    b_inhibs = ast.literal_eval(row['rInhibs'])
    b_dragons = ast.literal_eval(row['rDragons'])
    b_barons = ast.literal_eval(row['rBarons'])
    b_heralds = ast.literal_eval(row['rHeralds'])
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
        b_tower_total = 0
        for tower in b_towers:
            if float(tower[0]) <= i:
                b_tower_total += 1
        minute.append(b_tower_total)
        b_tower_total = 0
        for tower in b_towers:
            if float(tower[0]) <= i:
                b_tower_total += 1
        minute.append(b_tower_total)
    data_cleaned.append(line)

