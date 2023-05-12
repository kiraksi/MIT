"""
6.1010 Spring '23 Lab 11: LISP Interpreter Part 1
"""
#!/usr/bin/env python3
import os
import lab
import sys
import json

import pytest

TEST_DIRECTORY = os.path.dirname(__file__)


class NotImplemented:
    def __eq__(self, other):
        return False


try:
    nil_rep = lab.result_and_frame(lab.parse(["nil"]))[0]
except:
    nil_rep = NotImplemented()


def list_from_ll(ll):
    if isinstance(ll, lab.Pair):
        if ll.cdr == nil_rep:
            return [list_from_ll(ll.car)]
        return [list_from_ll(ll.car)] + list_from_ll(ll.cdr)
    elif ll == nil_rep:
        return []
    elif isinstance(ll, (float, int)):
        return ll
    else:
        return "SOMETHING"


def make_tester(func):
    """
    Helper to wrap a function so that, when called, it produces a
    dictionary instead of its normal result.  If the function call works
    without raising an exception, then the results are included.
    Otherwise, the dictionary includes information about the exception that
    was raised.
    """

    def _tester(*args):
        try:
            return {"ok": True, "output": func(*args)}
        except lab.SchemeError as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            return {"ok": False, "type": exc_type.__name__}

    return _tester


def load_test_values(n):
    """
    Helper function to load test inputs/outputs
    """
    with open(os.path.join(TEST_DIRECTORY, "test_inputs", f"{n:02d}.txt")) as f:
        inputs = eval(f.read())
    with open(os.path.join(TEST_DIRECTORY, "test_outputs", f"{n:02d}.txt")) as f:
        outputs = eval(f.read())
    return inputs, outputs


def run_continued_evaluations(ins):
    """
    Helper to evaluate a sequence of expressions in an environment.
    """
    lab.eval = None 
    lab.exec = None
    env = None
    outs = []
    try:
        t = make_tester(lab.result_and_frame)
    except:
        t = make_tester(lab.evaluate)
    for i in ins:
        if env is None:
            args = (i,)
        else:
            args = (i, env)
        out = t(*args)
        if out["ok"]:
            env = out["output"][1]
        if out["ok"]:
            try:
                typecheck = (int, float, lab.Pair)
                func = list_from_ll
            except:
                typecheck = (int, float)
                func = lambda x: x if isinstance(x, typecheck) else "SOMETHING"
            out["output"] = func(out["output"][0])
        outs.append(out)
    return outs


def compare_outputs(x, y, msg):
    # y is expected, x is your result
    if x["ok"]:
        assert y["ok"], (
            msg
            + f'\n\nExpected an exception ({y.get("type", None)}), but got {x.get("output", None)!r}'
        )
        if isinstance(x["output"], (int, float)):
            assert type(x["output"]) == type(y["output"]), (
                msg
                + f'\n\nOutput has incorrect type (expected {type(y.get("output", None))} but got {type(x.get("output", None))}'
            )
            assert abs(x["output"] - y["output"]) <= 1e-6, (
                msg
                + f'\n\nOutput has incorrect value (expected {y.get("output", None)!r} but got {x.get("output", None)!r})'
            )
        else:
            assert x["output"] == y["output"], (
                msg
                + f'\n\nOutput has incorrect value (expected {y.get("output", None)!r} but got {x.get("output", None)!r})'
            )
    else:
        assert not y["ok"], (
            msg
            + f'\n\nDid not expect an exception (got {x.get("type", None)}, expected {y.get("output", None)!r})'
        )
        assert x["type"] == y["type"], (
            msg
            + f'\n\nExpected {y.get("type", None)} to be raised, not {x.get("type", None)}'
        )
        assert x.get("when", "eval") == y.get("when", "eval"), (
            msg
            + f'\n\nExpected error to be raised at {y.get("when", "eval")} time, not at {x.get("when", "eval")} time.'
        )


def do_continued_evaluations(n):
    """
    Test that the results from running continued evaluations in the same
    environment match the expected values.
    """
    inp, out = load_test_values(n)
    msg = message(n)
    results = run_continued_evaluations(inp)
    for x, (result, expected) in enumerate(zip(results, out)):
        m = f"\nevaluate input line {x+2}: \n\t{repr(inp[x])}"
        m += f'\nexpected:\n\t{expected.get("output") if expected.get("output") else expected.get("type")}'
        m += f'\nresult:\n\t{result.get("output") if result.get("output") else result.get("type")}'
        if n == 8: # bad lookups test case
            m += "\nBe careful not to use mutable default arguments!"
        compare_outputs(result, expected, msg+m)


def do_raw_continued_evaluations(n):
    """
    Test that the results from running continued evaluations in the same
    environment match the expected values.
    """
    with open(os.path.join(TEST_DIRECTORY, "test_outputs", f"{n:02d}.txt")) as f:
        expected = eval(f.read())
    env = None
    results = []
    try:
        t = make_tester(lab.result_and_frame)
    except:
        t = make_tester(lab.evaluate)
    with open(os.path.join(TEST_DIRECTORY, "test_inputs", f"{n:02d}.scm")) as f:
        for line in iter(f.readline, ""):
            try:
                parsed = lab.parse(lab.tokenize(line.strip()))
            except lab.SchemeSyntaxError:
                results.append(
                    {
                        "expression": line.strip(),
                        "ok": False,
                        "type": "SchemeSyntaxError",
                        "when": "parse",
                    }
                )
                continue
            out = t(*((parsed,) if env is None else (parsed, env)))
            if out["ok"]:
                env = out["output"][1]
            if out["ok"]:
                try:
                    typecheck = (int, float, lab.Pair)
                    func = list_from_ll
                except:
                    typecheck = (int, float)
                    func = lambda x: x if isinstance(x, typecheck) else "SOMETHING"
                out["output"] = func(out["output"][0])
            out["expression"] = line.strip()
            results.append(out)
    for ix, (result, exp) in enumerate(zip(results, expected)):
        msg = f"for line {ix+1} in test_inputs/{n:02d}.scm:\n    {result['expression']}"
        compare_outputs(result, exp, msg=msg)


