from numpy import *
a = arange(15).reshape(3,5)
print(a.shape)
print(a.ndim)
print(a.dtype)
print(ones( (2,3,4), dtype=int16 ) )
print(random.random((2,3)))
b=linspace(0, pi, 3)
print(b)
print(type(b))
for row in b:
    print(row)
for element in b.flat:
    print(element)

a=random.random((3,4))
a.shape=(2,6)
print(a)
print(a.transpose())
