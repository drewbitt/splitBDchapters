import datetime
import math
import argparse
from tempfile import mkstemp
from os import fdopen, remove
from shutil import move


def split_file(file, names, only_names, rsplit, offset=1, file_name_format="chapters%n"):
    """Main method to split the chapter file
        file: main chapter file, names: boolean for if to add generic chapter names,
        only_names: boolean to ONLY add generic chapter names without creating a new file,
        rsplit: array of indexes to include in each file (see README for split explanation),
        offset: what to start numbering at for filenames, file_name_format: format for new filenames"""

    if only_names:
        # Create temp file
        fh, abs_path = mkstemp()
        with fdopen(fh, 'w') as new_file:
            with open(file, 'r') as old_file:
                for count, line in enumerate(old_file):
                    if count % 2 != 0:
                        chap_num = str(math.ceil((count + 1) / 2)).zfill(2)
                        new_file.write("CHAPTER{0}NAME=Chapter {1}\n".format(chap_num, chap_num))
                    else:
                        new_file.write(line)
        remove(file)
        move(abs_path, file)
    else:
        with open(file) as f:
            content = f.readlines()
        # strip \n chars
        content = [x.strip() for x in content]

        # keeps track of how many lines are processed in total in loop
        count_lines = 0

        for count, chapter_num in enumerate(rsplit):
            if count == len(rsplit) - 1:
                break

            initial_time = datetime.time()

            file_name = file_name_format.replace("%n", str(count + offset).zfill(3))
            with open(file_name + '.txt', 'w') as output_file:
                # loop over sliced list of lines
                for inner_count, line in enumerate(content[chapter_num * 2:]):
                    count_lines = count_lines + 1

                    # time is now line_time[1]
                    line_time = line.split("=")

                    # Extract chapter number through math (could be done with EZ regex too)
                    chap_num = str(math.ceil((inner_count + 1) / 2)).zfill(2)

                    # Alter chapter number if not first file
                    if count > 0:
                        begin_line = "CHAPTER" + chap_num
                    else:
                        # need to get rid of any existing chapter titles if --title
                        if names:
                            begin_line = line if inner_count % 2 == 0 else line.split("=")[0] + "="
                        else:
                            begin_line = line

                    # Adjust time for every other line
                    if inner_count % 2 == 0:
                        begin_line = begin_line.split("=")[0]

                        if inner_count == 0:
                            # start with time of 00:00:00.000
                            ex_time = datetime.time()
                            # first time line = initial time to adjust by
                            initial_time = line_time[1]
                            initial_time = datetime.datetime.strptime(initial_time, "%H:%M:%S.%f")
                        else:
                            ex_time = line_time[1]
                            ex_time = datetime.datetime.strptime(ex_time, "%H:%M:%S.%f")
                            # creates a datetime.timedelta when subtracting two datetime.time
                            ex_time = ex_time - initial_time

                        # Have to print datetime.time differently than datetime.timedelta
                        if isinstance(ex_time, datetime.time):
                            the_time = ex_time.strftime("%H:%M:%S.%f")[:-3]
                            output_file.write(begin_line + "=" + the_time)
                        else:
                            if str(ex_time)[-1] == "0":
                                the_time = "0" + str(ex_time)[:-3]
                            else:
                                the_time = str(ex_time)[:-3]
                            output_file.write(begin_line + "=" + the_time)
                    else:
                        # count > 0 needs "NAME" because I hacked the beginning of the line earlier
                        if count > 0:
                            output_file.write(begin_line + "NAME=")
                        else:
                            output_file.write(begin_line)

                        if names:
                            output_file.write("Chapter " + chap_num)

                    # if line num = chapter number of end specified in split, break
                    if count_lines == rsplit[count + 1] * 2:
                        break
                    output_file.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a eac3to BD chapter file into new chapter files")
    parser.add_argument('file', nargs=1)
    parser.add_argument('--indexes', '-i', help="Indexes to split the files at")
    parser.add_argument('--offset', '-o', type=int, default=1, help="Number to start file numbering at. Default 1")
    parser.add_argument('--file-name', '-f', dest="file_name", default="chapters%n",
                        help="Name format for generated files. Use %n to specify number location. Defaults to chapters%n")
    parser.add_argument('--titles', action="store_true", help="Set if you want to set generic chapter titles.")
    parser.add_argument('--only-titles', dest="only_titles", action="store_true",
                        help="Set for only doing generic chapter titles. Ignores all other arguments and edits the same file as given.")
    args = parser.parse_args()

    split = None
    if not args.only_titles:
        split = [int(n) for n in args.indexes.split(',')]
    # don't really gotta pass any of these with this scope
    split_file(args.file[0], args.titles, args.only_titles, split, args.offset, args.file_name)
