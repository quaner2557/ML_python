#  面向过程的写法
std1 = {'name': 'Michael', 'score': 98}
std2 = {'name': 'Bob', 'score': 81}
print('%s:%s' %(std1['name'], std1['score']))

# 面向对象的写法
# 类名通常是大写开头的单词
# (object)表示该类是从哪个类继承下来的
class Student(object):
    #第一个参数永远是self
    def __init__(self, name, score):
        self.name=name
        self.score=score

    def print_score(self):
        print('%s:%s' % (self.name, self.score))

#要调用一个方法，只需要在实例变量上直接调用
# 除了self不用传递，其他参数正常传入
bart = Student('Bart Simpson', 59)
bart.print_score()

# Python允许对实例变量绑定任何数据
# 对两个实例变量，拥有的变量名称都可能不同
# >>> bart = Student('Bart Simpson', 59)
# >>> lisa = Student('Lisa Simpson', 87)
# >>> bart.age = 8
# >>> bart.age
# 8
# >>> lisa.age
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# AttributeError: 'Student' object has no attribute 'age'

# 让内部属性不被外部访问，可以把属性的名称前加上两个下划线__
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))

    def get_grade(self):
        if self.__score >= 90:
            return 'A'
        elif self.__score >= 60:
            return 'B'
        else:
            return 'C'

# 变量名类似__xxx__的是特殊变量，可以直接访问，不是private变量


#####################################################################
# 继承和多态
