from glob import glob
from ffprobe3 import FFProbe
import datetime
import math
import sys
import os
import argparse


def split_by_video(file, names, videos, offset=1, file_name_format="chapters%n"):
    """ Wrapper for split.py that accepts video files as input and calls split.split_files based on indexes found by video times """

    # expand wildcard for Windows, convert to path
    videos = [os.path.normpath(x) for b in videos for x in glob(b)]

    print("Getting video lengths...")
    video_lengths = []
    for filename in videos:
        video_lengths.append(getLength(filename))

    parse_file(file, video_lengths)


def getLength(filename):
    """Returns length of file to the microsecond using ffprobe"""
    return FFProbe(filename).streams[0].duration


def convert_times(times):
    """ Convert times from ffprobe so they're usable by datetime """
    new_times = []
    for t in times:
        # Doing manual math to convert seconds above 60 to minutes and seconds. Probably could've been done with timedeltas
        big_seconds = t.split(".")
        mth = int(big_seconds[0]) / 60
        frac, whole = math.modf(mth)

        # New format - minutes.seconds.microseconds
        new_times.append(str(int(whole)) + "." + str(int(frac*60)) + "." + big_seconds[1])
    return new_times


def parse_file(file, times):
    """ Read chapter file and find the time for each episode in successive order. Returns index to split at"""

    total_time = datetime.timedelta(0,0)
    indexes = []
    time_arr_index = 0
    first = None

    times = convert_times(times)
    # convert times array to datetime objects
    times = [datetime.datetime.strptime(t, "%M.%S.%f") for t in times]

    with open(file) as f:
        # Remove blank lines since I work with len(content)
        content = [line for line in f.readlines() if line.strip()]

    # strip \n chars
    content = [x.strip() for x in content]

    for count, line in enumerate(content):
        if first == None:
            if count == 0:
                first = 0
            else:
                first = math.ceil((count+1)/2)

        # Get time and compare to time in times[]
        if count % 2 == 0:
            # time is now line_time[1]
            line_time = line.split("=")

            dt_line = datetime.datetime.strptime(line_time[1], "%H:%M:%S.%f")

            # Compare time to time in times[time_arr_index] - within two seconds. Duration may need to change.
            if dt_line - datetime.timedelta(0, 2) <= times[time_arr_index] + total_time <= dt_line + datetime.timedelta(0, 2):
                total_time += times[time_arr_index]
                time_arr_index += 1

                indexes.extend([first, math.ceil((count+1)/2)])
                first = None

            if time_arr_index+1 > len(times):
                # we done, add indexes for whats remaining
                if count+2 < len(content):
                    indexes.extend([math.ceil((count+1)/2)+1, int(len(content)/2)])
                    break

    print(indexes)
    return indexes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wrapper for splitting files based on video times")
    parser.add_argument('file', nargs=1)
    parser.add_argument('--videos', '-i', nargs="*", help="Video files. Their lengths act as splitting indexes")
    parser.add_argument('--offset', '-o', type=int, default=1, help="Number to start file numbering at. Default 1")
    parser.add_argument('--file-name', '-f', dest="file_name", default="chapters%n",
                        help="Name format for generated files. Use %n to specify number location. Defaults to chapters%n")
    parser.add_argument('--titles', action="store_true", help="Set if you want to set generic chapter titles.")

    args = parser.parse_args()

    split_by_video(args.file[0], args.titles, args.videos, args.offset, args.file_name)
