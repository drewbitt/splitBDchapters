# splitBDchapters

Split text file BD chapters from eac3to into separate files for each episode while adjusting times. Expects unedited eac3to chapter file.

Useful when multiple episodes are combined in one mpls.


Usage:
`split.py filename.txt --indexes 0,4,9,15,18 --offset 1 --file-name "chapters$n" --titles`

The example would have 0-4,5-9,10-15,16-18 together. Need to include the first and last chapter.

`--offset/-o` determines the starting index number for the generated files and is a default of 1. `--titles` is optionally included if you want generic "Chapter 01, Chapter 02" chapter names.

`--file-name` defaults to `chapters%n`. Use it to specify the name format for generated files, `%n` is used to specify the split number location in the string.

You can also use `--only-titles` for only creating generic chapter title names without creating additional chapter files.
