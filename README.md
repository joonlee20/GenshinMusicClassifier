# Genshin Music Classifier

This is a project to classify music from different regions in the video game
Genshin Impact.

Special thanks to the Sound of AI Youtube channel
(https://www.youtube.com/@ValerioVelardoTheSoundofAI) 
for providing the background knowledge necessary for this project. In
particular, the two courses I learned from were:

- Audio Signal Processing for Machine Learning
  https://youtube.com/playlist?list=PL-wATfeyAMNqIee7cH3q1bh4QJFAaeNv0
- Deep Learning (for Audio) with Python
  https://youtube.com/playlist?list=PL-wATfeyAMNrtbkCNsLcpoAyBBRJZVlnf

Below is a breakdown of the different steps involved for each stage of the
project:

### Downloading from YouTube
To download from YouTube, use the youtube_downloader.sh script provided. First
make sure you have Python, and youtube-dl installed.

## Compiling the Dataset
To create the dataset, I manually listened to songs on Youtube and organized
them into playlists. You can see the links to those playlists in the youtube
downloader shell script.

More details can be seen in the preprocess.py script, but once I had the raw
audio files, I did the following:
- Standardize the length of the clips, which meant either looping clips that
  were too short, or splitting up clips that were too long
- Bootstrap the data since I did not have equal quantities of songs from each
  area
- Extract the Mel Cepstrum Frequency Coefficients (MFCCs), which turn the audio
  wave data into a format more suitable for Deep Learning
- Store the MFCC data into a JSON file

## Models and Results
So far, I have tried three models:

### Simple Neural Networks
Initially, I tried the same network as the one used in the course video since
that network was also used to classify 10 genres of music. However, this only
had around 20-30% accuracy so I wanted to tweak the layers and neurons.

After seeing a post on StackOverflow, I decided to try only one hidden layer.
This hidden layer had a size of half the input layer and ended up having 40%
test accuracy. As mentioned in the "Compiling the Dataset" section, I realized
that the data distribution also may have been impacting the quality of the
model since, for example, I had 100 songs from one region and only 15 songs
from another. With bootstrapping, the test accuracy increased to 60%. 

### Convolutional Neural Network
A later video in the Deep Learning Youtube course uses a CNN, and I tried using
the same model for this project. This helped increase the test accuracy to 70%.

For graphs of the results, they can be seen in the Results/ folder of this
project.

## Troubleshooting
To run the youtube downloader script, make sure you have youtube-dl installed.
You can use the command:
```
pip install youtube-dl
```

To run the code related to audio processing, make sure you have librosa
installed. You can use the command:
```
pip install librosa
```

If you encounter an error like: "ERROR: ffprobe/avprobe and ffmpeg/avconv not
found. Please install one."

Download ffmpeg from https://www.gyan.dev/ffmpeg/builds/ and move the
executables in the bin/ folder to the Python Scripts/ folder.
https://stackoverflow.com/a/63127380

## Prediction
Stretch goal

## Generate New Songs for Specific Areas
Stretch goal