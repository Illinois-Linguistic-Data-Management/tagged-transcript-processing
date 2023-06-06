import tagged_cha_reader
import data_writer
import analysis
import os
from collections import OrderedDict

LANGUAGE = "spanish"
BACKSLASH = "\\"

# the directory containting files to analyze
INPUT_DIR = f"properly_tagged_{LANGUAGE}{BACKSLASH}"
FILENAMES = os.listdir(INPUT_DIR)
# the tokens to look at
TOKENS = ["a", "the", "el-det", "los-det", "la-det", "las-det", "los-pro", "la-pro", "las-pro", "un", "una", "unos", "unas"]



texts = OrderedDict()
print(f"Processing {LANGUAGE} language .cha files")
# extract texts from files and index them by speaker
for file_name in FILENAMES:
    text_num = int(file_name[0:3])
    new_text = " ".join(tagged_cha_reader.get_lines(INPUT_DIR + file_name))


    texts[text_num] = new_text

data = data_writer.DataFile()

for text_num in texts:
    new_data_line = data_writer.DataLine(text_num)
    doc = (texts[text_num])
    try:
        new_data_line.word_count = analysis.count_words(doc)
    except IndexError:
        print (text_num)
        break

    # get the data
    for token in TOKENS:
        dep = "det"
        # some tokens specify dependencies
        if "-" in token:
            real_token = token.split("-")[0]
            dep = token.split("-")[1]
            # find non determiners by removing determiners from total occurances
            if dep == "pro":
                count = analysis.count_dep(doc, real_token, "PRON") 
            else:
                count = analysis.count_dep(doc, real_token,  dep.upper())
        else:
            count = analysis.count_dep(doc, token, dep.upper())
        # update with results

        new_data_line.update_entry(token, dep, count)

    new_data_line.update_totals()
    data.add_line(new_data_line)

data.write_to_csv(f"{LANGUAGE}_output")





