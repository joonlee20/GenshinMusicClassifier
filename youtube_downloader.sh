# This script downloads the audio files from Youtube to be used for training
# the model. It uses the free youtube-dl tool

mkdir MusicData
cd MusicData/
# Mondstadt

# Dragonspine
mkdir Dragonspine
cd Dragonspine/
youtube-dl --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1d3emY6Otllgv7nS3ny5V4
cd ..

# Liyue
# Chasm
# Inazuma
# Sumeru Rainforest
# Sumeru Desert