"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3
import os
import lab
import json
import copy

import pytest

import sys

sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.join(os.path.dirname(__file__), "test_inputs")

## HELPER FUNCTIONS


def _open_case(casename):
    with open(os.path.join(TEST_DIRECTORY, casename + ".json")) as f:
        cnf = json.load(f)
        res = [
            [(variable, polarity) for variable, polarity in clause] for clause in cnf
        ]
        rev = [
            [(variable, polarity) for variable, polarity in clause[::-1]]
            for clause in cnf
        ]
        rev_f = sorted(rev)
        s_f = res[::-1]
        s_f_2 = sorted(res, key=len)
        return res, rev, rev_f, s_f, s_f_2


def _satisfiable(cnf):
    assignment = lab.satisfying_assignment(copy.deepcopy(cnf))
    assert all(
        any(
            variable in assignment and assignment[variable] == polarity
            for variable, polarity in clause
        )
        for clause in cnf
    ), f"Invalid assignment found: {assignment}"


def check_well_formed_literal(literal):
    assert isinstance(literal, (list, tuple))
    assert len(literal) == 2
    assert isinstance(literal[1], bool)


def check_well_formed_clause(clause):
    assert isinstance(clause, (list, tuple))
    for literal in clause:
        check_well_formed_literal(literal)


def check_well_formed_formula(cnf):
    assert isinstance(cnf, (list, tuple))
    for clause in cnf:
        check_well_formed_clause(clause)


def _unsatisfiable(cnf):
    assignment = lab.satisfying_assignment(copy.deepcopy(cnf))
    assert assignment is None, f"Expected None but got {assignment}"


def _test_from_file(casename, testfunc):
    for cnf in _open_case(casename):
        testfunc(cnf)


## TESTS FOR SAT SOLVER


