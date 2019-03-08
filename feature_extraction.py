#!/usr/bin/env python3

####
## NOTE: This code is not necessary to use, since feature extraction results have already been stored in the audio folder.
####

import os



## Runs feature extraction using DisVoice
AUDIO_FOLDER = 'audio'
SONG_FOLDER = 'song'
DISVOICE_FOLDER = 'disvoice'

to_delete = []

articulation_info = []
phonation_info = []

cwd = os.getcwd()

# Iterate through all actor folders and then audio files
# for actor_folder in os.listdir(AUDIO_FOLDER):
#     actor_folderpath = os.path.join(os.getcwd(), AUDIO_FOLDER, actor_folder)
#     for audio_filename in os.listdir(actor_folderpath):
#         audio_filepath = os.path.join(actor_folderpath, audio_filename)

#         # Get raw filename and extension of file
#         filename, extension = os.path.splitext(audio_filepath)
#         if extension != ".wav":
#             continue

#         # Set up filename for feature extraction file
#         feature_filename = filename + '.txt'
#         feature_filepath= os.path.join(actor_folderpath, feature_filename)

#         # Set up filename for articulation
#         articulation_filename = filename+'.articulation.txt'
#         articulation_filepath = os.path.join(actor_folderpath, articulation_filename)
#         articulation_info.append((audio_filepath, articulation_filepath))

#         # Set up file info for phonation
#         phonation_filename = filename+'.phonation.txt'
#         phonation_filepath = os.path.join(actor_folderpath, phonation_filename)
#         phonation_info.append((audio_filepath, phonation_filepath))

        # # Run feature extraction on this file
        # print("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        # res = os.system("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        # if int(res) != 0:
        #     to_delete.append(audio_filepath)

# Change working directory to DisVoice articulation folder
# articulation_folder = os.path.join(os.getcwd(), DISVOICE_FOLDER, "articulation")
# print(articulation_folder)
# os.chdir(articulation_folder)

# for audio_filepath, articulation_filepath in articulation_info:
#     # # Run feature extraction on this file
#     print("python3 articulation.py {} {}".format(audio_filepath, articulation_filepath))
#     res = os.system("python3 articulation.py {} {}".format(audio_filepath, articulation_filepath))
#     if int(res) != 0:
#         to_delete.append(audio_filepath)
#     # print(articulation_filepath)



song_articulation_info = []

# Song data
os.chdir(cwd)
# Iterate through all actor folders and then audio files
for actor_folder in os.listdir(SONG_FOLDER):
    actor_folderpath = os.path.join(os.getcwd(), SONG_FOLDER, actor_folder)
    for audio_filename in os.listdir(actor_folderpath):
        audio_filepath = os.path.join(actor_folderpath, audio_filename)

        # Get raw filename and extension of file
        filename, extension = os.path.splitext(audio_filepath)
        if extension != ".wav":
            continue

        # Set up filename for feature extraction file
        feature_filename = filename + '.txt'
        feature_filepath= os.path.join(actor_folderpath, feature_filename)

        # Set up filename for articulation
        articulation_filename = filename+'.articulation.txt'
        articulation_filepath = os.path.join(actor_folderpath, articulation_filename)
        song_articulation_info.append((audio_filepath, articulation_filepath))

        # # Run feature extraction on this file
        # print("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        # res = os.system("python3 ./" + DISVOICE_FOLDER + "/prosody/prosody.py {} {}".format(audio_filepath, feature_filepath))
        # if int(res) != 0:
        #     to_delete.append(audio_filepath)

# Change working directory to DisVoice articulation folder
articulation_folder = os.path.join(cwd, DISVOICE_FOLDER, "articulation")
# print(articulation_folder)
os.chdir(articulation_folder)
for audio_filepath, articulation_filepath in song_articulation_info:
    # Run feature extraction on this file
    print("python3 articulation.py {} {}".format(audio_filepath, articulation_filepath))
    res = os.system("python3 articulation.py {} {}".format(audio_filepath, articulation_filepath))
    if int(res) != 0:
        to_delete.append(audio_filepath)
    # print(articulation_filepath)



print("The following files caused an issue in disvoice")
for err in to_delete:
    print(err)