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

        initial_time = 0

        with open('chapters' + str(count+1) + '.txt', 'w') as output_file:
            # loop over sliced list of lines
            for inner_count, line in enumerate(content[chapter_num*2:]):
                count_lines = count_lines + 1

                # Adjust time on odd number lines
                if count_lines % 2 == 0:
                    output_file.write(line)
                else:
                    # split line into before and after =
                    # time is now line_time[1]
                    line_time = line.split("=")

                    if inner_count == 1:
                        # first time line = initial time to adjust by
                        initial_time = line_time[1]
                        time = "00:00:00:00"
                    else:
                        time = line_time[1] - initial_time
                    output_file.write(line_time[0]+"="+time)

                # if line num = chapter number of end, break
                if count_lines == split[count+1] * 2:
                    break
                output_file.write("\n")


# Define what each episodes last chapter is (need 0 and last chapter)
# for my example, 0-4,5-9,10-15,16-18
split = [0,4,9,15,18]

split_file(sys.argv[-1])