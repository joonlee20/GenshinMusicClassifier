import os
import librosa
import json

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
# 
# Based off of
# https://github.com/musikalkemist/DeepLearningForAudioWithPython/blob/master/12-%20Music%20genre%20classification%3A%20Preparing%20the%20dataset/code/extract_data.py
# 
# Youtube course video
# https://www.youtube.com/watch?v=_xcFAiufwd0&list=PL-wATfeyAMNrtbkCNsLcpoAyBBRJZVlnf&index=13

DATASET_PATH = ""
SAMPLE_RATE = 22050
NUM_SAMPLES_ONE_MIN = SAMPLE_RATE * 60
JSON_PATH = ""
DATA = {
        "mapping": [],
        "labels": [],
        "mfcc": []
    }

def preprocess(dataset_path):
    # Walk through folders in the directory
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dataset_path)):
        
        # Make sure we are only looking at sub folders.
        if dirpath is not dataset_path:
            
            label = dirpath.split("\\")[-1]
            labelIndex = i - 1

            for file in filenames:

                filePath = os.path.join(dirpath, file)
                signal, _ = librosa.load(filePath, sr=SAMPLE_RATE)
                print(filePath)
                # print("Signal: " + str(signal[:10]))

                # Figure out length
                signal, _ = librosa.load(filePath, sr=SAMPLE_RATE)
                signalLenSeconds = int(librosa.get_duration(y=signal, sr=SAMPLE_RATE))

                # If longer than 1 min, send to splitIntoMinutes
                if signalLenSeconds > 60:
                    splitIntoMinutes(signal, label, labelIndex)
                # If less than 1 min, send to loopToOneMinute
                elif signalLenSeconds < 60:
                    loopToOneMinute(signal, label, labelIndex)
                # The song is less than 61 seconds long, leave as is
                else:
                    storeSong(signal, label, labelIndex)
    
    # save MFCCs to json file
    with open(JSON_PATH, "w") as fp:
        json.dump(DATA, fp, indent=4)

def loopToOneMinute(song, label, labelIndex):
    loopedSong = []
    while (len(loopedSong) < NUM_SAMPLES_ONE_MIN):
        loopedSong.append(song)

    print("Looped Song length: " + str(len(loopedSong)))

    storeSong(loopedSong, label, labelIndex)

def splitIntoMinutes(song, label, labelIndex):
    secondsLength = librosa.get_duration(y=song, sr=SAMPLE_RATE)
    minuteIntervals = [(i * NUM_SAMPLES_ONE_MIN, (i + 1) * NUM_SAMPLES_ONE_MIN) for i in range(0, int(secondsLength / 60))]

    i = 0
    for interval in minuteIntervals:
        print("Storing Minute " + str(i) + " of song.")
        # Get data for the relevant interval
        intervalSong = song[interval[0]:interval[1]]
        storeSong(intervalSong, label, labelIndex)
        i += 1

    lastSong = song[int(secondsLength / 60):int(secondsLength) % 60]

    # Only create a new looped song if the remaining audio data is significant
    # which we define here to be greater than 10 seconds long.
    if (len(lastSong) > SAMPLE_RATE * 10):
        loopToOneMinute(lastSong, label, labelIndex)

def storeSong(song, label, labelIndex):
    # Store song into training data folder
    print("Storing song of length: " + str(len(song)))
    truncatedSong = song[:NUM_SAMPLES_ONE_MIN]

    DATA["mapping"].append(label)
    DATA["labels"].append(labelIndex)

    # Extract Mel Frequency Cepstral Coefficients
    mfcc = librosa.feature.mfcc(y=truncatedSong, sr=SAMPLE_RATE, n_mfcc=13, n_fft=2048, hop_length=512)
    print("MFCC length: " + str(len(mfcc.tolist()[0])))
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