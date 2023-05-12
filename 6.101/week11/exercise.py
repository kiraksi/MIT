# What will be printed by the following? (Or what exceptions will be
# raised?)  Draw an environment diagram to represent the program
# execution.

x = 0
def outer():
    x = 1
    def inner():
        x = 2
        print("inner:", x)

    inner()
    print("outer:", x)

outer()
print("global:", x)
