"""
6.1010 Spring '23 Lab 4: Recipes
"""
#!/usr/bin/env python3
import os
import sys
import copy
import json
import pickle
import random

import lab

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


example_recipes = [
    ('compound', 'chili', [('beans', 3), ('cheese', 10), ('chili powder', 1), ('cornbread', 2), ('protein', 1)]),
    ('atomic', 'beans', 5),
    ('compound', 'cornbread', [('cornmeal', 3), ('milk', 1), ('butter', 5), ('salt', 1), ('flour', 2)]),
    ('atomic', 'cornmeal', 7.5),
    ('compound', 'burger', [('bread', 2), ('cheese', 1), ('lettuce', 1), ('protein', 1), ('ketchup', 1)]),
    ('compound', 'burger', [('bread', 2), ('cheese', 2), ('lettuce', 1), ('protein', 2),]),
    ('atomic', 'lettuce', 2),
    ('compound', 'butter', [('milk', 1), ('butter churn', 1)]),
    ('atomic', 'butter churn', 50),
    ('compound', 'milk', [('cow', 1), ('milking stool', 1)]),
    ('compound', 'cheese', [('milk', 1), ('time', 1)]),
    ('compound', 'cheese', [('cutting-edge laboratory', 11)]),
    ('atomic', 'salt', 1),
    ('compound', 'bread', [('yeast', 1), ('salt', 1), ('flour', 2)]),
    ('compound', 'protein', [('cow', 1)]),
    ('atomic', 'flour', 3),
    ('compound', 'ketchup', [('tomato', 30), ('vinegar', 5)]),
    ('atomic', 'chili powder', 1),
    ('compound', 'ketchup', [('tomato', 30), ('vinegar', 3), ('salt', 1), ('sugar', 2), ('cinnamon', 1)]),  # the fancy ketchup
    ('atomic', 'cow', 100),
    ('atomic', 'milking stool', 5),
    ('atomic', 'cutting-edge laboratory', 1000),
    ('atomic', 'yeast', 2),
    ('atomic', 'time', 10000),
    ('atomic', 'vinegar', 20),
    ('atomic', 'sugar', 1),
    ('atomic', 'cinnamon', 7),
    ('atomic', 'tomato', 13),
]

def compare_recipe_list(expected, result):
    assert len(expected) == len(result), f'Expected recipes list of length {len(expected)} but got {len(result)}'
    assert type(expected) == type(result), f'Expected recipes list to be of type {type(expected)} but got {type(result)}'
    for item in result:
        assert isinstance(item, tuple), f'Expected all items in recipes to be a tuple but got {item}'
        assert len(item) == 3, f'Expected all items in recipes to have length 3 but got {len(item)} \n for {item}'
        a, b, c = item
        assert isinstance(a, str) and a in {'atomic', 'compound'}, f'Expected first item in recipe tuple to be atomic or compound but got {a} in {item}'
        assert isinstance(b, str), f'Expected second item in recipe tuple to be a string but got {type(b)} for {b} in {item}'
        expected_type = (list, ) if a == 'compound' else (int, float)
        assert isinstance(c, expected_type), f'Expected third item in recipe to be of type {expected_type} but got {type(c)} for {c} in {item}'

    exp = set((a, b, tuple(c) if a =='compound' else c) for a,b,c in expected)
    res = set((a, b, tuple(c) if a =='compound' else c) for a,b,c in result)
    assert res == exp, f'Found {len(res.intersection(exp))} matching recipes. Additional recipes: {len(res-exp)} \n {res-exp} \n Missing Recipes: {len(exp-res)} \n {exp-res}'


def canonize_flat_recipe(recipe):
    """
    Produce a nice immutable representation good for sorting and comparison.
    """
    if recipe is None:
        return None
    assert isinstance(recipe, dict), "Each recipe should be flat, e.g. a dictionary!"
    return frozenset(recipe.items())


def canonize_flat_recipes(recipes):
    """
    Like above, for lists of recipes
    """
    assert isinstance(recipes, list) and all(isinstance(i, dict) for i in recipes), "Recipes should be represented as a list of dictionaries!"
    return frozenset((canonize_flat_recipe(recipe) for recipe in recipes))

