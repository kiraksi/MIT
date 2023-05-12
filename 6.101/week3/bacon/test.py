#!/usr/bin/env python3
import os
import lab
import sys
import pickle
import random

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


def setup_module(module):
    """
    This function loads the various databases.  It will be run once every time
    test.py is invoked.
    """
    for i in ("tiny", "small", "large"):
        filename = os.path.join(TEST_DIRECTORY, "resources", f"{i}.pickle")
        with open(filename, "rb") as f:
            raw = pickle.load(f)
            setattr(module, f"raw_db_{i}", raw)
            setattr(module, f"db_{i}", lab.transform_data(raw))
            setattr(module, f"fset_{i}", {frozenset(i[:-1]) for i in raw})


def test_acted_together_01():
    # Simple test, two actors who acted together
    actor1 = 4724
    actor2 = 9210
    assert lab.acted_together(db_small, actor1, actor2) is True


def test_acted_together_02():
    # Simple test, two actors who had not acted together
    actor1 = 4724
    actor2 = 16935
    assert lab.acted_together(db_small, actor1, actor2) is False


def test_acted_together_03():
    # Simple test, same actor
    actor1 = 4724
    actor2 = 4724
    assert lab.acted_together(db_small, actor1, actor2) is True


def _run_pickled_together_test(n):
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "acted_together_%02d.pickle" % n,
    )
    with open(filename, "rb") as f:
        tests = pickle.load(f)
    for a1, a2, v in tests:
        res = lab.acted_together(db_large, a1, a2)
        assert (
            res == v and isinstance(res, bool)
        ), f"expected {bool(v)} for {a1} and {a2} acting together, got {res}"


@pytest.mark.parametrize("test_num", [0, 1])
def test_acted_together_additional(test_num):
    _run_pickled_together_test(test_num)


def test_bacon_number_01():
    # Actors with Bacon number of 2
    n = 2
    expected = {1640, 1811, 2115, 2283, 2561, 2878, 3085, 4025, 4252, 4765,
                6541, 9827, 11317, 14104, 16927, 16935, 19225, 33668, 66785,
                90659, 183201, 550521, 1059002, 1059003, 1059004, 1059005,
                1059006, 1059007, 1232763}

    first_result = lab.actors_with_bacon_number(db_small, n)
    assert isinstance(first_result, set)
    assert first_result == expected

    second_result = lab.actors_with_bacon_number(db_small, n)
    assert isinstance(second_result, set)
    assert second_result == expected


def test_bacon_number_02():
    # Actors with Bacon number of 3
    n = 3
    expected = {52, 1004, 1248, 2231, 2884, 4887, 8979, 10500, 12521,
                14792, 14886, 15412, 16937, 17488, 19119, 19207, 19363,
                20853, 25972, 27440, 37252, 37612, 38351, 44712, 46866,
                46867, 48576, 60062, 75429, 83390, 85096, 93138, 94976,
                109625, 113777, 122599, 126471, 136921, 141458, 141459,
                141460, 141461, 141495, 146634, 168638, 314092, 349956,
                558335, 572598, 572599, 572600, 572601, 572602, 572603,
                583590, 931399, 933600, 1086299, 1086300, 1168416, 1184797,
                1190297, 1190298, 1190299, 1190300}

    first_result = lab.actors_with_bacon_number(db_small, n)
    assert isinstance(first_result, set)
    assert first_result == expected

    second_result = lab.actors_with_bacon_number(db_small, n)
    assert isinstance(second_result, set)
    assert second_result == expected


def test_bacon_number_03():
    # random large Bacon number
    N = random.randint(50, 100)
    k = random.randint(7, 30)
    assert (
        len(lab.actors_with_bacon_number(lab.transform_data(make_bacon_tree(N, k)), N))
        == k
    )


def test_bacon_number_04():
    # random graph, Bacon number with no people
    N = random.randint(5, 10)
    k = random.randint(4, 7)
    assert len(lab.actors_with_bacon_number(lab.transform_data(make_bacon_tree(N, k)), 10**20)) == 0
    assert len(lab.actors_with_bacon_number(lab.transform_data(make_bacon_tree(N, k)), 10**20)) == 0


