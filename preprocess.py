from asyncore import loop
import os
import librosa

# This file standardizes the set of audio data by making them all exactly one
# minute long. If the file is:
# 1) Less than one minute long, it will be looped to be exactly one minute
#    long.
# 2) Greater than one minute long, it will be split at the one minute mark and
#    the remaining data will be handled like case 1.
# 3) Multiple minutes long, it will be divided equally into one minute segments
#    and the last clip will be handled like case 1.

# Run with
# `python preprocess.py`
# Modified from
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/12-%20Music%20genre%20classification%3A%20Preparing%20the%20dataset/code/extract_data.py
# 
# Youtube course video
# https://www.youtube.com/watch?v=_xcFAiufwd0&list=PL-wATfeyAMNrtbkCNsLcpoAyBBRJZVlnf&index=13

DATASET_PATH = ""
SAMPLE_RATE = 22050
NUM_SAMPLES_ONE_MIN = SAMPLE_RATE * 60

def preprocess(dataset_path):
    # Walk through folders in the directory
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        
        # Make sure we are only looking at sub folders.
        if dirpath is not dataset_path:

            for file in filenames:

                file_path = os.path.join(dirpath, file)
                signal, _ = librosa.load(file_path, sr=SAMPLE_RATE)
                print(file_path)
                # print("Signal: " + str(signal[:10]))

                # Figure out length
                signal, _ = librosa.load(file_path, sr=SAMPLE_RATE)
                signal_len_seconds = int(librosa.get_duration(y=signal, sr=SAMPLE_RATE))

                # If longer than 1 min, send to splitIntoMinutes
                if signal_len_seconds > 60:
                    splitIntoMinutes(signal)
                # If less than 1 min, send to loopToOneMinute
                elif signal_len_seconds < 60:
                    loopToOneMinute(signal)
                # The song is less than 61 seconds long, leave as is
                else:
                    storeSong(signal)

def loopToOneMinute(song):
    loopedSong = []
    while (len(loopedSong) < NUM_SAMPLES_ONE_MIN):
        loopedSong.append(song)

    print("Looped Song length: " + str(len(loopedSong)))

    storeSong(loopedSong)

def splitIntoMinutes(song):
    secondsLength = librosa.get_duration(y=song, sr=SAMPLE_RATE)
    minuteIntervals = [(i, i+ 60) for i in range(0, int(secondsLength / 60))]

    i = 0
    for interval in minuteIntervals:
        print("Storing Minute " + str(i) + " of song.")
        # Get data for the relevant interval
        intervalSong = song[interval[0]:interval[1]]
        storeSong(intervalSong)
        i += 1

    lastSong = song[int(secondsLength / 60):int(secondsLength) % 60]

    # Only create a new looped song if the remaining audio data is significant
    # which we define here to be greater than 10 seconds long.
    if (len(lastSong) > SAMPLE_RATE * 10):
        loopToOneMinute(lastSong)

def storeSong(song):
    # Store song into training data folder
    truncated_song = song[:NUM_SAMPLES_ONE_MIN]
    var = 0

if __name__ == "__main__":
    print("Running program")
    preprocess(DATASET_PATH)