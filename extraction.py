"""
The purpose of this module is to provide functionality for extracting
the contexts of particular tokens or classes of tokens.
"""

from collections.abc import Callable


def is_verb(token: str) -> bool:
    """
    returns True if the token is a verb
    """
    token_parts = token.split(".")
    return len(token_parts) > 1 and token_parts[1] == "VERB"
def is_noun(token: str) -> bool:
    """
    returns True if the token is a noun
    """
    token_parts = token.split(".")
    return len(token_parts) > 1 and (token_parts[1] == "NOUN" or token_parts[1] == "PRON" or token_parts[1] == "PRO")

def is_det(token: str) -> bool:
    """
    returns True f the token is a determiner or 
    something determiner-adjacent
    """
    POSSESSIVES = ["his", "her", "its", "your", "my", "our", "their", "su", "sus", "'s"]
    MERGED = ["del", "al"]
    if get_pos(token) == "DET":
        return True 
    elif get_text(token) in POSSESSIVES or get_text(token) in MERGED:
        return True 
    return False

def get_text(token: str) -> str:
    """
    get the text component of the token
    """
    return token.split(".")[0] 
def get_pos(token: str) -> str:
    """
    get the part of speech component of the token
    """
    parts = token.split(".")
    if len(parts) > 1:
        return parts[1]
    return ""

def matches_pos(token : str, pos: str) -> bool:
    """
    returns True if token has the part of speech
    specified in pos, and False otherwise
    """
    return pos == get_pos(token)
def matches_text(token : str, text: str) -> bool:
    """
    returns True if token has the same text as text
    (case-insensitive), and false otherwise.
    """
    return text.lower() == get_text(token).lower()
def match_any(token : str, *words : str):
    """
    returns True if token has the same text as any
    of the word in words(case-insensitive), and 
    false otherwise.
    """
    for word in words:
        if matches_text(token, word):
            return True 
    return False


def extract(text: str, pos: str, token_strings: list[str] = None, scan_forward_limit: int = 0, scan_backward_limit: int = 0, 
            forward_target_detected: Callable[[str], bool] = None, backward_target_detected: Callable[[str], bool] = None) -> list[str]:
    """
    Given a text, a target part of speech, and optionally target text content, numerical limits on forward 
    and backward scanning, and functions to trigger an end of scan, searches the text for occurences of the
    target, and returns the contexts in which the target occurs, the boundarys of which are determined by the
    optional limit and detection parameters.

    Parameters:

        text (str): tokenized text (e.g. "I.PRON eat.VERB cake.NOUN")         
        pos (str): a part of speech tag to match on
        token_strings (str list): an optional list of strings to match on. If given, only tokens with matching text will be collected.
        scan_forward_limit (int): the number of tokens after a match to add to the token's contex
        scan_backward_limit (int): the number of tokens before a match to add to the token's context
        forward_target_detected (str) -> bool: a callable to check whether a token in front of the match is a context boundary. 
        backward_target_detected (str) -> bool: a callable to check whether a token before the match is a context boundary. 

    Returns:
        str list : a list of extracted contexts

    Examples:
        >>> extract("I.PRON eat.VERB cake.NOUN", "VERB", scan_forward_limit = 1)
        ["eat cake"]

        >>> extract("You.PRON run.VERB and.CCONJ swim.VERB", "CCONJ", 
                     forward_target_detected = is_verb, backward_target_detected = is_verb)
        ["run and swim"]
    """
    results = []
    tokens = text.split()
    # this function returns true if the token matches the specified part of speech, and 
    # if provided, any of the given token strings 
    detected = lambda token : matches_pos(token, pos) and (match_any(token, *token_strings) if token_strings else True)
    
    for i, token in enumerate(tokens):

        # these functions check whether enough context has been collected on each end
        if scan_backward_limit and backward_target_detected:
            # this returns false if either the backtrack distance is too high or a target is detected
            backward_limit_not_reached = lambda x : x >= 0 and  backward_target_detected and i - x <= scan_backward_limit 
        else:
            # this returns false if both the backtrack distance is too high and a target is detected
            backward_limit_not_reached = lambda x : x >= 0 and  (backward_target_detected or i - x <= scan_backward_limit)

        if scan_forward_limit and forward_target_detected:
            # this returns false if either the forward distance is too high or a target is detected
            forward_limit_not_reached = lambda x :  x < len(tokens) and  forward_target_detected and x - i <= scan_forward_limit
        else:
            # this returns false if both the forward distance is too high and a target is detected
            forward_limit_not_reached = lambda x :  x < len(tokens) and  (forward_target_detected or x - i <= scan_forward_limit)

        if detected(token):
            context = get_text(token)
            # collect tokens in front of the target until a boundary condition is met
            j = i - 1 
            while (backward_limit_not_reached(j)):
                context = get_text(tokens[j]) + " " + context
                if backward_target_detected and backward_target_detected(tokens[j]):
                    break     
                else:
                    j -= 1
                    
            k = i + 1
            # collect tokens after the target until a boundary condition is met 
            if forward_limit_not_reached(k):
                context += " "
            while (forward_limit_not_reached(k)):
                context += get_text(tokens[k])
                if forward_target_detected and forward_target_detected(tokens[k]):
                    break 
                else:
                    context += " "
                k += 1

            results += [context.strip()]

    return results 

if __name__ == "__main__":
    import tagged_cha_reader 
    import os
    import platform

    # choose appropriate separator based on os
    if platform.system() == "Windows":
        BACKSLASH = "\\"
    else:
        BACKSLASH = "/"
        
    # the directory containing files to analyze
    INPUT_DIR = f"input{BACKSLASH}"
    OUTPUT_DIR = f"contexts{BACKSLASH}"

    FILENAMES = os.listdir(INPUT_DIR)

   # define extractors here
    extractors = {"a_and_als": lambda text : extract(text, "ADP", token_strings=["a", "al"], 
                                                     forward_target_detected= is_noun, 
                                                     backward_target_detected = is_verb), 
                  "verbs" : lambda text : extract(text, "VERB", forward_target_detected= is_noun),
                  "test"  : lambda text : extract(text, "NOUN", scan_backward_limit= 7, 
                                                  backward_target_detected= is_det)}
    # create a csv file for each extractor
    for extractor_name in extractors:
        output = open(f"{extractor_name}_extraction_results_spanish.csv", "w")
        extractor = extractors[extractor_name]
        # start with header line
        lines = f"participant,group,instance,example\n"
        
        for file_name in sorted(FILENAMES):
            # DS_Store check needed for macOS; only process spanish language texts here
            if file_name != ".DS_Store" and tagged_cha_reader.get_transcript_language(f"input{BACKSLASH}{file_name}") != "eng":
                text = tagged_cha_reader.get_text(INPUT_DIR + file_name)
                prefix = file_name.split(".")[0]
                text_num = int(prefix[0:3])
                group_num = (text_num // 100) * 100
                #group = tagged_cha_reader.get_group_description(text_num)
                results = extractor(text)
                for i, result in enumerate(results):
                    # commas would result in extra columns, so replace 
                    # them with a different character in new_result
                    if ',' in result:
                        new_result = ""
                        for char in result:
                            if char == ',':
                                new_result += '|'
                            else:
                                new_result += char
                        result = new_result
                    # create new csv line with data
                    line = f"{text_num},{group_num},{i + 1},{result}"
                    if i < len(results):
                        line += "\n"
                    lines += line 

        output.write(lines)
        output.close()