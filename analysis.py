"""
A module for analyzing text tagged in the following format: 'text.POS'.
"""

def count_words(text : str) -> int:
    """
    Given a tagged text, counts all the words (tokens other than punctuation)
    in it
    """

    counter = 0

    
    tokens = text.split(" ")
    for token in tokens:
        # tokens should be formatted as text.POS
        pos = token.split(".")[1]
        if pos != "PUNCT":
            counter += 1

    return counter

def count_dep(text : str, word : str, pos : str = None) -> int:
    """
    Given a tagged text, a word, and optionally a dependency, 
    find all matches. If no dependency is provided, just find
    all occurences of the word.
    """
    tokens = text.split(" ")
    counter = 0
    for token in tokens:

        current_word = token.split(".")[0].lower()
        if (len(token.split(".")) >= 2):

            current_pos = token.split(".")[1]
        else:
            # if a word is not tagged for some reason, 
            # it will be ignored
            current_pos = None

        if pos:
            if word == current_word and pos == current_pos:
                counter += 1 
        else:
            if word == current_word:
                counter += 1

    return counter


