# 类似__slots__这种形如__xxx__的变量或者函数名在Python中是有特殊用途的

###################################################################
# __str__
class Student(object):
    def __init__(self,name):
        self.name = name

    def __str__(self):
        return 'Student object (name:%s)' % self.name

print(Student('Michael'))

#################################################################
# __iter__
# 如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法
# 该方法返回一个迭代对象，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值
# 直到遇到StopIteration错误时退出循环。
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a+self.b # 计算下一个值
        if self.a > 100000:           # out iteration
           raise StopIteration();
        return self.a                 # 返回下一个值

for n in Fib():
    print(n)

###############################################################
# __getitem__
# others like __setitem__() __delitem__()
# 要表现得像list那样按照下标取出元素，需要实现__getitem__()方法
class Fib2(object):
    def __getitem__(self, n):
        if isinstance(n, int):
           a, b = 1, 1
           for x in range(n):
                a, b = b, a+b
           return a

        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

print(Fib2()[0])
print(Fib2()[0:5])

###############################################################
# 当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')
# 来尝试获得属性，这样，我们就有机会返回score的值：

# class Student(object):
#
#     def __getattr__(self, attr):
#         if attr=='age':
#             return lambda: 25
#         raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)


###############################################################
# 任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用。请看示例：
class Student(object):
    def __init__(self,name):
        self.name = name

    def __call__(self, *args, **kwargs):
        print('My name is %s.' % self.name)

s = Student('Michael')
print(s())


# =============================================
# 完全动态调用特性：
# 把一个类的所有属性和方法调用全部动态化处理

# __call__(): 用于实例自身的调用，达到()调用的效果
# 即可以把此类的对象当作函数来使用，相当于重载了括号运算符

# __getattr__(): 当调用不存在的属性时调用此方法来尝试获得属性
class Chain(object):
    def __init__(self, path=''):    # 默认路径参数path为空
        self._path = path

    def __getattr__(self, path):
        print('call __getattr__(%s)' % path)
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    def __call__(self, param):
        print('cal __call__(%s)' % param)
        return Chain('%s/%s' % (self._path, param))

    __repr__ = __str__


# /status/user/timeline/list
# Chain().status.user.timeline.list调用分析
# 首先执行Chain()返回一个实例对象C1(path = '')，
# 通过实例对象C1来获取status属性，因为C1中不存在status属性，所以就会调用
# __getattr__()来尝试获取status属性，接着通过__getattr__()方法返回
# 带参数status的实例对象C2(path = '/status')，然后通过实例对象C2来获取user属性，
# C2中不存在user属性，接着调用__getattr__()方法返回带参数user
# 的实例对象C3(path = '/status/user')，然后通过实例对象C3来获取timeline属性，
# 因C3不存在timeline属性，故调用__getattr__()方法返回带参数timeline
# 的实例对象C4(path = '/status/user/timeline')，通过实例对象C4来获取list属性，
# 又因C4中不存在list属性，调用__getattr__()方法返回带参数list
# 的实例对象C5(path = '/status/user/timeline/list')，
# 最后通过调用__str__()方法来打印实例对象C5，即返回/status/user/timeline/list
# 具体参考见下面的测试结果
print(Chain().status.user.timeline.list)
print('--------------------------------------')

# GET /users/:user/repos
# :user替换为实际用户名
# /users/Lollipop/repos
# Chain().users('Lollipop').repos 调用分析
# 首先执行Chain()返回一个实例对象Q1(path = '')，
# 通过实例对象Q1来获取users属性，因为Q1中不存在users属性，
# 所以就会调用__getattr__()方法尝试获取users属性，接着通过
# __getattr__()方法返回带参数users的实例对象Q2(path = '/users')，
# 然后因为通过()直接调用实例对象Q2，并带参数'Lollipop'，故会调用
# __call__()方法，返回了带参数Lollipop的实例对象Q3(path = '/users/Lollipop')，
# 接着通过实例对象Q3来获取repos属性，又因Q3中不存在repos属性，即会调用
# __getattr__()方法返回带参数repos的实例对象Q4(path = '/users/Lollipop/repos')
# 最后通过调用__str__()方法来打印实例对象Q4，即返回/users/Lollipop/repos
# 具体参考见下面的测试结果
print(Chain().users('Lollipop').repos)

