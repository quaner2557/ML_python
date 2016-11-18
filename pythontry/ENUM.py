#######################################################################################
# 我们就获得了Month类型的枚举类，可以直接使用Month.Jan来引用一个常量，或者枚举它的所有成员：
# value属性则是自动赋给成员的int常量，默认从1开始计数。
from enum import Enum
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

for name, member in Month.__members__.items():
    print(name, '=>', member, ',', member.value)

# 如果需要更精确地控制枚举类型，可以从Enum派生出自定义类
from enum import Enum, unique

@unique
class Weekday(Enum):
    Sun = 0 # Sun的value被设定为0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
# 既可以用成员名称引用枚举常量，又可以直接根据value的值获得枚举常量
print(Weekday.Tue)
print(Weekday['Tue'])
print(Weekday.Tue.value)
print(Weekday(1))
for name, member in Weekday.__members__.items():
     print(name, '=>', member)

for value in Weekday.__members__.items():
    print(value)

for value in Weekday.__members__.values():
    print(value)

for value in Weekday.__members__.values():
    print(value.value)