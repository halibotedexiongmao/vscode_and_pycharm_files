import numpy as np
from matplotlib import pyplot as plt
plt.subplot(2,2,1)
x = np.arange(1,20)
y1 = 2 * x + 5
y2=np.sin(x)
plt.title("Matplotlib demo")
plt.xlabel("x axis caption")
plt.ylabel("y axis caption")
plt.plot(x, y1, linestyle='', marker='o', markersize=3)

plt.subplot(2,2,2)
plt.bar(y1,y2,align='center')

plt.subplot(2,2,4)
plt.title('sin wave')
#plt.plot(x,y2, linestyle='', marker='o', markersize=3)
plt.scatter(x, y2, s=30)

#plt.subplot(2,2,(2,1))
#plt.plot(y1,y2)
plt.show()
