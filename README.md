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

## Compiling the Dataset

### Downloading from YouTube
To download from YouTube, use the youtube_downloader.sh script provided. First
make sure you have Python, and youtube-dl installed.

To install youtube-dl, you can use the command:

```
pip install youtube-dl
```

To run the code, make sure you have librosa installed. To install librosa, you
can use the command:

```
pip install librosa
```


## Building the Model
TBD

## Training the Model
TBD


## Troubleshooting
ERROR: ffprobe/avprobe and ffmpeg/avconv not found. Please install one.

Download ffmpeg from https://www.gyan.dev/ffmpeg/builds/ and move the
executables in the bin/ folder to the Python Scripts/ folder.
https://stackoverflow.com/a/63127380


## Testing and Evaluating the Model
TBD