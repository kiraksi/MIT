# Python list vs. linked-list (LL)
lst1 = [1, 2, 3]
LL1 = (1, (2, (3, None)))

lst2 = [3]
LL2 = (3, None)

lst3 = []
LL3 = None


# Exercise 1: implement LL_elements as a function:

def LL_elements(LL):
    """
    return a Python list of all of the elements in a linked list

    """
    ...





# Exercise 2: implement LL_elements as a generator:

def LL_elements(LL):
    """
    return an iterable of all of the elements in a linked list

    """
    ...





if __name__ == "__main__":
    for ele in LL_elements(make_LL(1, 2, 3)):
        print(ele)
    # prints
    # 1
    # 2
    # 3

