import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("raw/LeagueofLegends.csv")
blue = df[df.bResult == 1]
red = df[df.bResult == 0]

print("Blue:")
print("    # -", blue.shape[0])
print("    % -", blue.shape[0]/df.shape[0])
print()
print("Red:", red.shape[0])
print("    # -", red.shape[0])
print("    % -", red.shape[0]/df.shape[0])

print(blue)

df2 = pd.read_csv("LoL_clean_manual.csv")
blue = df2[df2.bResult == 1]
red = df2[df2.bResult == 0]
print(df2.shape[0])
length_l = df[["gamelength"]]
length_l = length_l.values.tolist()
length = []
for elem in length_l:
    length.append(elem[0])
print("Shortest game:", min(length))
print("Longest Game:", max(length))
average = sum(length) / len(length)
print("Average:", average)

gold_r = red[["Minute", "golddiff"]].values.tolist()
gold_b = blue[["Minute", "golddiff"]].values.tolist()



gold_minute = {}
for i in range(len(gold_r)):
    if gold_r[i][0] in gold_minute:
        gold_minute[gold_r[i][0]].append(-gold_r[i][1])
    else:
        gold_minute[gold_r[i][0]] = [-gold_r[i][1]]

for i in range(len(gold_b)):
    if gold_b[i][0] in gold_minute:
        gold_minute[gold_b[i][0]].append(gold_b[i][1])
    else:
        gold_minute[gold_b[i][0]] = [gold_b[i][1]]
print(gold_minute[75])

for x in gold_minute:
    gold_minute[x] = sum(gold_minute[x]) / len(gold_minute[x])

averages = []
i = 1
while i in gold_minute:
    averages.append(gold_minute[i])
    i += 1
y = [i+1 for i in range(len(averages)-1)]
print
plt.plot(y, averages[:74])
plt.xlabel("minute")
plt.ylabel("golddiff")
plt.title("Average gold lead of the winning team by minute")
plt.show()

