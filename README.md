# tagged-transcript-processing

These scripts are designed to analyze transcripts processed by the parser found in the `spanglish-pos-tagger` repository.

Usage: place the transcripts to analyze into a directory called `\properly_tagged_english`, or `\properly_tagged_spanish`, depending on 
the language of the transcripts. Edit the LANGUAGE variable in `main.py` accordingly. The script files should be in the directory containing the `\properly_tagged_x` directory. Run the `main.py` file; the data should be saved to a file called `x_output.csv`. 

If an input file is improperly formatted, `main.py` may terminate prematurely and print a number. This is the transcript number of the first transcript to throw an error. The `misc.py` file can be used to scan a batch of transcripts for such errors; the files to investigate should be placed in a directory called `\all`. The transcript number of any detected defective files will be printed out.