def test_bacon_path_01():
    # Bacon path, small database, path does not exist
    actor_id = 2876669
    expected = None

    first_result = lab.bacon_path(db_small, actor_id)
    assert first_result == expected

    second_result = lab.bacon_path(db_small, actor_id)
    assert second_result == expected


def test_bacon_path_02():
    # Bacon path, small database, length of 3 (4 actors, 3 movies)
    actor_id = 46866
    len_expected = 3

    first_result = lab.bacon_path(db_small, actor_id)
    second_result = lab.bacon_path(db_small, actor_id)

    check_valid_path(fset_small, first_result, 4724, actor_id, len_expected)
    check_valid_path(fset_small, second_result, 4724, actor_id, len_expected)


def test_bacon_path_03():
    # Bacon path, large database, length of 2 (3 actors, 2 movies)
    actor_id = 1204
    len_expected = 2
    result = lab.bacon_path(db_large, actor_id)

    check_valid_path(fset_large, result, 4724, actor_id, len_expected)


def test_bacon_path_04():
    # Bacon path, large database, length of 4 (5 actors, 4 movies)
    actor_id = 197897
    len_expected = 4
    result = lab.bacon_path(db_large, actor_id)

    check_valid_path(fset_large, result, 4724, actor_id, len_expected)


def test_bacon_path_05():
    # Bacon path, large database, length of 6 (7 actors, 6 movies)
    actor_id = 1345462
    len_expected = 6
    result = lab.bacon_path(db_large, actor_id)
    # here, we compute the result twice, to test for mutation of the db
    result = lab.bacon_path(db_large, actor_id)
    len_result = -1 if result is None else len(result) - 1

    check_valid_path(fset_large, result, 4724, actor_id, len_expected)


def test_bacon_path_06():
    # Bacon path, large database, does not exist
    actor_id = 1204555
    expected = None
    result = lab.bacon_path(db_large, actor_id)
    assert result == expected


def test_actor_to_actor_path_01():
    # Actor path, large database, length of 7 (8 actors, 7 movies)
    actor_1 = 1345462
    actor_2 = 89614
    len_expected = 7

    first_result = lab.actor_to_actor_path(db_large, actor_1, actor_2)
    second_result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    check_valid_path(fset_large, first_result, actor_1, actor_2, len_expected)
    check_valid_path(fset_large, second_result, actor_1, actor_2, len_expected)


def test_actor_to_actor_path_02():
    # Actor path, large database, length of 4 (5 actors, 4 movies)
    actor_1 = 100414
    actor_2 = 57082
    len_expected = 4

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)
    check_valid_path(fset_large, result, actor_1, actor_2, len_expected)


def test_actor_to_actor_path_03():
    # Bacon path, large database, length of 7 (8 actors, 7 movies)
    actor_1 = 43011
    actor_2 = 1379833
    len_expected = 7

    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)
    check_valid_path(fset_large, result, actor_1, actor_2, len_expected)


def test_actor_to_actor_path_04():
    # Bacon path, large database, does not exist
    actor_1 = 43011
    actor_2 = 1204555
    result = lab.actor_to_actor_path(db_large, actor_1, actor_2)

    assert result is None


def test_actor_to_actor_path_05():
    # actor path that exists
    x = 1372398
    y = 62597
    p = lab.actor_to_actor_path(db_large, x, y)
    e = [1372398, 7056, 4566, 540, 100567, 62597]

    check_valid_path(fset_large, p, x, y, len(e) - 1)


def test_actor_to_actor_path_06():
    # actor path that exists
    e = [184581, 27111, 11086, 170882]
    x = e[0]
    y = e[-1]
    p = lab.actor_to_actor_path(db_large, x, y)
    check_valid_path(fset_large, p, x, y, len(e) - 1)


def test_actor_to_actor_path_07():
    # actor path that exists
    e = list(range(700))
    random.shuffle(e)
    data = [(i, j, 0) for i, j in zip(e, e[1:])]
    random.shuffle(data)
    x = e[0]
    y = e[-1]
    p = lab.actor_to_actor_path(lab.transform_data(data), x, y)
    check_valid_path({frozenset(i[:-1]) for i in data}, p, x, y, len(e) - 1)


