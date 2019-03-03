#!/usr/bin/env python3

import os
from enum import Enum

# Base folder of audio files
AUDIO_FOLDER = "audio"

## Relevant Enum classes
# Gender of the speaker
class Gender(Enum):
    FEMALE = 0
    MALE = 1

# Emotion of sound file
# Note that there is no strong intensity for a neutral emotion
class Emotion(Enum):
    Neutral = 1
    Calm = 2
    Happy = 3
    Sad = 4
    Angry = 5
    Fearful = 6
    Disgust = 7
    Surprised = 8

# Intensity of emotion
# Note that there is no strong intensity for a neutral emotion
class EmotionIntensity(Enum):
    Normal = 1
    Strong = 2


# Holds metadata for a single audio file
class AudioFile():
    def __init__(self, path, filename):
        # Store params
        self.path = path
        self.full_filename = filename

        # Split full filename into file name and file extension
        self.filename, self.extension = os.path.splitext(self.full_filename)

        ## Extract audio metadata from filename
        # Filenames look like: 03-01-03-02-02-01-12.wav
        split_filename = self.filename.split('-')

        # We are not interested in modality or vocal channel for this task
        # self.modality = split_filename[0]
        # self.vocal_channel = split_filename[1]

        # The emotion annotation
        emotion_int = int(split_filename[2])
        self.emotion = Emotion(emotion_int)

        # Whether this emotion was done "strong" or "normal"
        emotion_intensity_int = int(split_filename[3])
        self.emotion_intensity = EmotionIntensity(emotion_intensity_int)

        # The id of the text of the utterance (1 or 2)
        self.statement = int(split_filename[4])

        # The actual statement spoken by the speaker
        if self.statement == 1:
            self.statement_text = "Kids are talking by the door"
        else:
            self.statement_text = "Dogs are sitting by the door"

        # How many times this exact utterance has been given by this speaker (1st or 2nd time)
        self.repetition = int(split_filename[5])

        # Id of the actor (1-24)
        self.actor_id = int(split_filename[6])

        # The gender of the actor
        gender_int = self.actor_id % 2
        self.gender = Gender(gender_int)
    


# Holds all of our audio files
class AudioParser():
    def __init__(self):
        # Our full list of audio files
        self.audio_files = []

        # Iterate through each actor's folder
        for actor_folder in os.listdir(AUDIO_FOLDER):
            # Get path of this actor folder
            actor_folderpath = os.path.join(AUDIO_FOLDER, actor_folder)

            # Iterate through each of the actor's sound files
            for audio_filename in os.listdir(actor_folderpath):
                # Get relative path of this sound file
                audio_filepath = os.path.join(actor_folderpath, audio_filename)

                # Create audio instance and store in our list
                audio_file = AudioFile(audio_filepath, audio_filename)
                self.audio_files.append(audio_file)




a = AudioParser()
print(a.audio_files[1].gender)