def test_sat_small_nested_backtrack():
    cnf = [
        [("a", True), ("b", True)],
        [("a", False), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [("b", True), ("c", False)],
    ]
    _satisfiable(cnf)


def test_sat_small_double_backtrack():
    # a will be guessed as True, which is wrong
    # then a both assignments on b will fail and cause a backtrack to a
    cnf = [
        [("a", True), ("b", True)],
        [("a", False), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [("b", True), ("c", False)],
        [("a", False), ("b", False), ("c", False)],
    ]
    _satisfiable(cnf)


def test_sat_small_deep_double_backtrack():
    # a will be guessed as True, which is wrong
    # then a both assignments on b will fail and cause a backtrack to a
    cnf = [
        [("d", True), ("b", True)],
        [("a", True), ("b", True)],
        [("a", False), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [("b", True), ("c", False)],
        [("a", False), ("b", False), ("c", False)],
    ]
    _satisfiable(cnf)


def test_sat_small_deep_double_backtrack2():
    cnf = [
        [("d", True), ("b", True)],
        [("a", False), ("b", True)],
        [("a", True), ("b", False), ("c", True)],
        [("b", True), ("c", True)],
        [("b", True), ("c", False)],
        [("a", True), ("b", False), ("c", False)],
    ]
    _satisfiable(cnf)


def test_sat_big_A():
    _test_from_file("A", _satisfiable)


def test_sat_big_B():
    _test_from_file("B", _satisfiable)


def test_sat_big_C():
    _test_from_file("C", _satisfiable)  # irrelevancies


def test_sat_big_D():
    _test_from_file("D", _unsatisfiable)


def test_sat_big_E():
    _test_from_file("E", _satisfiable)


def test_sat_big_F():
    _test_from_file("F", _unsatisfiable)


def test_sat_big_G():
    _test_from_file("G", _satisfiable)


def test_sat_big_H():
    _test_from_file("H", _unsatisfiable)


def test_sat_big_I():
    _test_from_file("I", _satisfiable)


def test_sat_big_J():
    _test_from_file("J", _unsatisfiable)


def test_sat_big_K():
    _test_from_file("K", _satisfiable)


def test_sat_big_L():
    _test_from_file("L", _satisfiable)


def _test_sudoku(start, expect_none=False):
    original = [list(r) for r in start]
    sat_formula = lab.sudoku_board_to_sat_formula(start)
    assert start == original
    check_well_formed_formula(sat_formula)
    assignments = lab.satisfying_assignment(sat_formula)
    result = lab.assignments_to_sudoku_board(assignments, len(original))
    assert start == original
    check_sudoku(original, result, expect_none)


def test_sat_smalldoku_0():
    grid = [
        [0, 0, 0, 2],
        [0, 0, 0, 1],
        [4, 0, 0, 0],
        [2, 0, 0, 0],
    ]
    _test_sudoku(grid)


def test_sat_smalldoku_1():
    grid = [
        [1, 0, 0, 0],
        [0, 0, 0, 4],
        [3, 0, 0, 0],
        [0, 0, 0, 2],
    ]
    _test_sudoku(grid)


def test_sat_smalldoku_2():
    grid = [
        [1, 0, 0, 0],
        [0, 0, 0, 4],
        [3, 0, 0, 0],
        [0, 0, 1, 2],
    ]
    _test_sudoku(grid, expect_none=True)


def test_sat_smalldoku_3():
    grid = [
        [1, 0, 0, 0],
        [0, 0, 0, 4],
        [3, 0, 0, 0],
        [0, 0, 1, 2],
    ]
    _test_sudoku(grid, expect_none=True)


def test_sat_smalldoku_4():
    grid = [
        [1, 0, 3, 4],
        [2, 3, 0, 0],
        [3, 4, 1, 0],
        [0, 1, 2, 3],
    ]
    _test_sudoku(grid, expect_none=True)


def test_sat_sudoku_0():
    grid0 = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    _test_sudoku(grid0)


def test_sat_sudoku_1():
    grid1 = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [2, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 4, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 2, 0, 0, 0, 0, 1, 0],
        [0, 3, 8, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    _test_sudoku(grid1)


def test_sat_sudoku_2():
    grid2 = [
        [5, 1, 7, 6, 0, 0, 0, 3, 4],
        [0, 8, 9, 0, 0, 4, 0, 0, 0],
        [3, 0, 6, 2, 0, 5, 0, 9, 0],
        [6, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 3, 0, 0, 0, 6, 0, 4, 7],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 0, 7, 8],
        [7, 0, 3, 4, 0, 0, 5, 6, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    _test_sudoku(grid2)


def test_sat_sudoku_3():
    grid3 = [
        [0, 0, 1, 0, 0, 9, 0, 0, 3],
        [0, 8, 0, 0, 2, 0, 0, 9, 0],
        [9, 0, 0, 1, 0, 0, 8, 0, 0],
        [1, 0, 0, 5, 0, 0, 4, 0, 0],
        [0, 7, 0, 0, 3, 0, 0, 5, 0],
        [0, 0, 6, 0, 0, 4, 0, 0, 7],
        [0, 0, 8, 0, 0, 5, 0, 0, 6],
        [0, 3, 0, 0, 7, 0, 0, 4, 0],
        [2, 0, 0, 3, 0, 0, 9, 0, 0],
    ]
    _test_sudoku(grid3)


def test_sat_sudoku_4():
    grid4 = [
        [1, 0, 0, 0, 6, 0, 0, 0, 9],
        [0, 9, 0, 1, 0, 5, 0, 8, 0],
        [0, 0, 7, 0, 8, 0, 3, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 6, 0],
        [4, 0, 5, 0, 0, 0, 8, 0, 3],
        [0, 1, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 9, 0, 3, 0, 1, 0, 0],
        [0, 6, 0, 2, 0, 9, 0, 3, 0],
        [2, 0, 0, 0, 7, 0, 0, 0, 5],
    ]
    _test_sudoku(grid4)


def test_sat_sudoku_5():
    grid5 = [
        [5, 0, 1, 8, 0, 3, 7, 0, 2],  # http://www.extremesudoku.info/sudoku.html
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 0, 0, 2, 0, 5, 0, 0, 8],
        [6, 0, 2, 0, 0, 0, 4, 0, 7],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [1, 0, 7, 0, 0, 0, 9, 0, 5],
        [8, 0, 0, 9, 0, 2, 0, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 9, 5, 0, 7, 6, 0, 1],
    ]
    _test_sudoku(grid5)


def test_sat_sudoku_6():
    grid6 = [
        [0, 8, 0, 0, 0, 0, 0, 9, 0],  # https://sudoku.com/expert/
        [0, 1, 0, 0, 8, 6, 3, 0, 2],
        [0, 0, 0, 3, 1, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 2, 6, 1, 0, 0, 4],
        [0, 0, 0, 5, 4, 0, 0, 0, 6],
        [3, 0, 9, 0, 0, 0, 8, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    _test_sudoku(grid6)


def test_sat_sudoku_7():
    grid7 = [
        [0, 0, 0, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 5, 6, 7, 8, 9, 1],
        [0, 0, 0, 6, 7, 8, 9, 1, 2],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [7, 8, 9, 1, 2, 3, 0, 0, 0],
        [8, 9, 1, 2, 3, 4, 0, 0, 0],
        [9, 1, 2, 3, 4, 5, 0, 0, 0],
    ]
    _test_sudoku(grid7, expect_none=True)


def test_sat_sudoku_8():
    grid8 = [
        [2, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [5, 0, 2, 6, 0, 0, 4, 0, 7],
        [0, 0, 0, 0, 0, 4, 1, 0, 0],
        [0, 0, 0, 0, 9, 8, 0, 2, 3],
        [0, 0, 0, 0, 0, 3, 0, 8, 0],
        [0, 0, 5, 0, 1, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
    ]
    _test_sudoku(grid8, expect_none=True)


def check_sudoku(original, result, expect_none=False):
    if expect_none:
        assert result is None
    else:
        assert result is not None
        n = len(original)
        assert len(result) == n
        assert all(len(row) == n for row in result)
        sn = int(n**0.5)
        all_nums = set(range(1, n + 1))
        assert all(
            (iv == jv or iv == 0)
            for i, j in zip(original, result)
            for iv, jv in zip(i, j)
        )
        assert all(set(i) == all_nums for i in result)
        for c in range(n):
            assert {i[c] for i in result} == all_nums
        for sr in range(sn):
            for sc in range(sn):
                assert {
                    result[r][c]
                    for r in range(sr * sn, (sr + 1) * sn)
                    for c in range(sc * sn, (sc + 1) * sn)
                } == all_nums


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
