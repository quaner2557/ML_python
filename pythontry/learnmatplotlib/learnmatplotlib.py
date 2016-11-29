import numpy as np
from matplotlib import pyplot as plt
# X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
# C,S=np.cos(X),np.sin(X)
# plt.plot(X,C,color="black",linewidth=1.0,linestyle="-")
# plt.plot(X,S)
# plt.xlim(-3.0,3.0)
# plt.xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi])
# ax = plt.gca() # gca stands for 'get current axis'
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.spines['bottom'].set_position(('data',0))
# ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('data',0))
#
# plt.plot(X,C,color="blue",linewidth=2.5,linestyle="-",label="cosine")
# plt.legend(loc='upper left')
#
# t = 2 * np.pi/3
# plt.plot([t, t], [0, np.cos(t)], color='blue', linewidth=2.5, linestyle="--")
# plt.scatter([t, ], [np.cos(t), ], 50, color='blue')
# plt.annotate(r'$sin(\frac{2\pi}{3})=\frac{\sqrt{3}}{2}$',
# xy=(t, np.sin(t)), xycoords='data',
# xytext=(+10, +30), textcoords='offset points', fontsize=16,
# arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
# plt.plot([t, t],[0, np.sin(t)], color='red', linewidth=2.5, linestyle="--")
# plt.scatter([t, ],[np.sin(t), ], 50, color='red')
# plt.annotate(r'$cos(\frac{2\pi}{3})=-\frac{1}{2}$',
# xy=(t, np.cos(t)), xycoords='data',
# xytext=(-90, -50), textcoords='offset points', fontsize=16,
# arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
#
#
#
# plt.show()
#
# n = 256
# X = np.linspace(-np.pi, np.pi, n, endpoint=True)
# Y = np.sin(2 * X)
# plt.plot(X, Y + 1, color='blue', alpha=1.00)
# plt.plot(X, Y - 1, color='blue', alpha=1.00)
#
# plt.show()
#
# n = 1024
# X = np.random.normal(0,1,n)
# Y = np.random.normal(0,1,n)
# plt.scatter(X,Y)
#
# plt.show()
#
# n = 12
# X = np.arange(n)
# Y1 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
# Y2 = (1 - X / float(n)) * np.random.uniform(0.5, 1.0, n)
# plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
# plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')
# for x, y in zip(X, Y1):
#   plt.text(x + 0.4, y + 0.05, '%.2f ' % y, ha='center', va='bottom')
# plt.ylim(-1.25, +1.25)
# plt.show()

# def f(x, y):
#    return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 -y ** 2)
# n = 256
# x = np.linspace(-3, 3, n)
# y = np.linspace(-3, 3, n)
# X, Y = np.meshgrid(x, y)
# plt.contourf(X, Y, f(X, Y), 8, alpha=.75, cmap='jet')
# C = plt.contour(X, Y, f(X, Y), 8, colors='black', linewidth=.5)
# plt.show()

def f(x, y):
   return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
n = 10
x = np.linspace(-3, 3, 4 * n)
y = np.linspace(-3, 3, 3 * n)
X, Y = np.meshgrid(x, y)
plt.imshow(f(X, Y))

plt.subplot(2,2,1)
# plt.show()