def _load_test(n):
    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', f'big_recipes_{n:02d}.pickle'), 'rb') as f:
        return pickle.load(f)

def _filter_graph(graph, elts):
    elts = set(elts)
    return [i for i in graph if i[1] not in elts]


def check_recipe_book(result, expected):
    assert len(result) == len(expected), "recipe books should be the same length!"
    assert isinstance(result, dict), "recipe book should be a dictionary!"

    for ing, val in expected.items():
        assert ing in result, f"missing ingredient {ing} from recipe book"
        canonical_rep = sorted(sorted(rec) for rec in val)
        canonical_res = sorted(sorted(rec) for rec in result.get(ing, []))
        assert (
            canonical_rep == canonical_res
        ), f"recipes don't match for ingredient {ing}"


def test_recipe_book_examples():
    orig = copy.deepcopy(example_recipes)

    check_recipe_book(lab.make_recipe_book(orig), {'chili': [[('beans', 3),
           ('cheese', 10),
           ('chili powder', 1),
           ('cornbread', 2),
           ('protein', 1)]],
         'cornbread': [[('cornmeal', 3),
           ('milk', 1),
           ('butter', 5),
           ('salt', 1),
           ('flour', 2)]],
         'burger': [[('bread', 2),
           ('cheese', 1),
           ('lettuce', 1),
           ('protein', 1),
           ('ketchup', 1)],
          [('bread', 2), ('cheese', 2), ('lettuce', 1), ('protein', 2)]],
         'butter': [[('milk', 1), ('butter churn', 1)]],
         'milk': [[('cow', 1), ('milking stool', 1)]],
         'cheese': [[('milk', 1), ('time', 1)], [('cutting-edge laboratory', 11)]],
         'bread': [[('yeast', 1), ('salt', 1), ('flour', 2)]],
         'protein': [[('cow', 1)]],
         'ketchup': [[('tomato', 30), ('vinegar', 5)],
          [('tomato', 30),
           ('vinegar', 3),
           ('salt', 1),
           ('sugar', 2),
           ('cinnamon', 1)]]})

    assert example_recipes == orig, "be careful not to mutate the input!"


def test_atomic_costs_examples():
    orig = copy.deepcopy(example_recipes)

    assert lab.make_atomic_costs(orig) == {
        "beans": 5,
        "cornmeal": 7.5,
        "lettuce": 2,
        "butter churn": 50,
        "salt": 1,
        "flour": 3,
        "chili powder": 1,
        "cow": 100,
        "milking stool": 5,
        "cutting-edge laboratory": 1000,
        "yeast": 2,
        "time": 10000,
        "vinegar": 20,
        "sugar": 1,
        "cinnamon": 7,
        "tomato": 13,
    }

    assert orig == example_recipes, "be careful not to mutate the input!"



def test_lowest_cost_examples_all_included():
    orig = copy.deepcopy(example_recipes)

    # atomic food items, should just return their costs
    assert lab.lowest_cost(example_recipes, 'time') == 10000
    assert lab.lowest_cost(example_recipes, 'salt') == 1
    assert abs(lab.lowest_cost(example_recipes, 'cornmeal') - 7.5) <= 1e-6

    # compound food items, only one layer deep
    assert lab.lowest_cost(example_recipes, 'protein') == 100
    assert lab.lowest_cost(example_recipes, 'milk') == 105
    assert lab.lowest_cost(example_recipes, 'bread') == 9

    # two layers
    assert lab.lowest_cost(example_recipes, 'cheese') == 10105

    # more complex
    assert lab.lowest_cost(example_recipes, 'burger') == 10685
    assert lab.lowest_cost(example_recipes, 'chili') == 102985

    assert example_recipes == orig, 'be careful not to mutate the input!'


@pytest.mark.parametrize('testnum', range(11))
def test_lowest_cost_big_all_included(testnum):
    for i in range(testnum*5, (testnum+1)*5):
        test_data = _load_test(i)
        graph = test_data['graph']
        target = test_data['target']
        orig_graph = copy.deepcopy(graph)
        result = lab.lowest_cost(graph, target)
        assert graph == orig_graph, "be careful not the change the input!"
        assert result == test_data['orig_min']


