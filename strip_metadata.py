#!/usr/bin/env python3


####
## NOTE: This code is not necessary to use, since file in audio folder have already been stripped of metadata.
####

import os
## Strips metadata from all audio files in top 2 levels of AUDIO_FOLDER folder
## This is an optional step. Some wav files have metadata that causes the DisVoice feature extraction step to fail
## NOTE: Requires FFMPEG
AUDIO_FOLDER = 'audio'
SONG_FOLDER = 'song'


# # Iterate through all actor folders and then audio files
# for actor_folder in os.listdir(AUDIO_FOLDER):
#     actor_folderpath = os.path.join(os.getcwd(), AUDIO_FOLDER, actor_folder)
#     for audio_filename in os.listdir(actor_folderpath):
#         audio_filepath = os.path.join(actor_folderpath, audio_filename)

#         # Wipe metadata with ffmpeg
#         query = "ffmpeg -i {} -map_metadata -1 -c:v copy -c:a copy {} -y".format(audio_filepath, audio_filepath)
#         os.system(query)


# Song files
# Iterate through all actor folders and then audio files !! for song !!
for actor_folder in os.listdir(SONG_FOLDER):
    actor_folderpath = os.path.join(os.getcwd(), SONG_FOLDER, actor_folder)
    for audio_filename in os.listdir(actor_folderpath):
        audio_filepath = os.path.join(actor_folderpath, audio_filename)

        # Wipe metadata with ffmpeg
        query = "ffmpeg -i {} -map_metadata -1 -c:v copy -c:a copy {} -y".format(audio_filepath, audio_filepath)
        os.system(query)

