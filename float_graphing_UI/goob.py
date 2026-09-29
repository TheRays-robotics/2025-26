import matplotlib.pyplot as plt
import numpy as np
import re
file = open("2025-26/float_graphing_UI/data.txt")

lines = file.readlines()
days = []
temperataure = [0,35,85,157,221,260,282,260,202,137,58,31,61,94,147,219,248,268,281,253,178,104,75,53,52,51,50]

# for line in lines:
#     days.append(float(re.findall(r"T.*T",line)[-1].strip("T")))
#     temperature.append(float(re.findall(r"P.*P",line)[-1].strip("P"))*-1)

temperature = []
for i in range(27):
    days.append(i*5)
for i in temperataure:
    temperature.append(i*-1)




plt.plot(days, temperature, marker='o')
plt.title('')
plt.xlabel('time')
plt.ylabel('depth')
plt.show()



#ice tank at words is 