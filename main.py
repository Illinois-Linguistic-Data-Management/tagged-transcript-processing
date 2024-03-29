import tagged_cha_reader
import data_writer
import analysis
import os
import platform

# choose appropriate separator based on os
if platform.system() == "Windows":
    BACKSLASH = "\\"
else:
    BACKSLASH = "/"
    
# the directory containing files to analyze
INPUT_DIR = f"input{BACKSLASH}"

FILENAMES = os.listdir(INPUT_DIR)
# the tokens to look at 
TOKENS = data_writer.HEADER_TOKENS
NAMES = data_writer.NAMES

texts = {}

# extract texts from files and index them by speaker
for file_name in FILENAMES:
    # macOS compatibility
    if not file_name.startswith("."):
        # use the filename as a key instead
        file_prefix = file_name.split(".")[0]
        new_text = tagged_cha_reader.get_text(INPUT_DIR + file_name)


        texts[file_prefix] = new_text

data = data_writer.DataFile()

for file_prefix in sorted(texts.keys()):
    # initialize DataLine and text
    text_num = int(file_prefix[0:3])
    new_data_line = data_writer.DataLine(text_num)
    doc = (texts[file_prefix])

    # an improperly formatted file might throw an error here
    try:
        new_data_line.word_count = analysis.count_words(doc)
    except IndexError:
        print (file_prefix)
        break
    
    new_data_line.language = tagged_cha_reader.get_transcript_language(INPUT_DIR + file_prefix + ".cha")
    new_data_line.group = tagged_cha_reader.get_group_description(text_num)

    # get the data
    for token in TOKENS:
        dep = "det"
        # some tokens specify dependencies
        if "-" in token:
            real_token = token.split("-")[0]
            dep = token.split("-")[1]
            # find non determiners by removing determiners from total occurances
            if dep == "pro":
                count = analysis.count_pos(doc, real_token, "PRON") 
            else:
                count = analysis.count_pos(doc, real_token,  dep.upper())
        else:
            count = analysis.count_pos(doc, token, dep.upper())
        # update with results

        new_data_line.update_entry(token, dep, count)
    # investigate names separately
    for name in NAMES:
        count = analysis.count_name(doc, name)
        new_data_line.update_entry(name, "", count)

    new_data_line.update_totals()
    data.add_line(new_data_line)

data.write_to_csv("unified_output")





