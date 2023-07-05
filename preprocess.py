import filepaths
import json
import librosa
import numpy as np
import os
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

DATASET_PATH = filepaths.RAW_DATA_PATH
SAMPLE_RATE = 22050 # per second
DATA_WINDOW = 10 # seconds
NUM_SAMPLES_ONE_WINDOW = SAMPLE_RATE * DATA_WINDOW
JSON_PATH = filepaths.DATASET_PATH
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
        "SumeruRainforest": 1,
        "Temp": 1
    }

def preprocess(dataset_path, json_path):
    # Walk through folders in the directory
    for i, (dir_path, dir_names, file_names) in enumerate(os.walk(dataset_path)):
        
        # Make sure we are only looking at sub folders.
        if dir_path is not dataset_path:
            
            label = dir_path.split("\\")[-1]
            label_index = i - 1

            # Bootstrap the data since the number of songs we have from each
            # game area is not the same
            bootstrapped_file_names = []
            len_file_names = len(file_names)
            while len(bootstrapped_file_names) < len_file_names * LABEL_WEIGHT_DICT[label]:
                bootstrapped_file_names.append(file_names[random.randrange(len_file_names)])

            for file in file_names:

                file_path = os.path.join(dir_path, file)
                signal, _ = librosa.load(file_path, sr=SAMPLE_RATE)
                print(file_path)

                # Figure out length
                signal, _ = librosa.load(file_path, sr=SAMPLE_RATE)
                signal_len_seconds = int(librosa.get_duration(y=signal, sr=SAMPLE_RATE))

                for j in range(LABEL_WEIGHT_DICT[label]):
                    # If longer than 1 window, send to splitIntoMinutes
                    if signal_len_seconds > DATA_WINDOW:
                        split_into_segments(signal, label, label_index)
                    # If less than 1 min, send to loopToOneMinute
                    elif signal_len_seconds < DATA_WINDOW:
                        loop_to_one_segment(signal, label, label_index)
                    # The song is less than 61 seconds long, leave as is
                    else:
                        store_song(signal, label, label_index)
    
    # save MFCCs to json file
    with open(json_path, "w") as fp:
        json.dump(DATA, fp, indent=4)

def loop_to_one_segment(song, label, label_index):
    looped_song = []
    while (len(looped_song) < NUM_SAMPLES_ONE_WINDOW):
        looped_song.extend(song)

    store_song(np.array(looped_song), label, label_index)

def split_into_segments(song, label, label_index):
    seconds_length = librosa.get_duration(y=song, sr=SAMPLE_RATE)
    segment_intervals = [(i * NUM_SAMPLES_ONE_WINDOW, (i + 1) * NUM_SAMPLES_ONE_WINDOW) for i in range(0, int(seconds_length / DATA_WINDOW))]

    i = 0
    for interval in segment_intervals:
        print("Storing Segment " + str(i) + " of song.")

        # Get data for the relevant interval
        intervalSong = song[interval[0]:interval[1]]

        store_song(intervalSong, label, label_index)
        i += 1

    last_song = song[int(seconds_length / DATA_WINDOW):int(seconds_length) % DATA_WINDOW]

    # Only create a new looped song if the remaining audio data is significant
    # which we define here to be greater than 20% of the data window size.
    if (len(last_song) > SAMPLE_RATE * DATA_WINDOW / 5):
        loop_to_one_segment(last_song, label, label_index)

def store_song(song, label, label_index):
    # Store song into training data folder
    print("Storing song of length: " + str(len(song)))
    truncated_song = song[:NUM_SAMPLES_ONE_WINDOW]

    DATA["mapping"].append(label)
    DATA["labels"].append(label_index)

    # Extract Mel Frequency Cepstral Coefficients
    mfcc = librosa.feature.mfcc(y=truncated_song, sr=SAMPLE_RATE, n_mfcc=13, n_fft=2048, hop_length=512)

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
    preprocess(DATASET_PATH, JSON_PATH)
    print("Finished preprocessing")