def test_lowest_cost_examples_excluded():
    graph = _filter_graph(example_recipes, ('cow',))
    orig = copy.deepcopy(graph)

    # atomic food items, should just return their costs
    assert lab.lowest_cost(graph, 'time') == 10000
    assert lab.lowest_cost(graph, 'salt') == 1
    assert abs(lab.lowest_cost(graph, 'cornmeal') - 7.5) <= 1e-6

    # compound food items, only one layer deep
    assert lab.lowest_cost(graph, 'protein') is None
    assert lab.lowest_cost(graph, 'milk') is None
    assert lab.lowest_cost(graph, 'bread') == 9

    # two layers
    assert lab.lowest_cost(graph, 'cheese') == 11000

    # more complex
    assert lab.lowest_cost(graph, 'burger') == None
    assert lab.lowest_cost(graph, 'chili') == None

    assert graph == orig, 'be careful not to mutate the input!'



def test_lowest_cost_more_examples_excluded():
    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', 'examples_filter.pickle'), 'rb') as f:
        test_data = pickle.load(f)

    for (target, filt) in test_data:
        graph = _filter_graph(example_recipes, filt)
        orig = copy.deepcopy(graph)
        result = lab.lowest_cost(graph, target)
        assert graph == orig, 'be careful not to mutate the input!'
        assert result == test_data[(target, filt)][1]


@pytest.mark.parametrize('testnum', range(11))
def test_lowest_cost_big_excluded(testnum):
    for i in range(testnum*5, (testnum+1)*5):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min']),
        ]:
            graph = _filter_graph(test_data['graph'], test_data[filt])
            orig_graph = copy.deepcopy(graph)
            result = lab.lowest_cost(graph, target)
            assert graph == orig_graph, "be careful not the change the input!"
            assert result == expected


def test_lowest_cost_examples_forbidden():
    assert lab.lowest_cost.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    orig = copy.deepcopy(example_recipes)

    # atomic food items, should just return their costs
    assert lab.lowest_cost(example_recipes, 'time', ('cow',)) == 10000
    assert lab.lowest_cost(example_recipes, 'salt', ('cow',)) == 1
    assert abs(lab.lowest_cost(example_recipes, 'cornmeal', ('cow',)) - 7.5) <= 1e-6

    # compound food items, only one layer deep
    assert lab.lowest_cost(example_recipes, 'protein', ('cow',)) is None
    assert lab.lowest_cost(example_recipes, 'milk', ('cow',)) is None
    assert lab.lowest_cost(example_recipes, 'bread', ('cow',)) == 9

    # two layers
    assert lab.lowest_cost(example_recipes, 'cheese', ('cow',)) == 11000

    # more complex
    assert lab.lowest_cost(example_recipes, 'burger', ('cow',)) == None
    assert lab.lowest_cost(example_recipes, 'chili', ('cow',)) == None

    assert example_recipes == orig, 'be careful not to mutate the input!'



def test_lowest_cost_more_examples_forbidden():
    assert lab.lowest_cost.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', 'examples_filter.pickle'), 'rb') as f:
        test_data = pickle.load(f)

    for (target, filt) in test_data:
        orig = copy.deepcopy(example_recipes)
        result = lab.lowest_cost(example_recipes, target, filt)
        assert example_recipes == orig, 'be careful not to mutate the input!'
        assert result == test_data[(target, filt)][1]


@pytest.mark.parametrize('testnum', range(11))
def test_lowest_cost_big_forbidden(testnum):
    assert lab.lowest_cost.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    for i in range(testnum*5, (testnum+1)*5):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min']),
        ]:
            graph = test_data['graph']
            orig_graph = copy.deepcopy(graph)
            result = lab.lowest_cost(graph, target, test_data[filt])
            assert graph == orig_graph, "be careful not the change the input!"
            assert result == expected


@pytest.mark.parametrize('testnum', range(5))
def test_lowest_cost_big_excluded_forbidden(testnum):
    assert lab.lowest_cost.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    for i in range(testnum*11, (testnum+1)*11):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min']),
        ]:
            graph = _filter_graph(test_data['graph'], test_data[filt][::2])
            orig_graph = copy.deepcopy(graph)
            result = lab.lowest_cost(graph, target, test_data[filt][1::2])
            assert graph == orig_graph, "be careful not the change the input!"
            assert result == expected


