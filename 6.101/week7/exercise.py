## Fix the buggy implementation of zip_lists below:

# Linked list representation
#
# Each linked list has zero or more elements. An empty linked list is
# represented as an empty list, a linked list with a single element is
# a list of length one, and a linked list with more than one element
# is represented as a list containing [element, rest], where rest is a
# linked list.


def zip_lists(linked1, linked2):
    """Given two linked lists (not necessarily of the same length, return
    a linked list of tuples of the corresponding elements in the two
    linked lists (for as many tuples as there are elements in the
    shortest linked list)

    """
    if not linked1 or not linked2:
        return []
    start = [(linked1[0], linked2[0])]
    end = zip_lists(linked1[1:], linked2[1:])
    if end:
        start.append(end)
    return start
