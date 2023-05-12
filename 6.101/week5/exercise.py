# Given the following tree representation:

t1 = {'value': 3, 'children': []}

t2 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                {'value': 3, 'children': []},
                {'value': 7, 'children': []}]}

t3 = {'value': 9,
      'children': [{'value': 2, 'children': []},
                {'value': 3,
                    'children': [{'value': 99, 'children': []},
                                {'value': 16,
                                'children': [{'value': 7, 'children': []}]},
                                {'value': 42, 'children': []}]}]}

def tree_max(tree):
    """
    Given tree as dict { value: number, children: list of trees },
    returns the maximum value found in the tree
    """
    ...
