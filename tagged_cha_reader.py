"""
A module for reading .cha files that have been tagged.
The get_lines method will return the lines which contain
tagged tokens.
"""

FILENAME = "148mbert_english.cha"
from collections import OrderedDict

def get_transcript_language(cha_file: str) -> str:
    with open(cha_file) as f:
        lines = f.readlines()
    for line in lines:
        if "@Languages" in line:
            contents = line.split()
            contents = contents[1].split(",")
            return contents[0]
        
def get_group_description(group_num: int) -> str:
    descriptions = OrderedDict([(199, "bil.children"), (299, "bil.adults"), (399, "Eng-mon.children"), (499, "Eng-mon.adults"), (599, "Span-L2.children"), 
                    (699, "Span-mon.children"), (799, "Span-mon.adults")])

    for key in descriptions:
        if group_num <= key:
            return descriptions[key]
        
# def get_group_language(group_num: int) -> str:
#     languages = OrderedDict([(199, "English, Spanish"), (299, "English, Spanish"), (399, "English"), (499, "Eng-mon.adults"), (599, "Span-L2.children"), 
#                     (699, "Span-mon.children"), (799, "Span-mon.adults")])


def get_lines(cha_file: str) -> list[str]:
    """
    Given the name of a tagged cha file, produces a list of strings 
    with each string being a tagged line from the file

    Parameters:

        cha_file  (str): the name of a .cha file, extension included

    Returns:
        str list : a list of lines from the file

    Examples:
        >>> get_lines("example.cha"))

        >>> get_lines("example2.cha"))
    """
    content = []
    with open(cha_file) as f:
        lines = f.readlines()
    for line in lines:
        if "%pos:" in line and line[0] != "@":
            content.append(line[5:-1])

    new_content = []
    for line in content:
        line = line.strip()
        if len(line) > 0:
            new_content.append(line)

    return new_content
    
if __name__ == "__main__":
    # content = get_lines(FILENAME)


    # for l in content:
    #     print(l)
    test = " ".join(get_lines(FILENAME))
    test2 = test.split()
    test3 = " ". join([x.split(".")[0] for x in test.split()])


    print(test)
    print(test3)
