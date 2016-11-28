from numpy import *
a = arange(12)
b = a
# print(a,b)
b.shape = 3,4
# print(a,b)
c = a.view()
print(a)
c.shape = 2,6
c[0,4] = 1234
print(a)
palette = array( [ [0,0,0],                # black
                  [255,0,0],              # red
                   [0,255,0],              # green
                  [0,0,255],              # blue
                  [255,255,255] ] )       # white
print(palette)
B = arange(12).reshape(3,4)
M = mat(B.copy())
print(M[:,M.A[0,:]>1])