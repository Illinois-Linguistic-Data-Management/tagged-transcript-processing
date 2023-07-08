"""
A module with classes useable for
 collecting and writing determiner data.
"""

# # openpyxl - for working with xls files
# from openpyxl.workbook import Workbook
from collections import OrderedDict

DEFINITES = ["the",  "el-det", "los-det", "la-det", "las-det", "lo-det"]
INDEFINITES = ["a", "un", "una", "unos", "unas"]
PRONOUNS = ["los-pro", "la-pro", "las-pro", "lo-pro", 
            "me", "him", "her-pro", "us", "them", "you", "it", "le", "les", "se",  #obj pronouns - but it and you can be obj or subj
            "I", "he", "she", "we", "they", "yo", "tu", "él", "ella", "nosotros", "ellos", "ellas"] # subj pronouns
POSSESSIVES = ["my", "his", "her-det", "its", "our", "your", "their",
               "su", "sus"]
NAMES = ["little red riding hood", "girl", "grandmother", "grandma", "wolf", "animal", "hunter", "man", "mother", "woodcutter",
         "caperucita roja", "caperucita", "niña", "abuela", "abuelita", "lobo", "cazador", "hombre", "madre", "leñador"]

HEADER_START = ["participant", "group description","transcript language", "total words"]
HEADER_TOKENS = DEFINITES + INDEFINITES + POSSESSIVES + PRONOUNS 

# things we want to find the total counts and percents for
TOTALS = ["definite determiner", "indefinite determiner", "possessive determiner", "name", "pronoun"] 

# make columns for count and % of each quantity totaled
HEADER_TOTALS = [f(x) for x in TOTALS for f in [lambda x : x + " count", lambda x : x +" %"]] 

HEADER = HEADER_START + HEADER_TOKENS + NAMES + HEADER_TOTALS

# tally unique items distinguished by hyphens for reference
VARIABLE_ENTRIES = list(set([x.split("-")[0] for x in HEADER_TOKENS if "-" in x ]))

class DataLine(object):
    
    def __init__(self, participant_num) -> None:
        self.entries = OrderedDict()
        for entry in HEADER:
            if entry == HEADER[0]:
                self.entries[entry] = participant_num
            else:
                self.entries[entry] = 0

    @property
    def as_list(self) :
        result_list = []
        for entry in self.entries:
            result_list += [str(self.entries[entry])]
        return result_list

    @property
    def as_csv_line(self) -> str:

        return ",".join(self.as_list)
    
    @property
    def word_count(self)-> int:
        return self.entries["total words"]
    
    @word_count.setter
    def word_count(self, val: int)-> None:
        self.entries["total words"] = val

    @property
    def language(self):
        return self.entries["transcript language"]
    
    @language.setter 
    def language(self, val):
        self.entries["transcript language"] = val 

    @property
    def group(self):
        return self.entries["group description"] 
    
    @group.setter 
    def group(self, val):
        self.entries["group description"] = val


    def update_totals(self):
        def_count = 0
        indef_count = 0
        pos_count = 0
        pro_count = 0
        name_count = 0
        for entry in self.entries:
            if entry in DEFINITES:
                def_count += self.entries[entry] 
            elif entry in INDEFINITES:
                indef_count += self.entries[entry] 
            elif entry in POSSESSIVES:
                pos_count += self.entries[entry] 
            elif entry in PRONOUNS:
                pro_count += self.entries[entry] 
            elif entry in NAMES:
                name_count += self.entries[entry] 
            
        self.entries["definite determiner count"] = def_count
        self.entries["indefinite determiner count"] = indef_count
        self.entries["possessive determiner count"] = pos_count
        self.entries["pronoun count"] = pro_count
        self.entries["name count"] = name_count

        if self.word_count == 0:
            return
        else:
            self.entries["definite determiner %"]  = round((def_count*100)/self.word_count, 2)
            self.entries["indefinite determiner %"]  = round((indef_count*100)/self.word_count, 2)
            self.entries["possessive determiner %"]  = round((pos_count*100)/self.word_count, 2)
            self.entries["pronoun %"]  = round((pro_count*100)/self.word_count, 2)
            self.entries["name %"]  = round((name_count*100)/self.word_count, 2)
        



    # can't the tallying of counts above be done here instead !! ?? 
    def update_entry(self, token: str, dep: str, val: int):
        if token in VARIABLE_ENTRIES:
            token = token + "-" + dep

        
        self.entries[token] = val




class DataFile(object):

    def __init__(self) -> None:
        self.lines = []

    @property
    def as_csv_contents(self):
        new_str = ",".join(HEADER)
        if len(self.lines) > 0:
            new_str += "\n"

        for i, line in enumerate(self.lines):
            new_str += line.as_csv_line 
            if i != len(self.lines) - 1:
                new_str += "\n"

        return new_str
    
    def add_line(self, line: DataLine):
        self.lines.append(line)
    
    def write_to_csv(self, title = "data_output"):
        output = open((title + ".csv"), "w")

        output.write(self.as_csv_contents)

        output.close()

    # def write_to_xlsx(self, title = "data_output"):
    #     # adapted from https://stackoverflow.com/questions/37182528/how-to-append-data-using-openpyxl-python-to-excel-file-from-a-specified-row
    #     file_name = title + ".xlsx"
    #     wb = Workbook()
    #     page = wb.active
    #     page.append(HEADER)

    #     for line in self.lines:
    #         page.append(line.as_list)
    #     wb.save(filename = file_name)

if __name__ == "__main__":
    print(VARIABLE_ENTRIES)
    print (HEADER_TOTALS)
    # data =  DataFile()
    # data.add_line(DataLine(101))
    # data.add_line(DataLine(203))

    # data.write_to_xlsx()
    #print(data.as_csv_contents)


            











        