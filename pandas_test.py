import pandas as pd
import ast

data = pd.read_csv("raw/LeagueofLegends.csv")

data = data[["Year", "bResult", "gamelength", "golddiff", "bKills", "bTowers", "bInhibs", "bDragons", "bBarons", "bHeralds", "rKills", "rTowers", "rInhibs", "rDragons", "rBarons", "rHeralds", "blueTopChamp", "blueJungleChamp", "blueMiddleChamp", "blueADCChamp", "blueSupportChamp", "redTopChamp", "redJungleChamp", "redMiddleChamp", "redADCChamp", "redSupportChamp"]]
data = data[data.Year != 2015]

print(data)
