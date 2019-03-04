#!/usr/bin/env python3

import os
## Runs feature extraction using DisVoice
AUDIO_FOLDER = 'audio'
DISVOICE_FOLDER = 'disvoice'

to_delete = []
# Iterate through all actor folders and then audio files
for actor_folder in os.listdir(AUDIO_FOLDER):
    actor_folderpath = os.path.join(os.getcwd(), AUDIO_FOLDER, actor_folder)
    for audio_filename in os.listdir(actor_folderpath):
        audio_filepath = os.path.join(actor_folderpath, audio_filename)

        # Get raw filename and extension of file
        filename, extension = os.path.splitext(audio_filepath)
        if extension != ".wav":
            continue

        # Set up filename for feature extraction file
        feature_filename = filename + '.txt'
        feature_filepath= os.path.join(actor_folderpath, feature_filename)

        # Run feature extraction on this file
        # print(audio_filepath)
        # print(feature_filepath)
        print("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        res = os.system("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        if int(res) != 0:
            to_delete.append(audio_filepath)
        # import sys
        # sys.exit()
print("The following files caused an issue in disvoice")
for err in to_delete:
    print(err)