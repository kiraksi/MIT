## Let’s look at a simple piece of code:
x = 10
y = x
x = 7
y  #?


## Here’s a similar-looking case:
x = [10]
y = x
x = [7]
y  #?


## Now let’s think about this case:
x = [10]
y = x
x[0] = 7
y  #?


## This behavior can cause hard-to-detect bugs. Let’s look at this
## function:
def clean_list(data):
    # Returns a new version of `data` in which all empty lists inside
    # `data` have been removed. Leaves `data` unchanged.
    new_data = data
    while [] in new_data:
        new_data.remove([])
    return new_data

# Does this function do the right thing?
x = [1, [2, 3], [], 4]
y = clean_list(x)
y  #?

# OK, but let’s look more closely at the spec. Did we change x?
x  #?


## Here are a number of interesting cases:
x = 5
y = x
x += 3
x  #?
y  #?

x = [5]
y = x
x += [3]
x  #?
y  #?

x = [5]
y = x
x = x + [3]
x  #?
y  #?


## One with += but now with strings:
x = "today is "
y = "Wednesday"
z = x
x += y
x  #?
z  #?


## Aliasing/mutation can be useful!

armando_grades = [87, 93]
bethany_grades = [89, 89]
cameron_grades = [93, 91]

# everyone got 100% on the project
for grade_list in [armando_grades, bethany_grades, cameron_grades]:
    grade_list.append(100)

armando_mean = sum(armando_grades) / len(armando_grades)

print("armando_grades:", armando_grades) #?
print("bethany_grades:", bethany_grades) #?


## Avoiding aliasing

# approach: copy rather than alias

def clean_list(data):
    # Returns a new version of `data` in which all empty lists inside
    # `data` have been removed. Leaves `data` unchanged.

    #new_data = data #OLD
    new_data = data[:]  # top-level copy!
    while [] in new_data:
        new_data.remove([])
    return new_data

x = [1, [2, 3], [], 4]
y = clean_list(x)
y  #?
x  #?