@pytest.mark.parametrize('scale', (0, 1, 10))
def test_scale_recipe_small(scale):
    assert lab.scale_recipe({}, scale) == {}

    recipe = {'vanilla ice cream': 3, 'chocolate chips': 6}
    recipe_copy = {'vanilla ice cream': 3, 'chocolate chips': 6}
    expected = {'vanilla ice cream': 3 * scale, 'chocolate chips': 6 * scale}

    res = lab.scale_recipe(recipe, scale)
    assert len(res) == len(recipe), f"expected recipe of length {len(recipe)}, got recipe of length {len(res)}"
    assert res == expected
    assert recipe == recipe_copy, "Be careful not to modify the input"


@pytest.mark.parametrize('scale_num', range(1,4))
def test_scale_recipe_medium(scale_num):
    scales = {1: 163, 2: 251, 3: 420}
    scale = scales[scale_num]
    recipe = {
        "beans": 5,
        "cornmeal": 7,
        "lettuce": 2,
        "butter churn": 50,
        "salt": 1,
        "flour": 3,
        "chili powder": 1,
        "cow": 100,
        "milking stool": 5,
        "cutting-edge laboratory": 1000,
        "yeast": 2,
        "time": 10000,
    }
    recipe_copy = {
        "beans": 5,
        "cornmeal": 7,
        "lettuce": 2,
        "butter churn": 50,
        "salt": 1,
        "flour": 3,
        "chili powder": 1,
        "cow": 100,
        "milking stool": 5,
        "cutting-edge laboratory": 1000,
        "yeast": 2,
        "time": 10000,
    }
    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', f'scale_recipe_medium_0{scale_num}.pickle'), 'rb') as f:
        expected = pickle.load(f)
    
    res = lab.scale_recipe(recipe, scale)
    assert len(res) == len(recipe), f"expected recipe of length {len(recipe)}, got recipe of length {len(res)}"
    assert res == expected
    assert recipe == recipe_copy, "Be careful not to modify the input"


def test_grocery_list_small():
    # two cups of coffee
    flat_recipes = [
        {'coffee': 3, 'creamer': 2},
        {'coffee': 4, 'milk': 5},
    ]
    flat_recipes2 = [
        {'coffee': 3, 'creamer': 2},
        {'coffee': 4, 'milk': 5},
    ]
    res = lab.make_grocery_list(flat_recipes)
    assert res == {
        'coffee': 7,
        'creamer': 2,
        'milk': 5,
    }
    assert flat_recipes == flat_recipes2, "Be careful not to modify the input to make_grocery_list!"

def test_grocery_list_medium():
    # coffee and donuts
    flat_recipes = [
        {'coffee': 3, 'creamer': 2},
        {'coffee': 4, 'milk': 5},
        {'milk': 2, 'dough': 8, 'sugar': 1},
        {},
        {'milk': 2, 'dough': 8, 'sugar': 1},
        {'milk': 3, 'dough': 5, 'sugar': 1},
    ]
    flat_recipes2 = [rep.copy() for rep in flat_recipes]
    res = lab.make_grocery_list(flat_recipes)
    assert res == {
        'coffee': 7,
        'creamer': 2,
        'milk': 12,
        'dough': 21,
        'sugar': 3,
    }
    assert flat_recipes == flat_recipes2,  "Be careful not to modify the input to make_grocery_list!"

