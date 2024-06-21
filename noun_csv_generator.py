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
        # only group 700s are added
        if file_prefix[0] == '7':
            new_text = tagged_cha_reader.get_lines(INPUT_DIR + file_name)


            texts[file_prefix] = new_text

data = data_writer.DataFile()
# each entry in 'texts' is a list of sentences, representing a document

output = open(("noun_lines.csv"), "w")

new_texts = {}
for file_prefix in sorted(texts.keys()):
    
    new_sentences = []
    for sentence in texts[file_prefix]:
        tokens = sentence.split(" ")

        noun_count = 0
        new_tokens = []
        
        for token in tokens:
            word = token.split(".")[0]
            pos = token.split(".")[1]
            if word == ",":
                token = "COMMA."+ pos
            if pos == "NOUN":
                token = word +".!" 
                noun_count += 1
            new_tokens += [token]
        new_sentences += [" ".join(new_tokens)]
    new_texts[file_prefix] = new_sentences

for file_prefix in sorted(new_texts.keys()):
    for sentence in new_texts[file_prefix]:
        noun_count = 0 
        tokens = sentence.split(" ")
        for token in tokens:
            if '!' == token.split(".")[1] or 'PROPN' == token.split(".")[1]:
                noun_count += 1

        for j in range(noun_count):

            tokens = sentence.split(" ")
            output.write(file_prefix + ",")
            new_noun_encountered = False
            encountered_noun_count = 0
            for i, token in enumerate(tokens):
                
                word = token.split(".")[0]
                pos = token.split(".")[1]

                output.write(word)
                #print(pos)
                if (pos == "!" or pos =="PROPN") and j == encountered_noun_count:
                    #tokens[i] = word + ".NOUN"

                    encountered_noun_count += 1
                    new_noun_encountered = True
                    output.write("!")
                elif (pos == "!" or pos == "PROPN"):
                    encountered_noun_count += 1
                if i < len(tokens) - 1:
                    output.write(" ")
            output.write("\n")
           


output.close()