def test_actor_to_actor_path_08():
    x = 1234567890
    y = 1234567898
    data = raw_db_large[:]
    data.append((x, y, 0))
    p = lab.actor_to_actor_path(lab.transform_data(data), 4724, y)
    assert p is None


def _run_pickled_a2a_path_test(n):
    filename = os.path.join(
        TEST_DIRECTORY,
        "resources",
        "tests",
        "actor_to_actor_path_%02d.pickle" % n,
    )
    with open(filename, "rb") as f:
        tests = pickle.load(f)
    for a1, a2, l in tests:
        path = lab.actor_to_actor_path(db_large, a1, a2)
        check_valid_path(fset_large, path, a1, a2, l)


@pytest.mark.parametrize("test_num", [0, 1, 2, 3, 4])
def test_actor_to_actor_path_additional(test_num):
    _run_pickled_a2a_path_test(test_num)


def test_actor_path_01():
    result = lab.actor_path(db_large, 975260, lambda p: False)
    assert result is None


def test_actor_path_02():
    result = lab.actor_path(db_large, 975260, lambda p: True)
    result2 = lab.actor_path(db_large, 975260, lambda p: p == 975260)
    assert result == result2 == [975260]


def test_actor_path_03():
    ppl = {536472, 44795, 240045, 19534}
    result1 = lab.actor_path(db_large, 10526, lambda p: p in ppl)
    check_valid_path(fset_large, result1, 10526, 19534, 3)

    result2 = lab.actor_path(db_large, 10526, lambda p: p in ppl and p > 19534)
    check_valid_path(fset_large, result1, 10526, None, 3)
    assert result2[-1] in {536472, 44795}


def test_actor_path_04():
    result = lab.actor_path(db_large, 152597, lambda p: p in {129507, 1400266, 1355798})
    check_valid_path(fset_large, result, 152597, None, 6)
    assert result[-1] in {1400266, 1355798}


def test_actor_path_05():
    result = lab.actor_path(db_large, 26473, lambda p: p in {105656, 118946})
    check_valid_path(fset_large, result, 26473, 118946, 1)


def test_actor_path_06():
    result = lab.actor_path(db_large, 129507, lambda p: p == 152597)
    check_valid_path(fset_large, result, 129507, 152597, 7)


def test_movie_path_01():
    check_connected_movie_path(18860, 75181, 1)


def test_movie_path_02():
    check_connected_movie_path(142416, 44521, 4)


def random_number_list(L, i=1):
    o = list(range(i * 100000, i * 100000 + L))
    random.shuffle(o)
    return o


def check_valid_path(f, p, s, e, l):
    '''
    f : a set of frozenset actor pairs present in the data base
    p : result path found using lab function
    s : start actor
    e : end actor
    l : length of expected path - 1 
    '''
    lp = len(p) if p is not None else None
    assert lp == l+1, f"expected a path of length {l+1} between {s} and {e}, got {lp}"
    assert s is None or p[0] == s, f"path does not start with {s}"
    assert e is None or p[-1] == e, f"path does not end with {e}"
    assert all(frozenset(i) in f for i in zip(p, p[1:])), f"invalid path returned"


def check_connected_movie_path(m1, m2, expected_length):
    m1a = set()
    m2a = set()
    for a, b, c in raw_db_large:
        if c == m1:
            s = m1a
        elif c == m2:
            s = m2a
        else:
            continue
        s.add(a)
        s.add(b)
    result = lab.actors_connecting_films(db_large, m1, m2)
    assert result[0] in m1a
    assert result[-1] in m2a
    check_valid_path(fset_large, result, None, None, expected_length)


def make_bacon_tree(L, n=10):
    id_set = 2
    path = [4724] + random_number_list(L, i=1)
    n -= 1
    out = set((i, j) for i, j in zip(path, path[1:]))
    while n > 0:
        point = random.choice(range(len(path) - 1))
        d = L - point
        if d == 0:
            continue
        newpath = random_number_list(d, i=id_set)
        p = [path[point]] + newpath
        out |= set((i, j) for i, j in zip(p, p[1:]))
        id_set += 1
        n -= 1
    return [(i, j, 0) for i, j in out]


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
