# splitBDchapters

Split text file BD chapters from eac3to into separate files for each episode while adjusting times. Expects unedited eac3to chapter file.

Useful when multiple episodes are combined in one mpls.

Usage:
`split.py filename.txt 0,4,9,15,18 10`

The example would have 0-4,5-9,10-15,16-18 together. Need to include 0 and the last chapter.

The third integer parameter is optional and is used as a filename number. If you wanted to start from a different episode when creating new text files, i.e. instead of chapters1.txt, chapters2.txt etc. with an option of 10 this would be chapters10.txt, chapters11.txt etc