def run_test_number(n, func, fname=''):
    tester = make_tester(func)
    inp, out = load_test_values(n)
    msg = message(n) 
    for x, (i, o) in enumerate(zip(inp, out)):
        m = f"\n{func.__name__ if not fname else fname} input line {x+2}: \n\t{repr(i)}"
        m += f'\nexpected:\n\t{o.get("output") if o.get("output") else o.get("type")}'
        res = tester(i)
        m += f'\nresult:\n\t{res.get("output") if res.get("output") else res.get("type")}'
        compare_outputs(res, o, msg+m)


def message(n, include_code=False):
    sn = n if n >= 10 else "0"+str(n)
    msg = f"\nfor test_inputs/{sn}.txt"
    try:
        with open(os.path.join(TEST_DIRECTORY, "scheme_code", f"{n:02d}.scm")) as f:
            code = f.read()
        msg += f" and scheme_code/{n}.scm"
    except Exception as e:
        with open(os.path.join(TEST_DIRECTORY, "test_inputs", f"{n:02d}.txt")) as f:
            code = f.read()
    if include_code:
        msg += " that begins with\n"
        msg += code if len(code) < 80 else code[:80] + "..."
    return msg


def _test_file(fname, num):
    try:
        out = lab.evaluate_file(os.path.join(TEST_DIRECTORY, "test_files", fname))
        out = list_from_ll(out)
        out = {"ok": True, "output": out}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        out = {"ok": False, "type": exc_type.__name__}
    with open(os.path.join(TEST_DIRECTORY, "test_outputs", f"{num}.txt")) as f:
        expected = eval(f.read())
    msg = _test_file_msg(fname, num)
    return out, expected, msg


def _test_file_msg(fname, n):
    msg = f"\nwhile running test_files/{fname} that begins with\n"
    with open(os.path.join(TEST_DIRECTORY, "test_files", fname)) as f:
        code = f.read()
    msg += code if len(code) < 80 else code[:80] + "..."
    return msg


## TESTS FOR TOKENIZATION AND PARSING



def test_tokenize():
    run_test_number(0, lab.tokenize)


def test_tokenize_lines():
    run_test_number(31, lab.tokenize)


def test_tokenize_comments():
    run_test_number(32, lab.tokenize)


def test_parse():
    run_test_number(1, lab.parse)


def test_parse_valid():
    run_test_number(33, lab.parse)


def test_parse_invalid():
    run_test_number(2, lab.parse)


def test_tokenize_and_parse():
    run_test_number(3, lambda i: lab.parse(lab.tokenize(i)), "parse(tokenize(line))")


## TESTS FOR CALCULATOR


def test_calc():
    run_test_number(4, lab.evaluate)


def test_mult_div():
    run_test_number(5, lab.evaluate)


def test_calc_pair():
    run_test_number(34, lab.evaluate)
    

def test_calc_nested():
    run_test_number(35, lab.evaluate)


## TESTS FOR VARIABLE ASSIGNMENT AND LOOKUP

def test_result_and_frame():
    # is result_and_frame defined and work for a simple input
    output = lab.result_and_frame(5)
    try:
        assert len(output) == 2, f"Expected len 2 but got {output=}"
    except:
        assert False, f"Expected len 2 but got {output=}"
    assert output[0] == 5, f"Expected first part of output evaluated expression but got {output=}"
    assert output[1] is not None and output[0]!=output[1], f"Expected second part of output to be a frame but got {output=}"


def test_simple_assignment_1():
    do_continued_evaluations(6)


def test_simple_assignment_2():
    do_continued_evaluations(7)


def test_bad_lookups():
    do_continued_evaluations(8)


def test_rename_builtin():
    do_continued_evaluations(9)


## TESTS FOR FUNCTION DEFINITION/APPLICATIONi


def test_simple_function():
    do_continued_evaluations(10)


def test_inline_lambda():
    do_continued_evaluations(11)


def test_closures():
    do_continued_evaluations(12)


## INTEGRATION TESTS


def test_short_definition():
    do_raw_continued_evaluations(13)


def test_dependent_definition():
    do_raw_continued_evaluations(14)


def test_scoping_1():
    do_raw_continued_evaluations(15)


def test_scoping_2():
    do_raw_continued_evaluations(16)


def test_scoping_3():
    do_raw_continued_evaluations(17)


def test_scoping_4():
    do_raw_continued_evaluations(18)


def test_scoping_5():
    do_raw_continued_evaluations(19)


def test_calling_errors():
    do_raw_continued_evaluations(20)


def test_functionception():
    do_raw_continued_evaluations(21)


def test_alias():
    do_raw_continued_evaluations(22)


def test_big_scoping_1():
    do_raw_continued_evaluations(23)


def test_big_scoping_2():
    do_raw_continued_evaluations(24)


def test_big_scoping_3():
    do_raw_continued_evaluations(25)


def test_big_scoping_4():
    do_raw_continued_evaluations(26)


## ADDITIONAL TESTS FOR COMMON ERRORS


def test_more_syntax():
    do_raw_continued_evaluations(27)


def test_nested_defines():
    do_raw_continued_evaluations(28)


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
