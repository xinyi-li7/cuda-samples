import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("performance.csv")

program = df["program"]
soap_slow = df["soap_slowdown"]
gpufpx_slow = df["GPU-FPX_slowdown"]
x = np.log(gpufpx_slow)
y = np.log(soap_slow)
#print(x)
#print(y)
#plt.axis('scaled')
#plt.plot(range(5))
# for n in range(0,len(x)-1):
#     if(x[n] < y[n]):
#         print(program[n])s
f, ax = plt.subplots(figsize=(8, 8))
plt.axis('square')
#ax = plt.axes()
ax.plot([0, 1], [0, 1], transform=ax.transAxes,linestyle='dashdot')
ax.scatter(x,y,c=".01")
plt.xlabel('log(slowdown) for GPU-FPX')
plt.ylabel('log(slowdown) for CPU version')
ax.set(xlim=(-0.5, 7.5), ylim=(-0.5, 7.5))





#plt.scatter(x,y)

plt.savefig("performance.png")
