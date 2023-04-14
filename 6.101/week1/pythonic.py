""" Lab 1 Midpoint """

# Every object in Python has a type (class). An object
# or value is an "instance" of that type.
#
# There are corresponding operations and functions that accept,
# manipulate, or create objects depending on their type.

# How learn about the available types, and their operations?
#
# See the Python documentation!
#
# https://docs.python.org/3/library/stdtypes.html
# https://docs.python.org/3/library/functions.html


## We can see the type, and test if an object is an instance of a given type:

x = 5
type(x)  # ?
isinstance(x, int)  # ?
isinstance(True, int)  # ?


## Different notions of equivalence

x = 5
y = x
x == y  # ?
x is y  # ?

x = 123456
y = 123456
x == y  # ?
x is y  # risky


# "pythonic" means idiomatic Python
#
# - more recognizable to other Python programmers
# - done't write Python with a Java or C accent!

## The following is python with a "C" language accent. 
## How would you rewrite the following to be more pythonic?

colors = ["red", "green", "blue", "yellow"]
names = {"Alice", "Bob", "Cam"}

i = 0
while i < len(colors):
    print(colors[i])
    i += 1

# What if we wanted to print in reverse order?

for c in reversed(colors):  # not colors.reverse()! Why?
    print(c)

for c in colors[::-1]:
    print(c)

    

## iterables

# Some types are "iterable", so we can loop over them:

my_list = [1, 2, 3]
for elem in my_list:
    print("list element", elem)

my_set = {1, 2, 3}
for elem in my_set:
    print("set element", elem)

# What will this print?
my_nums = {1: 'one', 2: 'two', 3: 'three'}
for elem in my_nums:
    print("dictionary element:", elem)

# How print both key and value?


## The 'in' operator works on iterables to test membership

2 in my_list      # True
2 in my_set       # True
2 in my_nums      # ?
"two" in my_nums  # ?
    

## Important iterators: range, enumerate

# Will almost never create a "range" unless in a loop. But...
# they are also Python objects!

r = range(5, 16, 5)
r  # ?
type(r)  # ?
list(r)  # ?

# more usual use...
fives = []
for f in range(5, 16, 5):
    fives.append(f)

# more pythonic
fives = list(range(5, 16, 5))


## List comprehensions

result = 0
for i in range(5):
    s = i**2
    result += s

# Much better: list comprehension!
result = [i**2 for i in range(5)]


## Not just *list* comprehensions!

x_to_the_x = {}
for x in range(10):
    x_to_the_x[x] = x**x

# How make the above more pythonic?
x_to_the_x = {x: x**x for x in range(10)}
