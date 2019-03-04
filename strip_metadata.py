#!/usr/bin/env python3

import os
## Strips metadata from all audio files in top 2 levels of AUDIO_FOLDER folder
## This is an optional step. Some wav files have metadata that causes the DisVoice feature extraction step to fail
## Requires FFMPEG
AUDIO_FOLDER = 'audio'


# Iterate through all actor folders and then audio files
for actor_folder in os.listdir(AUDIO_FOLDER):
    actor_folderpath = os.path.join(os.getcwd(), AUDIO_FOLDER, actor_folder)
    for audio_filename in os.listdir(actor_folderpath):
        audio_filepath = os.path.join(actor_folderpath, audio_filename)

        query = "ffmpeg -i {} -map_metadata -1 -c:v copy -c:a copy {} -y".format(audio_filepath, audio_filepath)
        # print(query)
        # import sys
        # sys.exit()
        os.system(query)