@pytest.mark.parametrize('num_ingredients', (20, 100, 1000))
def test_grocery_list_random(num_ingredients):
    ingredients = [str(i) for i in range(num_ingredients)]
    max_recipes = random.randint(num_ingredients // 5, num_ingredients // 2)
    max_quantity = max_recipes * 2
    totals = {str(i): random.randint(1, max_quantity) for i in range(num_ingredients)}
    original_totals = totals.copy() 
    flat_recipes = []
    for _ in range(max_recipes-1):
        # randomly place ingredients in recipes
        unused_ingredients = [ing for ing in ingredients if totals[ing] > 0]
        if not unused_ingredients:
            break
        in_recipe = random.sample(unused_ingredients, random.randint(1, len(unused_ingredients)))
        flat_recipe = {}
        for ing in in_recipe:
            q = random.randint(0, totals[ing])
            if not q:
                continue
            flat_recipe[ing] = q 
            totals[ing] -= q

        flat_recipes.append(flat_recipe)
    else:
        flat_recipes.append({ing: total for ing, total in totals.items() if total})

    flat_recipes2 = [rep.copy() for rep in flat_recipes]
    res = lab.make_grocery_list(flat_recipes)
    assert res == original_totals
    assert flat_recipes == flat_recipes2,  "Be careful not to modify the input to make_grocery_list!"


def test_cheapest_examples_all_included():
    orig = copy.deepcopy(example_recipes)

    # atomic food items, should just return their costs
    assert lab.cheapest_flat_recipe(example_recipes, 'time') == {'time': 1}
    assert lab.cheapest_flat_recipe(example_recipes, 'salt') == {'salt': 1}

    # compound food items, only one layer deep
    assert lab.cheapest_flat_recipe(example_recipes, 'protein') == {'cow': 1}

    assert lab.cheapest_flat_recipe(example_recipes, 'milk') == {'cow': 1, 'milking stool': 1}
    assert lab.cheapest_flat_recipe(example_recipes, 'bread') == {'flour': 2, 'salt': 1, 'yeast': 1}

    # two layers
    assert lab.cheapest_flat_recipe(example_recipes, 'cheese') == {'cow': 1, 'milking stool': 1, 'time': 1}

    # more complex
    assert lab.cheapest_flat_recipe(example_recipes, 'burger') == {'yeast': 2, 'salt': 3, 'flour': 4, 'cow': 2, 'milking stool': 1, 'time': 1, 'lettuce': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1}

    assert example_recipes == orig, 'be careful not to mutate the input!'


def test_cheapest_examples_forbidden():
    assert lab.cheapest_flat_recipe.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    orig = copy.deepcopy(example_recipes)

    # atomic food items
    assert lab.cheapest_flat_recipe(example_recipes, 'time', ('time',)) is None

    # compound food items, only one layer deep
    assert lab.cheapest_flat_recipe(example_recipes, 'protein', ('cow',)) is None

    # two layers
    assert lab.cheapest_flat_recipe(example_recipes, 'cheese', ('milking stool',)) == {'cutting-edge laboratory': 11}
    assert lab.cheapest_flat_recipe(example_recipes, 'cheese', ('milking stool', 'cutting-edge laboratory')) is None

    # more complex
    assert lab.cheapest_flat_recipe(example_recipes, 'burger', ('vinegar',)) == {'yeast': 2, 'salt': 2, 'flour': 4, 'cow': 4, 'milking stool': 2, 'time': 2, 'lettuce': 1}
    assert lab.cheapest_flat_recipe(example_recipes, 'burger', ('vinegar','milk')) == {'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 22, 'lettuce': 1, 'cow': 2}

    assert example_recipes == orig, 'be careful not to mutate the input!'


@pytest.mark.parametrize('testnum', range(5))
def test_cheapest_big_all_included(testnum):
    for i in range(testnum*11, (testnum+1)*11):
        test_data = _load_test(i)
        target = test_data['target']
        graph = test_data['graph']
        orig_graph = copy.deepcopy(graph)
        result = lab.cheapest_flat_recipe(graph, target)
        assert graph == orig_graph, "be careful not the change the input!"
        assert canonize_flat_recipe(result) == canonize_flat_recipe(test_data['orig_min_recipe'])


def test_cheapest_more_examples_excluded():
    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', 'examples_filter.pickle'), 'rb') as f:
        test_data = pickle.load(f)

    for (target, filt) in test_data:
        graph = _filter_graph(example_recipes, filt)
        orig = copy.deepcopy(graph)
        result = lab.cheapest_flat_recipe(graph, target)
        assert graph == orig, 'be careful not to mutate the input!'
        assert result == test_data[(target, filt)][0]


@pytest.mark.parametrize('testnum', range(5))
def test_cheapest_big_excluded(testnum):
    for i in range(testnum*11, (testnum+1)*11):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min_recipe']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min_recipe']),
        ]:
            graph = _filter_graph(test_data['graph'], test_data[filt])
            orig_graph = copy.deepcopy(graph)
            result = lab.cheapest_flat_recipe(graph, target)
            assert graph == orig_graph, "be careful not the change the input!"
            assert canonize_flat_recipe(result) == canonize_flat_recipe(expected)


