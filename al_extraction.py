def count_adp(text, adp):
    counter = 0
    tokens = text.split()
    for token in tokens:
        token_parts = token.split(".")
        if len(token_parts) > 1 and token_parts[1] == "ADP":
            counter = counter + 1 if  token_parts[0].lower() == adp else counter 
    return counter 


def detect_a_or_al(token):
    token_parts = token.split(".")
    if len(token_parts) > 1 and token_parts[1] == "ADP":
        return token_parts[0].lower() == "a" or token_parts[0].lower() == "al"
    return False

def is_verb(token):
    token_parts = token.split(".")
    return len(token_parts) > 1 and token_parts[1] == "VERB"
def is_noun(token):
    token_parts = token.split(".")
    return len(token_parts) > 1 and (token_parts[1] == "NOUN" or token_parts[1] == "PRON" or token_parts[1] == "PRO")
def get_text(token):
    return token.split(".")[0] 
def get_pos(token):
    parts = token.split(".")
    if len(parts) > 1:
        return parts[1]
    return ""



def extract_als(text):
    results = []
    tokens = text.split()
    for i, token in enumerate(tokens):
        if detect_a_or_al(token):
            context = ""
            # collect tokens in front of adp until a verb is found
            j = i 
            while (j > 0 and not is_verb(tokens[j])):
                context = get_text(tokens[j]) + " " + context
                j -= 1
            # add the verb too
            if j >= 0:
                context = get_text(tokens[j]) + " " + context
            k = i + 1
            # collect tokens afterwards 
            while (k < len(tokens)):
                context += get_text(tokens[k])
                if is_noun(tokens[k]):
                    break 
                else:
                    context += " "
                k += 1
            results += [context]
    return results 

if __name__ == "__main__":
    import tagged_cha_reader 
    test = tagged_cha_reader.get_text("input/103_spanish.cha")
    print(extract_als(test))
            










