import argparse
import datetime
import math
import os
import sys
from glob import glob

# github.com/nickerokhin/ffprobe3 gives mkv support with TAG:DURATION
from ffprobe3 import FFProbe

from split import split_file


def split_by_video(file, names, videos, offset=1, file_name_format="chapters%n"):
    """ Wrapper for split.py that accepts video files as input and calls split.split_files based on indexes found by video times """

    # expand wildcard for Windows, convert to path
    videos = [os.path.normpath(x) for b in videos for x in glob(b)]

    print("Getting video lengths...")
    video_lengths = []
    for filename in videos:
        video_lengths.append(getLength(filename))

    print("Video lengths: {}".format(video_lengths))
    indexes = parse_file(file, video_lengths)
    # Split!
    print("Splitting files")
    split_file(file, names, False, indexes, offset, file_name_format)


def getLength(filename):
    """Returns length of file to the microsecond using ffprobe"""
    return FFProbe(filename).streams[0].duration_seconds()


def convert_times(times):
    """ Convert times from ffprobe so they're usable by datetime """
    new_times = []
    for t in times:
        # Doing manual math to convert seconds above 60 to minutes and seconds. Probably could've been done with timedeltas
        t = str(t)
        big_seconds = t.split(".")
        mth = int(big_seconds[0]) / 60
        frac, whole = math.modf(mth)

        # New format - minutes.seconds.microseconds
        new_times.append(str(int(whole)) + "." + str(int(frac * 60)) + "." + big_seconds[1])
    return new_times


def parse_file(file, times):
    """ Read chapter file and find the time for each episode in successive order. Returns index to split at"""

    total_time = datetime.timedelta(0, 0)
    indexes = []
    time_arr_index = 0
    first = False

    times = convert_times(times)
    # convert times array to datetime objects
    times = [datetime.datetime.strptime(t, "%M.%S.%f") for t in times]

    with open(file) as f:
        # Remove blank lines since I work with len(content)
        content = [line for line in f.readlines() if line.strip()]

    # strip \n chars
    content = [x.strip() for x in content]

    for count, line in enumerate(content):

        # Get time and compare to time in times[]
        if count % 2 == 0:
            # time is now line_time[1]
            line_time = line.split("=")

            dt_line = datetime.datetime.strptime(line_time[1], "%H:%M:%S.%f")

            # Compare time to time in times[time_arr_index]. Duration may need to change for range
            dt_line_adjusted = [dt_line - datetime.timedelta(0, len(indexes) + 2), dt_line + datetime.timedelta(0, len(indexes) + 2)]
            if dt_line_adjusted[0] <= times[time_arr_index] + total_time <= dt_line_adjusted[1]:
                # Since I didn't use timedeltas for dates in the first place like I should have, will convert to timedelta
                # and then add to total_time so that I can add datetimes (impossible without using timedeltas)
                ti = times[time_arr_index]
                total_time += datetime.timedelta(hours=ti.hour, minutes=ti.minute, seconds=ti.second,
                                                 microseconds=ti.microsecond)

                time_arr_index += 1
                if first:
                    indexes.append(math.ceil((count + 1) / 2))
                else:
                    indexes.extend([0, math.ceil((count + 1) / 2)])
                first = True

            # check if second to last line - if so, and it didnt work in the first if condition, just ignore
            # because this means there isnt a chapter for the end of the last video file time
            elif count + 2 == len(content):
                time_arr_index += 1
                indexes.append(math.ceil((count + 1) / 2))

        elif time_arr_index + 1 > len(times):
            # we done, add indexes for whats remaining
            if count + 2 < len(content):
                indexes.append(int(len(content) / 2))
            print("\nUsing indexes {}".format(indexes))
            break

        # If this is true, is bad, exit.
        elif count + 1 == len(content) and time_arr_index + 1 <= len(times):
            print("\nDid not find a matching chapter for time {0} (video file number {1}). Exiting".format(
                times[time_arr_index], time_arr_index + 1))
            print("Debug indexes: {}".format(indexes))
            sys.exit(1)

    return indexes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper for splitting files based on video times")
    parser.add_argument('file', nargs=1)
    parser.add_argument('--video', '-i', nargs="*", help="Video files. Their lengths act as splitting indexes")
    parser.add_argument('--offset', '-o', type=int, default=1, help="Number to start file numbering at. Default 1")
    parser.add_argument('--file-name', '-f', dest="file_name", default="chapters%n",
                        help="Name format for generated files. Use %n to specify number location. Defaults to chapters%n")
    parser.add_argument('--titles', action="store_true", help="Set if you want to set generic chapter titles.")

    args = parser.parse_args()

    split_by_video(args.file[0], args.titles, args.video, args.offset, args.file_name)
