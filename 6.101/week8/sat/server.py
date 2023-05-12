#!/usr/bin/env python3

import os
import html
import json
import importlib
import mimetypes
import traceback

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

import lab as lab
from test import check_sudoku

LOCATION = os.path.realpath(os.path.dirname(__file__))


def parse_post(environ):
    try:
        body_size = int(environ.get("CONTENT_LENGTH", 0))
    except:
        body_size = 0

    body = environ["wsgi.input"].read(body_size)
    try:
        return json.loads(body)
    except:
        return {}

def find_region(n, r, c):
    """(slowly) find which region (as a set of locations) the given coordinates are in [0, n)"""
    for i in range(n):
        locs = set(subgrid_locs(n, i))
        if (r,c) in locs:
            return locs

def victory_check(payload):
    board = payload['board']
    empty_board = [[0] * len(board) for _ in board]
    try:
        assert board
        check_sudoku(empty_board, board)
        return {'victory': True}
    except AssertionError:
        return {'victory': False}

def solve(payload):
    board = payload
    formula = lab.sudoku_board_to_sat_formula(board)
    assignments = lab.satisfying_assignment(formula)
    sol = lab.assignments_to_sudoku_board(assignments, len(board))
    return sol


funcs = {
    'victory_check': victory_check,
    'solve': solve,
}

def application(environ, start_response):
    path = (environ.get("PATH_INFO", "") or "").lstrip("/")
    if path in funcs:
        try:
            out = funcs[path](parse_post(environ))
            body = json.dumps(out).encode("utf-8")
            status = "200 OK"
            type_ = "application/json"
        except Exception as e:
            tb = traceback.format_exc()
            print(
                "--- Python error (likely in your lab code) during the next operation:\n"
                + tb,
                end="",
            )
            body = html.escape(tb).encode("utf-8")
            status = "500 INTERNAL SERVER ERROR"
            type_ = "text/plain"
    else:
        if path == "":
            static_file = "sudoku.html"
        else:
            static_file = path

        test_fname = os.path.join(LOCATION, 'ui', static_file)
        try:
            status = "200 OK"
            with open(test_fname, "rb") as f:
                body = f.read()
            type_ = mimetypes.guess_type(test_fname)[0] or "text/plain"
        except FileNotFoundError:
            status = "404 FILE NOT FOUND"
            body = test_fname.encode("utf-8")
            type_ = "text/plain"

    len_ = str(len(body))
    headers = [("Content-type", type_), ("Content-length", len_)]
    start_response(status, headers)
    return [body]


if __name__ == "__main__":
    PORT = 6101
    print(f"starting server.  navigate to http://localhost:{PORT}/")
    with make_server("", PORT, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
