import sys

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

        with open('chapters' + str(count+1) + '.txt', 'w') as output_file:
            # loop over sliced list of lines
            for line in content[chapter_num*2:]:
                count_lines = count_lines + 1

                output_file.write(line)
                # if line num = chapter number of end, break
                if count_lines == split[count+1] * 2:
                    break
                output_file.write("\n")


# Define what each episodes last chapter is (need 0 and last chapter)
# for my example, 0-4,5-9,10-15,16-18
split = [0,4,9,15,18]

split_file(sys.argv[-1])