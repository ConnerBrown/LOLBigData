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

df2 = pd.read_csv("LoL_clean_manual.csv")
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
