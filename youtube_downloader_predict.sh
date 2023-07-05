#!/bin/sh

rm -r TempMusicData/
mkdir TempMusicData/
cd TempMusicData/
mkdir Temp
cd Temp/
echo $1
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail $1
cd ..