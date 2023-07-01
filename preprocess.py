import os
import librosa
import json
import numpy as np
import random

# This file standardizes the set of audio data by making them all exactly ten
# seconds long. If the file is:
# 1) Less than 10 seconds long, it will be looped to be exactly 10 seconds
#    long.
# 2) Greater than 10 seconds long but less than 20, it will be split at
#    the 10 second mark and the remaining data will be handled like case 1.
# 3) Greater than 20 seconds long, it will be divided equally into 10 second
#    segments and the last clip will be handled like case 1.
 
# Based off of
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/12-%20Music%20genre%20classification%3A%20Preparing%20the%20dataset/code/extract_data.py
# 
# Youtube course video
# https://youtu.be/szyGiObZymo

DATASET_PATH = ""
SAMPLE_RATE = 22050 # per second
DATA_WINDOW = 10 # seconds
NUM_SAMPLES_ONE_WINDOW = SAMPLE_RATE * DATA_WINDOW
JSON_PATH = ""
DATA = {
        "mapping": [],
        "labels": [],
        "mfcc": []
    }

# This dictionary helps when we bootstrap the data. It stores the factor by
# which we need to bootstrap music from a certain area so that we have
# approximately the same amount of data from each area.
LABEL_WEIGHT_DICT = {
        "Dragonspine": 5,
        "Inazuma": 1,
        "Mondstadt": 3,
        "SumeruDesert": 1,
        "Enkanomiya": 6,
        "Liyue": 1,
        "Ocean": 6,
        "SumeruRainforest": 1
    }

def preprocess(dataset_path):
    # Walk through folders in the directory
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        
        # Make sure we are only looking at sub folders.
        if dirpath is not dataset_path:
            
            label = dirpath.split("\\")[-1]
            labelIndex = i - 1

            # Bootstrap the data since the number of songs we have from each
            # game area is not the same
            bootstrappedFileNames = []
            lenFilenames = len(filenames)
            while len(bootstrappedFileNames) < lenFilenames * LABEL_WEIGHT_DICT[label]:
                bootstrappedFileNames.append(filenames[random.randrange(lenFilenames)])

            for file in filenames:

                filePath = os.path.join(dirpath, file)
                signal, _ = librosa.load(filePath, sr=SAMPLE_RATE)
                print(filePath)
                # print("Signal: " + str(signal[:10]))

                # Figure out length
                signal, _ = librosa.load(filePath, sr=SAMPLE_RATE)
                signalLenSeconds = int(librosa.get_duration(y=signal, sr=SAMPLE_RATE))

                for j in range(LABEL_WEIGHT_DICT[label]):
                    # If longer than 1 window, send to splitIntoMinutes
                    if signalLenSeconds > DATA_WINDOW:
                        splitIntoWindows(signal, label, labelIndex)
                    # If less than 1 min, send to loopToOneMinute
                    elif signalLenSeconds < DATA_WINDOW:
                        loopToOneWindow(signal, label, labelIndex)
                    # The song is less than 61 seconds long, leave as is
                    else:
                        storeSong(signal, label, labelIndex)
    
    # save MFCCs to json file
    with open(JSON_PATH, "w") as fp:
        json.dump(DATA, fp, indent=4)

def loopToOneWindow(song, label, labelIndex):
    loopedSong = []
    while (len(loopedSong) < NUM_SAMPLES_ONE_WINDOW):
        loopedSong.extend(song)

    storeSong(np.array(loopedSong), label, labelIndex)

def splitIntoWindows(song, label, labelIndex):
    secondsLength = librosa.get_duration(y=song, sr=SAMPLE_RATE)
    segmentIntervals = [(i * NUM_SAMPLES_ONE_WINDOW, (i + 1) * NUM_SAMPLES_ONE_WINDOW) for i in range(0, int(secondsLength / DATA_WINDOW))]

    i = 0
    for interval in segmentIntervals:
        print("Storing Segment " + str(i) + " of song.")

        # Get data for the relevant interval
        intervalSong = song[interval[0]:interval[1]]

        storeSong(intervalSong, label, labelIndex)
        i += 1

    lastSong = song[int(secondsLength / DATA_WINDOW):int(secondsLength) % DATA_WINDOW]

    # Only create a new looped song if the remaining audio data is significant
    # which we define here to be greater than 20% of the data window size.
    if (len(lastSong) > SAMPLE_RATE * DATA_WINDOW / 5):
        loopToOneWindow(lastSong, label, labelIndex)

def storeSong(song, label, labelIndex):
    # Store song into training data folder
    print("Storing song of length: " + str(len(song)))
    truncatedSong = song[:NUM_SAMPLES_ONE_WINDOW]

    DATA["mapping"].append(label)
    DATA["labels"].append(labelIndex)

    # Extract Mel Frequency Cepstral Coefficients
    mfcc = librosa.feature.mfcc(y=truncatedSong, sr=SAMPLE_RATE, n_mfcc=13, n_fft=2048, hop_length=512)

    DATA["mfcc"].append(mfcc.tolist())


if __name__ == "__main__":
    print("Running program")

    print("Clearing data")
    DATA = {
        "mapping": [],
        "labels": [],
        "mfcc": []
    }

    print("Starting preprocessing")
    preprocess(DATASET_PATH)
    print("Finished preprocessing")