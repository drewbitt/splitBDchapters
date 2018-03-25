import sys
import datetime

def split_file(file, offset=0):
    with open(file) as f:
        content = f.readlines()
    # strip \n chars
    content = [x.strip() for x in content]

    # keeps track of how many lines are processed in total in loop
    count_lines = 0

    for count, chapter_num in enumerate(split):
        if count == len(split)-1:
            break

        initial_time = datetime.time()

        with open('chapters' + str(count+1+offset) + '.txt', 'w') as output_file:
            # loop over sliced list of lines
            for inner_count, line in enumerate(content[chapter_num*2:]):
                count_lines = count_lines + 1

                # Adjust time for every other line
                if inner_count % 2 == 0:
                    # split line into before and after =
                    # time is now line_time[1]
                    line_time = line.split("=")

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
                        output_file.write(line_time[0]+"="+the_time)
                    else:
                        if str(ex_time)[-1] == "0":
                            the_time = "0" + str(ex_time)[:-3]
                        else:
                            the_time = str(ex_time)[:-3]
                        output_file.write(line_time[0]+"="+the_time)

                else:
                    output_file.write(line)

                # if line num = chapter number of end specified in split, break
                if count_lines == split[count+1] * 2:
                    break
                output_file.write("\n")


split = [int(n) for n in sys.argv[1].split(',')]

if len(sys.argv) == 4:
    split_file(sys.argv[2],int(sys.argv[3]))
else:
    split_file(sys.argv[2])