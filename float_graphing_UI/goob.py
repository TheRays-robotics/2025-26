import matplotlib.pyplot as plt
import numpy as np
import re
file = open("2025-26/float_graphing_UI/data.txt")

lines = file.readlines()
days = []
temperature = []

for line in lines:
    days.append(float(re.findall(r"T.*T",line)[-1].strip("T")))
    temperature.append(float(re.findall(r"P.*P",line)[-1].strip("P"))*-1)





plt.plot(days, temperature, marker='o')
plt.title('')
plt.xlabel('time')
plt.ylabel('depth')
plt.show()



#ice tank at words is 