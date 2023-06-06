"""
A module for reading .cha files that have been tagged.
The get_lines method will return the lines which contain
tagged tokens.
"""

FILENAME = "148mbert_english.cha"


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
    content = get_lines(FILENAME)


    for l in content:
        print(l)

