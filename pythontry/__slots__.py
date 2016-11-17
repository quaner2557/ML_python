class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
#__slots__定义的属性仅对当前类实例起作用，对继承的子类不起作用
class GraduateStudent(Student):
    pass

s = Student() # 创建新的实例
s.name = 'Michael' # 绑定属性'name'
s.age = 25 # 绑定属性'age'
# ERROR: AttributeError: 'Student' object has no attribute 'score'
try:
    s.score = 99
except AttributeError as e:
    print('AttributeError:', e)

g = GraduateStudent()
g.score = 99
print('g.score =', g.score)


