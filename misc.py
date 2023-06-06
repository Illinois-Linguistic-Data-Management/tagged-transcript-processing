from collections import OrderedDict
import os
import data_writer
import analysis
import tagged_cha_reader

FILENAMES = os.listdir("all\\")
texts = OrderedDict()

# extract texts from files and index them by speaker
for file_name in FILENAMES:
    text_num = int(file_name[0:3])
    new_text = " ".join(tagged_cha_reader.get_lines("all\\" + file_name))


    texts[text_num] = new_text

data = data_writer.DataFile()

for text_num in texts:
    new_data_line = data_writer.DataLine(text_num)
    doc = (texts[text_num])
    try:
        new_data_line.word_count = analysis.count_words(doc)
    except IndexError:
        print (text_num)
        