def test_cheapest_more_examples_forbidden():
    assert lab.cheapest_flat_recipe.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    with open(os.path.join(TEST_DIRECTORY, 'test_recipes', 'examples_filter.pickle'), 'rb') as f:
        test_data = pickle.load(f)

    for (target, filt) in test_data:
        orig = copy.deepcopy(example_recipes)
        result = lab.cheapest_flat_recipe(example_recipes, target, filt)
        assert example_recipes == orig, 'be careful not to mutate the input!'
        assert result == test_data[(target, filt)][0]


@pytest.mark.parametrize('testnum', range(5))
def test_cheapest_big_forbidden(testnum):
    assert lab.cheapest_flat_recipe.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    for i in range(testnum*11, (testnum+1)*11):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min_recipe']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min_recipe']),
        ]:
            graph = test_data['graph']
            orig_graph = copy.deepcopy(graph)
            result = lab.cheapest_flat_recipe(graph, target, test_data[filt])
            assert graph == orig_graph, "be careful not the change the input!"
            assert canonize_flat_recipe(result) == canonize_flat_recipe(expected)


@pytest.mark.parametrize('testnum', range(5))
def test_cheapest_big_excluded_forbidden(testnum):
    assert lab.cheapest_flat_recipe.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    for i in range(testnum*11, (testnum+1)*11):
        test_data = _load_test(i)
        target = test_data['target']
        for filt, expected in [
                ('change_filter', test_data['change_min_recipe']),
                ('none_filter', None),
                ('same_filter', test_data['orig_min_recipe']),
        ]:
            graph = _filter_graph(test_data['graph'], test_data[filt][::2])
            orig_graph = copy.deepcopy(graph)
            result = lab.cheapest_flat_recipe(graph, target, test_data[filt][1::2])
            assert graph == orig_graph, "be careful not the change the input!"
            assert canonize_flat_recipe(result) == canonize_flat_recipe(expected)


def test_ingredient_mixes_small():
    # single ingredient, single combination
    inp = [[{"a": 1, "b": 2}]]
    inp2 = [[{"a": 1, "b": 2}]]
    result = lab.ingredient_mixes(inp)

    assert inp == inp2, "Be careful not to modify the input!" 
    assert result == [{"a": 1, "b": 2}]

    # single ingredient, multiple combinations
    inp =[[{"a": 1, "b": 2}, {"c": 3}]]
    inp2 = [[{"a": 1, "b": 2}, {"c": 3}]]

    result = lab.ingredient_mixes(inp)

    assert inp == inp2, "Be careful not to modify the input!" 
    assert canonize_flat_recipes(
        result
    ) == canonize_flat_recipes(
        [
            {"a": 1, "b": 2},
            {"c": 3},
        ]
    )

    # multiple ingredients, one combination with a merge
    inp = [[{"a": 1}], [{"a": 1, "b": 2}]]
    inp2 = [[{"a": 1}], [{"a": 1, "b": 2}]]
    result = lab.ingredient_mixes(inp)

    assert inp == inp2, "Be careful not to modify the input!" 
    assert result == [{"a": 2, "b": 2}]

    # multiple ingredients, multiple combinations
    inp = [[{"a": 1}, {"a": 2}], [{"a": 4}, {"a": 8}]]
    inp2 = [[{"a": 1}, {"a": 2}], [{"a": 4}, {"a": 8}]]
    result = lab.ingredient_mixes(inp)
    assert inp == inp2, "Be careful not to modify the input!" 
    assert canonize_flat_recipes(result) == canonize_flat_recipes(
        [
            {"a": 9},
            {"a": 6},
            {"a": 10},
            {"a": 5},
        ]
    )


def test_ingredient_mixes_big():
    with open("test_recipes/ingredient_mixes.pickle", "rb") as f:
        cases = pickle.load(f)

    for title, inp, outp in cases:
        assert canonize_flat_recipes(
            lab.ingredient_mixes(inp)
        ) == canonize_flat_recipes(outp), f"failed big {title}"

