import sys
import datetime

def split_file(file):
    with open(file) as f:
        content = f.readlines()
    # strip \n chars
    content = [x.strip() for x in content]

    # keeps track of how many lines one by one are processed
    count_lines = 0

    for count, chapter_num in enumerate(split):
        # handling access out of bounds
        if count== len(split)-1:
            break

        initial_time = datetime.time()

        with open('chapters' + str(count+1) + '.txt', 'w') as output_file:
            # loop over sliced list of lines
            for inner_count, line in enumerate(content[chapter_num*2:]):
                count_lines = count_lines + 1

                # Adjust time for every other line
                if inner_count % 2 == 0:
                    # split line into before and after =
                    # time is now line_time[1]
                    line_time = line.split("=")

                    if inner_count == 0:
                        ex_time = datetime.time()
                        # first time line = initial time to adjust by
                        initial_time = line_time[1]
                        initial_time = datetime.datetime.strptime(initial_time, "%H:%M:%S.%f")
                    else:
                        ex_time = line_time[1]
                        ex_time = datetime.datetime.strptime(ex_time, "%H:%M:%S.%f")
                        # creates a datetime.timedelta when subtracting two datetime.time
                        ex_time = ex_time - initial_time

                    if isinstance(ex_time, datetime.time):
                        print(ex_time.strftime("%H:%M:%S.%f")[:-3])
                    else:
                        # is timedelta
                        if (str(ex_time)[-1] == "0"):
                            print("0" + str(ex_time)[:-3])
                    # output_file.write(line_time[0]+"="+ex_time)
                else:
                    output_file.write(line)

                # if line num = chapter number of end, break
                if count_lines == split[count+1] * 2:
                    break
                output_file.write("\n")


# Define what each episodes last chapter is (need 0 and last chapter)
# for my example, 0-4,5-9,10-15,16-18
split = [0,4,9,15,18]

split_file(sys.argv[-1])