"""
6.1010 Spring '23 Lab 9: Autocomplete
"""

#!/usr/bin/env python3
import os.path
import lab
import json
import types
import pickle

import sys
sys.setrecursionlimit(10000)

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


# convert prefix tree into a dictionary...
def dictify(t):
    assert set(t.__dict__) == {'value', 'children'}, "PrefixTree instances should only contain the two instance attributes mentioned in the lab writeup."
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out

# ...and back
def from_dict(d):
    t = lab.PrefixTree()
    for k, v in d.items():
        t[k] = v
    return t

# make sure the keys are not explicitly stored in any node
def any_key_stored(tree, keys):
    keys = [tuple(k) for k in keys]
    for i in dir(tree):
        try:
            val = tuple(getattr(tree, i))
        except:
            continue
        for j in keys:
            if j == val:
                return repr(i), repr(j)
    for child in tree.children:
        if len(child) != 1:
            return repr(child), repr(child)
    for child in tree.children.values():
        key_stored = any_key_stored(child, keys)
        if key_stored:
            return key_stored
    return None

# read in expected result
def read_expected(fname):
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', fname), 'rb') as f:
        return pickle.load(f)

def test_set():
    t = lab.PrefixTree()
    t['cat'] = 'kitten'
    t['car'] = 'tricycle'
    t['carpet'] = 'rug'
    expect = read_expected('1.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('cat', 'car', 'carpet')) is None

    t = lab.PrefixTree()
    t['a'] = 1
    t['an'] = 1
    t['ant'] = 0
    t['anteater'] = 1
    t['ants'] = 1
    t['a'] = 2
    t['an'] = 2
    t['a'] = 3
    expect = read_expected('2.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('an', 'ant', 'anteater', 'ants')) is None
    with pytest.raises(TypeError):
        t[(1, 2, 3)] = 20

    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    expect = read_expected('3.pickle')
    assert dictify(t) == expect, "Your prefix tree is incorrect."
    assert any_key_stored(t, ('man', 'mat', 'mattress', 'map', 'me', 'met', 'map')) is None
    with pytest.raises(TypeError):
        t['something',] = 'pam'


def test_get():
    d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39, 'children': 0}
    t = from_dict(d)
    assert dictify(t) == read_expected('person.pickle')
    assert all(t[k] == d[k] for k in d)
    assert any_key_stored(t, tuple(d)) is None

    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    assert all(t[k] == c[k] for k in c)
    assert any_key_stored(t, tuple(c)) is None
    for i in ('these', 'keys', 'dont', 'exist'):
        with pytest.raises(KeyError):
            x = t[i]
    with pytest.raises(TypeError):
        x = t[(1, 2, 3)]


def test_contains():
    d = {'name': 'John', 'favorite_numbers': [2, 4, 3], 'age': 39, 'children': 0}
    t = from_dict(d)
    assert dictify(t) == read_expected('person.pickle')
    assert all(i in t for i in d)
    with pytest.raises(TypeError):
        (1, 2, 3) in t

    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    assert all(i in t for i in c)
    badkeys = ('these', 'keys', 'dont', 'exist', 'm', 'ma', 'mak', 'mo',
               'mod', 'mode', 'ye', 'yea', 'y', '', 'car.pickle')
    assert all(i not in t for i in badkeys)


def test_iter():
    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    expected = [('a', '?'), ('man', ''), ('map', -1000), ('mat', 'object'),
                ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected


def test_delete():
    c = {'make': 'Toyota', 'model': 'Corolla', 'year': 2006, 'color': 'beige', 'storage space': ''}
    t = from_dict(c)
    assert dictify(t) == read_expected('car.pickle')
    del t['color']
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    with pytest.raises(KeyError):
        del t['color'] # can't delete again
    assert set(t) == set(c.items()) - {('color', 'beige')}
    t['color'] = 'silver'  # new paint job
    for i in t:
        if i[0] != 'color':
            assert i in c.items()
        else:
            assert i[1] == 'silver'

    for i in ('cat', 'dog', 'ferret', 'tomato'):
        with pytest.raises(KeyError):
            del t[i]

    with pytest.raises(TypeError):
        del t[1,2,3]

    t = lab.PrefixTree()
    t['man'] = ''
    t['mat'] = 'object'
    t['mattress'] = ()
    t['map'] = 'pam'
    t['me'] = 'you'
    t['met'] = 'tem'
    t['a'] = '?'
    t['map'] = -1000
    assert isinstance(iter(t), types.GeneratorType), "__iter__ must produce a generator"
    expected = [('a', '?'), ('man', ''), ('map', -1000), ('mat', 'object'),
                ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected
    del t['mat']
    expected = [('a', '?'), ('man', ''), ('map', -1000),
                ('mattress', ()), ('me', 'you'), ('met', 'tem')]
    assert sorted(list(t)) == expected


def test_word_frequencies():
    # small test
    l = lab.word_frequencies('toonces was a cat who could drive a car very fast until he crashed.')
    assert dictify(l) == read_expected('6.pickle')

    l = lab.word_frequencies('a man at the market murmered that he had met a mermaid. '
                           'mark didnt believe the man had met a mermaid.')
    assert dictify(l) == read_expected('7.pickle')

    l = lab.word_frequencies('what happened to the cat who had eaten the ball of yarn?  she had mittens!')
    assert dictify(l) == read_expected('8.pickle')



@pytest.mark.parametrize('bigtext', ['holmes', 'earnest', 'frankenstein'])
def test_big_corpora(bigtext):
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', '%s.txt' % bigtext), encoding='utf-8') as f:
        text = f.read()
        w = lab.word_frequencies(text)

        w_e = read_expected('%s_words.pickle' % bigtext)

        assert w_e == dictify(w), 'word frequencies prefix tree does not match for %s' % bigtext


def test_autocomplete_small():
    # Autocomplete on simple prefix trees with less than N valid words
    t = lab.word_frequencies("cat car carpet")
    result = lab.autocomplete(t, 'car', 3)
    assert set(result) == {"car", "carpet"}

    t = lab.word_frequencies("a an ant anteater a an ant a")
    result = lab.autocomplete(t, 'a', 2)
    assert set(result) in [{"a", "an"}, {"a", "ant"}]

    t = lab.word_frequencies("man mat mattress map me met a man a a a map man met")
    result = lab.autocomplete(t, 'm', 3)
    assert set(result) == {"man", "map", "met"}

    t = lab.word_frequencies("hello hell history")
    result = lab.autocomplete(t, 'help', 3)
    assert result == []
    with pytest.raises(TypeError):
        result = lab.autocomplete(t, ('tuple', ), None)


def test_autocomplete_big_1():
    alphabet = a = "abcdefghijklmnopqrstuvwxyz"

    word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
    word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
    word_list.append("bruteforceisbad")

    t = lab.word_frequencies(' '.join(word_list))
    for i in range(50_000):
        result1 = lab.autocomplete(t, 'ap', 1)
        result2 = lab.autocomplete(t, 'ap', 2)
        result3 = lab.autocomplete(t, 'ap', 3)
        result4 = lab.autocomplete(t, 'ap')
        result5 = lab.autocomplete(t, 'b')

        assert set(result1) == {'apple'}
        assert set(result2) == {'apple', 'apricot'}
        assert set(result4) == set(result3) == {'apple', 'apricot', 'application'}
        assert set(result5) == {'bruteforceisbad'}


def test_autocomplete_big_2():
    nums = {'t': [0, 1, 25, None],
            'th': [0, 1, 21, None],
            'the': [0, 5, 21, None],
            'thes': [0, 1, 21, None]}
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    w = lab.word_frequencies(text)
    for i in sorted(nums):
        for n in nums[i]:
            result = lab.autocomplete(w, i, n)
            expected = read_expected('frank_autocomplete_%s_%s.pickle' % (i, n))
            assert len(expected) == len(result), ('missing' if len(result) < len(expected) else 'too many') + ' autocomplete results for ' + repr(i) + ' with maxcount = ' + str(n)
            assert set(expected) == set(result), 'autocomplete included ' + repr(set(result) - set(expected)) + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(i) + ' with maxcount = '+str(n)
    with pytest.raises(TypeError):
        result = lab.autocomplete(w, ('tuple', ), None)


def test_autocomplete_big_3():
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    w = lab.word_frequencies(text)
    the_word = 'accompany'
    for ix in range(len(the_word)+1):
        test = the_word[:ix]
        result = lab.autocomplete(w, test)
        expected = read_expected('frank_autocomplete_%s_%s.pickle' % (test, None))
        assert len(expected) == len(result), ('missing' if len(result) < len(expected) else 'too many') + ' autocomplete results for ' + repr(test) + ' with maxcount = ' + str(None)
        assert set(expected) == set(result), 'autocomplete included ' + repr(set(result) - set(expected)) + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(test) + ' with maxcount = '+str(None)
    with pytest.raises(TypeError):
        result = lab.autocomplete(w, ('tuple', ), None)


def test_autocorrect_small():
    # Autocorrect on cat in small corpus
    t = lab.word_frequencies("cats cattle hat car act at chat crate act car act")
    result = lab.autocorrect(t, 'cat',4)
    assert set(result) == {"act", "car", "cats", "cattle"}

def test_autocorrect_big():
    nums = {'thin': [0, 8, 10, None],
            'tom': [0, 2, 4, None],
            'mon': [0, 2, 15, 17, 20, None]}
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    w = lab.word_frequencies(text)
    for i in sorted(nums):
        for n in nums[i]:
            result = lab.autocorrect(w, i, n)
            expected = read_expected('frank_autocorrect_%s_%s.pickle' % (i, n))
            assert len(expected) == len(result), ('missing' if len(result) < len(expected) else 'too many') + ' autocorrect results for ' + repr(i) + ' with maxcount = ' + str(n)
            assert set(expected) == set(result), 'autocorrect included ' + repr(set(result) - set(expected)) + ' instead of ' + repr(set(expected) - set(result)) + ' for ' + repr(i) + ' with maxcount = '+str(n)


def test_filter_small():
    # Filter to select all words in prefix tree
    t = lab.word_frequencies("man mat mattress map me met a man a a a map man met")
    result = lab.word_filter(t, '*')
    assert isinstance(result, list)
    result.sort()
    assert result == [("a", 4), ("man", 3), ("map", 2), ("mat", 1), ("mattress", 1), ("me", 1), ("met", 2)]

    # All three-letter words
    result = lab.word_filter(t, '???')
    assert isinstance(result, list)
    result.sort()
    assert result == [("man", 3), ("map", 2), ("mat", 1), ("met", 2)]

    # Words beginning with 'mat'
    result = lab.word_filter(t, 'mat*')
    assert isinstance(result, list)
    result.sort()
    assert result == [("mat", 1), ("mattress", 1)]

    # Words beginning with 'm', third letter is t
    result = lab.word_filter(t, 'm?t*')
    assert isinstance(result, list)
    result.sort()
    assert result == [("mat", 1), ("mattress", 1), ("met", 2)]

    # Words with at least 4 letters
    result = lab.word_filter(t, '*????')
    assert isinstance(result, list)
    result.sort()
    assert result == [("mattress", 1)]

    # All words
    result = lab.word_filter(t, '**')
    assert isinstance(result, list)
    result.sort()
    assert result == [("a", 4), ("man", 3), ("map", 2), ("mat", 1), ("mattress", 1), ("me", 1), ("met", 2)]


def test_filter_big_1():
    alphabet = a = "abcdefghijklmnopqrstuvwxyz"

    word_list = ["aa" + l1 + l2 + l3 + l4 for l1 in a for l2 in a for l3 in a for l4 in a]
    word_list.extend(["apple", "application", "apple", "apricot", "apricot", "apple"])
    word_list.append("bruteforceisbad")

    t = lab.word_frequencies(' '.join(word_list))
    for i in range(1000):
        result = lab.word_filter(t, "ap*")
        expected = {('apple', 3), ('apricot', 2), ('application', 1)}
        assert len(expected) == len(result), 'incorrect word_filter of ap*'
        assert set(expected) == set(result), 'incorrect word_filter of ap*'


def test_filter_big_2():
    patterns = ('*ing', '*ing?', '****ing', '**ing**', '????', 'mon*',
                '*?*?*?*', '*???')
    with open(os.path.join(TEST_DIRECTORY, 'testing_data', 'frankenstein.txt'), encoding='utf-8') as f:
        text = f.read()
    w = lab.word_frequencies(text)
    for ix, i in enumerate(patterns):
        result = lab.word_filter(w, i)
        expected = read_expected('frank_filter_%s.pickle' % (ix, ))
        assert len(expected) == len(result), 'incorrect word_filter of %r' % i
        assert set(expected) == set(result), 'incorrect word_filter of %r' % i


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
