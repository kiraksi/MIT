# You are organizing a potluck for your friends, and you want to make
# sure that everybody who comes to your party has something that they
# can eat!
# 
# Given a dictionary containing food preferences (mapping person =>
# list of foods they will eat), and a dictionary containing the food
# you have on the table (mapping food name => quantity), we want to
# give everybody one food in their preferences, but we can't give out
# more of a particular food than we have available at the start.

def feed(people, table):
    """
    >>> feed({'alice': ['pickles', 'ketchup'], 'bob': ['pickles']},
    ...      {'pickles': 1, 'ketchup': 1}) == {'alice': 'ketchup', 'bob': 'pickles'}
    True
    >>> feed({'alice': ['pickles'], 'bob': ['pickles']},
    ...      {'pickles': 1, 'ketchup': 1}) == None
    True
    >>> feed({'alice': ['pickles'], 'bob': ['pickles']},
    ...      {'pickles': 2, 'ketchup': 1}) == {'alice': 'pickles', 'bob': 'pickles'}
    True
    """


    """

Exercise: develop a STRATEGY to implement this

* Base case(s)?



* What kind of things need to be tried? I.e., how can
  the search proceed one step at a time?




* What are recursive case(s)? How does the problem get
  smaller on each step/recursion?




* How detect and handle when the recursion fails?

"""
