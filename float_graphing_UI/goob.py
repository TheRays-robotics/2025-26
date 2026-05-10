import matplotlib.pyplot as plt
import numpy as np

days = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130]
temperatue = [0,17,44,89,128,182,215,236,247,261,277,284,295,302,301,293,281,279,252,212,174,136,92,88,94,103,91]
temperature =[]
for i in temperatue:
    temperature.append(i*-1)
plt.plot(days, temperature, marker='o')
plt.title('')
plt.xlabel('time')
plt.ylabel('depth')
plt.show()