def test_all_recipes_examples_all_included():
    orig = copy.deepcopy(example_recipes)

    # atomic food items, should just return their costs
    assert lab.all_flat_recipes(example_recipes, 'time') == [{'time': 1}]
    assert lab.all_flat_recipes(example_recipes, 'salt') == [{'salt': 1}]

    # compound food items, only one layer deep
    assert lab.all_flat_recipes(example_recipes, 'protein') == [{'cow': 1}]

    assert lab.all_flat_recipes(example_recipes, 'milk') == [{'cow': 1, 'milking stool': 1}]
    assert lab.all_flat_recipes(example_recipes, 'bread') == [{'flour': 2, 'salt': 1, 'yeast': 1}]

    # two layers
    assert canonize_flat_recipes(lab.all_flat_recipes(example_recipes, 'cheese')) == canonize_flat_recipes([{'cow': 1, 'milking stool': 1, 'time': 1}, {'cutting-edge laboratory': 11}])

    # more complex
    burgers = [
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cow': 4, 'milking stool': 2, 'time': 2, 'lettuce': 1},
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 22, 'lettuce': 1, 'cow': 2},
        {'yeast': 2, 'salt': 3, 'flour': 4, 'cow': 2, 'milking stool': 1, 'time': 1, 'lettuce': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1},
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cow': 2, 'milking stool': 1, 'time': 1, 'lettuce': 1, 'tomato': 30, 'vinegar': 5},
        {'yeast': 2, 'salt': 3, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1},
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 5}
    ]

    assert canonize_flat_recipes(lab.all_flat_recipes(example_recipes, 'burger')) == canonize_flat_recipes(burgers)

    assert example_recipes == orig, 'be careful not to mutate the input!'

def test_all_recipes_examples_forbidden():
    assert lab.all_flat_recipes.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    orig = copy.deepcopy(example_recipes)

    # atomic food items
    assert lab.all_flat_recipes(example_recipes, 'salt', ('salt',)) == []

    # compound food items, only one layer deep
    assert lab.all_flat_recipes(example_recipes, 'protein', ('cow',)) == []

    # two layers
    assert lab.all_flat_recipes(example_recipes, 'cheese', ('milking stool',)) == [{'cutting-edge laboratory': 11}]
    assert lab.all_flat_recipes(example_recipes, 'cheese', ('milking stool', 'cutting-edge laboratory')) == []

    burgers2 = [
        {'yeast': 2, 'salt': 3, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 3, 'sugar': 2, 'cinnamon': 1},
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 11, 'lettuce': 1, 'cow': 1, 'tomato': 30, 'vinegar': 5},
        {'yeast': 2, 'salt': 2, 'flour': 4, 'cutting-edge laboratory': 22, 'lettuce': 1, 'cow': 2}
    ]
    assert canonize_flat_recipes(lab.all_flat_recipes(example_recipes, 'burger', ('milk',))) == canonize_flat_recipes(burgers2)

    assert example_recipes == orig, 'be careful not to mutate the input!'


@pytest.mark.parametrize('testnum', range(11))
def test_all_recipes_big(testnum):
    assert lab.all_flat_recipes.__defaults__ is not None, "Make sure that forbidden items are an optional agument!"

    for i in range(testnum*5, (testnum+1)*5):
        test_data = _load_test(i)
        target = test_data['target']
        test_data['identity_filter'] = ()
        for filt, expected in [
                ('identity_filter', test_data['orig_all']),
                ('change_filter', test_data['change_all']),
                ('none_filter', []),
                ('same_filter', test_data['same_all']),
        ]:
            for graph, filter_ in [(_filter_graph(test_data['graph'], test_data[filt]), ()),
                                   (test_data['graph'], test_data[filt]),
                                   (_filter_graph(test_data['graph'], test_data[filt][1::2]), test_data[filt][::2])]:
                orig_graph = copy.deepcopy(graph)
                result = lab.all_flat_recipes(graph, target, filter_)
                #print(result)
                assert graph == orig_graph, "be careful not the change the input!"
                assert canonize_flat_recipes(result) == canonize_flat_recipes(expected)



if __name__ == "__main__":
    import sys
    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
