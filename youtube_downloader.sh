# This script downloads the audio files from Youtube to be used for training
# the model. It uses the free youtube-dl tool

mkdir MusicData
cd MusicData/

# Mondstadt
mkdir Mondstadt
cd Mondstadt/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT0iD2rtznph5p3sXGo7j-IL
cd ..

# Dragonspine
mkdir Dragonspine
cd Dragonspine/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1d3emY6Otllgv7nS3ny5V4
cd ..

# Liyue
mkdir Liyue
cd Liyue/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1KKhS4B_Mz9xcTxVMHXaji
cd ..

# Chasm
mkdir Chasm
cd Chasm/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT0DpKGwfg03hkotEoPY9DCM
cd ..

# Inazuma
mkdir Inazuma
cd Inazuma/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT2I6Ylrv6DXsq1x6ix7Pe3k
cd ..

# Sumeru Rainforest
mkdir SumeruRainforest
cd SumeruRainforest/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT17GobBqo0e2ml3XRcB2veI
cd ..

# Sumeru Desert
mkdir SumeruDesert
cd SumeruDesert/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1Yh34NEyIJhXVcfeHrnDjq
cd ..

# Ocean
mkdir Ocean
cd Ocean/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1pV4YGsiqDdsYl-PD7gxa-
cd ..

# Enkanomiya
mkdir Enkanomiya
cd Enkanomiya/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1bmyU1kPi1p9VwOD2ZP8ov
cd ..

# Other
mkdir Other
cd Other/
youtube-dl --ignore-errors --prefer-ffmpeg --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail https://youtube.com/playlist?list=PLP2Zo4nJwCT1heLZ9COXk-_oLERCcKVgt
cd ..
