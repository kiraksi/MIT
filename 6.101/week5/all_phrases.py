from debug_recursion import show_recursive_structure


"""A grammar dictionary maps a root to a list of possible structures,
   each structure a list of required items, each item either another
   root (string) or a terminal (string).
"""
grammar = {
    "SENTENCE": [["NOUN", "VERB"], ["NOUN", "never", "VERB"]],
    "NOUN": [["pigs"], ["professors"]],
    "VERB": [["fly"], ["think"]],
}

@show_recursive_structure
def one_phrase(root, grammar):
    """Create ONE possible phrase generated from root"""
    # base case: terminal

    # recursive case:
    phrase = []
    ...
    return phrase

#print(f'\n{one_phrase("NOUN", grammar)=}')
#print(f'\n{one_phrase("SENTENCE", grammar)=}')


#@show_recursive_structure
def all_phrases(root, grammar):
    """
    Return: a list of possible phrases (each phrase a list of terminal strings)
    Given: input root (string) and grammar dictionary 
    """
    # base case: terminal
    if root not in grammar:  
        return [[root]]  # list of phrases

    # recursive case
    list_of_phrases = []
    ...
    return list_of_phrases



def small_test():
    print()
    result = all_phrases("pigs", grammar)
    expected = [["pigs"]]
    assert result == expected, f"{sorted(result)} != {sorted(expected)}"

    print()
    result = all_phrases("NOUN", grammar)
    expected = [["pigs"], ["professors"]]
    assert sorted(result) == sorted(expected), f"{sorted(result)} != {sorted(expected)}"

    print()
    result = all_phrases("VERB", grammar)
    expected = [["think"], ["fly"]]
    assert sorted(result) == sorted(expected), f"{sorted(result)} != {sorted(expected)}"

    print("Small test case passed!")


def test_sentence():
    expected = [
        ["pigs", "fly"],
        ["pigs", "think"],
        ["professors", "fly"],
        ["professors", "think"],
        ["pigs", "never", "fly"],
        ["pigs", "never", "think"],
        ["professors", "never", "fly"],
        ["professors", "never", "think"],
    ]

    print()
    result = all_phrases("SENTENCE", grammar)
    print(result)
    assert sorted(result) == sorted(expected), f"Got {result}"
    print("Test sentence correct!")


if __name__ == "__main__":
    pass
    #small_test()
    #test_sentence()
