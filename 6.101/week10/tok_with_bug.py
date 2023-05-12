def get_char_type(char):
    operators = {"+", "*", "/", "(", ")"}
    if char.isdigit():
        char_type = "num"
    elif char.isalpha():
        char_type = "let"
    elif char == "-":
        char_type = "min"
    elif char in operators:
        char_type = "opr"
    elif char == ".":
        char_type = "dot"
    elif char == " ":
        char_type = "spa"
    else:
        char_type = None
    return char_type


table_map =              {"num":0, "let":1, "min":2, "opr":3, "dot":4, "spa":5}
state_table = { "Start": ["Num_1", "Lettr", "Minus", "Opert", "Num_2", "Space"],
                "Num_1": ["Num_1", "EmitT", "EmitT", "EmitT", "Num_2", "EmitT"],
                "Num_2": ["Num_2", "EmitT", "EmitT", "EmitT", "EmitT", "EmitT"],
                "Minus": ["Num_1", "EmitT", "EmitT", "EmitT", "EmitT", "EmitT"],
                "Lettr": ["Lettr", "Lettr", "EmitT", "EmitT", "EmitT", "EmitT"],
                "Space": ["Start", "Start", "Start", "Start", "Start", "Start"],
                "Opert": ["EmitT", "EmitT", "EmitT", "EmitT", "EmitT", "EmitT"],
                "EmitT": ["Start", "Start", "Start", "Start", "Start", "Start"] }


def tokenize(str):
    state = "Start"
    curr = ""
    str_iter = iter(str)
    c = next(str_iter, None)
    while c:
        char_type = get_char_type(c)
        new_state = state_table[state][table_map[char_type]]
        print(f"{c=} {char_type=} {state=} => {new_state=} {curr=}", end="")
        if new_state == "Space":
            c = next(str_iter, None)
            new_state = "Start"
        elif new_state == "EmitT":
            yield curr
            curr = ""
            new_state = "Start"
        else:
            curr += c  # /concat
            c = next(str_iter, None)
        print(f" --> {curr=}")
        state = new_state
    yield curr


def prt(inp):
    print(f"tokenizing {inp} ...")
    print(f"{inp!r} tokenized as\n{list(tokenize(inp))}\n")


# Exercise: find & fix the bug that results in the behavior below

prt("awts + -50")   # ['awts', '+', '-50'] CORRECT
prt("awts + -.50")  # ['awts', '+', '-', '.50'] BUG should be ['awts', '+', '-.50']
