import librosa

# This file standardizes the set of audio data by making them all exactly one
# minute long. If the file is:
# 1) Less than one minute long, it will be looped to be exactly one minute
#    long.
# 2) Greater than one minute long, it will be split at the one minute mark and
#    the remaining data will be handled like case 1.
# 3) Multiple minutes long, it will be divided equally into one minute segments
#    and the last clip will be handled like case 1.

def preprocess():
    # Get folder path of all music data
    for folder in folderPath:
        for file in folder:
            # Figure out length
            song = librosa.load(file)
            secondsLength = librosa.get_duration(song)

            # If longer than 1 min, send to splitIntoMinutes
            if secondsLength > 60:
                splitIntoMinutes(song)

            # If less than 1 min, send to loopToOneMinute
            else:
                loopToOneMinute(song)

def loopToOneMinute(song):
    secondsLength = librosa.get_duration(song)
    secondsToLoop = 60 - secondsLength
    # Get audio data from 0 to secondsToLoop
    # Append audio data to song
    # loopedSong = song + loopedData
    # storeSong(loopedSong)

def splitIntoMinutes(song):
    secondsLength = librosa.get_duration(song)
    minuteIntervals = [(i, i+ 60) for i in range(0, secondsLength / 60)]
    for interval in minuteIntervals:
        # Get data for the relevant interval
        # intervalSong = song[interval.getFirst(), interval.getSecond]
        # storeSong(intervalSong)
    # lastSong = song[secondsLength / 60, secondsLength % 60]
    # loopToOneMinute(lastSong)

def storeSong(song):
    # Store song into training data folder
    var = 0