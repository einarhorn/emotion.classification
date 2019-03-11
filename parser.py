#!/usr/bin/env python3

import os
from enum import Enum

# Base folder of audio files
AUDIO_FOLDER = "audio"
SONG_FOLDER = "song"

# Set up this param and DisVoice such that:
# ./ + DISVOICE_FOLDER + /prosody/prosody.py
# is a valid path
DISVOICE_FOLDER = "disvoice"
RUN_FEATURE_EXTRACTION = True
DATA_FILE = "data.prosody.csv"
ARTICULATION_DATA_FILE = "data.articulation.csv"
COMBINED_DATA_FILE = "data.combined.csv"
MFCC_DATA_FILE = "data.mfcc.csv"
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
        self.folder_path = os.path.dirname(self.path)

        # Split full filename into file name and file extension
        self.filename, self.extension = os.path.splitext(self.full_filename)

        ## Extract audio metadata from filename
        # Filenames look like: 03-01-03-02-02-01-12.wav
        split_filename = self.filename.split('-')

        # We are not interested in modality or vocal channel for this task
        # self.modality = split_filename[0]
        self.vocal_channel = int(split_filename[1])

        # The emotion annotation
        self.emotion_int = int(split_filename[2]) - 1
        # self.emotion = Emotion(self.emotion_int)

        # Whether this emotion was done "strong" or "normal"
        self.emotion_intensity_int = int(split_filename[3])
        self.emotion_intensity = EmotionIntensity(self.emotion_intensity_int)

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
        self.gender_int = self.actor_id % 2
        self.gender = Gender(self.gender_int)

        # Read DisVoice results for this file
        # Metadata is an array of 38 features from DisVoice
        self.features = []
        metadata_filename = self.filename + '.' + "txt"
        metadata_path = os.path.join(self.folder_path, metadata_filename)
        if os.path.isfile(metadata_path):
            # Read metadata file
            with open(metadata_path, 'r') as infile:
                # Should only be one line
                for line in infile:
                    line = line.rstrip()
                    self.features = line.split()
        else:
            print("Could not find {}".format(metadata_path))

        # Read DisVoice articulation results for this file
        # articulation_metadata is an array of 488 features from DisVoice
        self.articulation_features = []
        articulation_metadata_filename = self.filename + '.articulation.' + "txt"
        articulation_metadata_path = os.path.join(self.folder_path, articulation_metadata_filename)
        if os.path.isfile(articulation_metadata_path):
            # Read metadata file
            with open(articulation_metadata_path, 'r') as infile:
                # Should only be one line
                for line in infile:
                    line = line.rstrip()
                    self.articulation_features = line.split()
        else:
            print("Could not find {}".format(articulation_metadata_path))
        
        self.mfcc_features = []
        mfcc_metadata_filename = self.filename + '.librosa_mfcc.' + "txt"
        mfcc_metadata_path = os.path.join(self.folder_path, mfcc_metadata_filename)
        if os.path.isfile(mfcc_metadata_path):
            # Read metadata file
            with open(mfcc_metadata_path, 'r') as infile:
                # Should only be one line
                for line in infile:
                    line = line.rstrip()
                    self.mfcc_features = line.split()
        else:
            print("Could not find {}".format(articulation_metadata_path))
    
    def to_csv_line(self):
        line_arr = [self.filename, self.emotion_int, self.vocal_channel, self.emotion_intensity_int, self.statement, self.repetition, self.actor_id, self.gender_int]
        line_arr += self.features
        line_arr = [str(item) for item in line_arr]
        return ",".join(line_arr)
    
    def to_csv_articulation_line(self):
        line_arr = [self.filename, self.emotion_int, self.vocal_channel, self.emotion_intensity_int, self.statement, self.repetition, self.actor_id, self.gender_int]
        line_arr += self.articulation_features
        line_arr = [str(item) for item in line_arr]
        return ",".join(line_arr)

    def to_csv_combined_line(self):
        line_arr = [self.filename, self.emotion_int, self.vocal_channel, self.emotion_intensity_int, self.statement, self.repetition, self.actor_id, self.gender_int]
        line_arr += self.features
        line_arr += self.mfcc_features
        # print(len(line_arr))
        line_arr = [str(item) for item in line_arr]
        return ",".join(line_arr)
    
    def to_csv_mfcc_line(self):
        line_arr = [self.filename, self.emotion_int, self.vocal_channel, self.emotion_intensity_int, self.statement, self.repetition, self.actor_id, self.gender_int]
        # all_feats = []
        # all_feats += self.articulation_features[22:58]
        # all_feats += self.articulation_features[80:116]
        # all_feats += self.articulation_features[22+122*1:58+122*1]
        # all_feats += self.articulation_features[80+122*1:116+122*1]
        # all_feats += self.articulation_features[22+122*2:58+122*2]
        # all_feats += self.articulation_features[80+122*2:116+122*2]
        # all_feats += self.articulation_features[22+122*3:58+122*3]
        # all_feats += self.articulation_features[80+122*3:116+122*3]
        line_arr += self.mfcc_features
        line_arr = [str(item) for item in line_arr]
        # print(len(line_arr))
        return ",".join(line_arr)


# Holds all of our audio files
class AudioParser():
    def __init__(self):
        # Our full list of audio files
        self.audio_files = []
        self.song_files = []

        # Iterate through each actor's folder
        for actor_folder in os.listdir(AUDIO_FOLDER):
            # Get path of this actor folder
            actor_folderpath = os.path.join(os.getcwd(), AUDIO_FOLDER, actor_folder)

            # Iterate through each of the actor's sound files
            for audio_filename in os.listdir(actor_folderpath):
                # Check this is .wav file
                _, extension = os.path.splitext(audio_filename)

                # Ignore non-wav files
                if extension != ".wav":
                    continue

                # Get relative path of this sound file
                audio_filepath = os.path.join(actor_folderpath, audio_filename)

                # Create audio instance and store in our list
                audio_file = AudioFile(audio_filepath, audio_filename)
                self.audio_files.append(audio_file)
        
        # PARSE SONGS
         # Iterate through each actor's folder
        for actor_folder in os.listdir(SONG_FOLDER):
            # Get path of this actor folder
            actor_folderpath = os.path.join(os.getcwd(), SONG_FOLDER, actor_folder)

            # Iterate through each of the actor's sound files
            for audio_filename in os.listdir(actor_folderpath):
                # Check this is .wav file
                _, extension = os.path.splitext(audio_filename)

                # Ignore non-wav files
                if extension != ".wav":
                    continue

                # Get relative path of this sound file
                audio_filepath = os.path.join(actor_folderpath, audio_filename)

                # Create audio instance and store in our list
                audio_file = AudioFile(audio_filepath, audio_filename)
                self.song_files.append(audio_file)
            
        self.prosody_features = [
            "Average fundamental frequency in voiced segments",
            "Standard deviation of fundamental frequency in Hz",
            "Variablity of fundamental frequency in semitones",
            "Maximum of the fundamental frequency in Hz",
            "Average energy in dB",
            "Standard deviation of energy in dB",
            "Maximum energy",
            "Voiced rate (number of voiced segments per second)",
            "Average duration of voiced segments",
            "Standard deviation of duration of voiced segments",
            "Pause rate (number of pauses per second)",
            "Average duration of pauses",
            "Standard deviation of duration of pauses ",
            "Average tilt of fundamental frequency",
            "Tilt regularity of fundamental frequency",
            "Mean square error of the reconstructed F0 with a 1-degree polynomial",
            "(Silence duration)/(Voiced+Unvoiced durations)",
            "(Voiced duration)/(Unvoiced durations)",
            "(Unvoiced duration)/(Voiced+Unvoiced durations)",
            "(Voiced duration)/(Voiced+Unvoiced durations)",
            "(Voiced duration)/(Silence durations)",
            "(Unvoiced duration)/(Silence durations)",
            "Unvoiced duration Regularity",
            "Unvoiced energy Regularity",
            "Voiced duration Regularity",
            "Voiced energy Regularity",
            "Pause duration Regularity",
            "Maximum duration of voiced segments",
            "Maximum duration of unvoiced segments",
            "Minimum duration of voiced segments",
            "Minimum duration of unvoiced segments",
            "rate (# of voiced segments) / (# of unvoiced segments)",
            "Average tilt of energy contour",
            "Regression coefficient between the energy contour and a linear regression",
            "Mean square error of the reconstructed energy contour with a 1-degree polynomial",
            "Regression coefficient between the F0 contour and a linear regression",
            "Average Delta energy within consecutive voiced segments",
            "Standard deviation of Delta energy within consecutive voiced segments",
        ]

        self.articulation_features = [
            'Bark band energies in onset transitions (22 BBE) [0] [mean]',
            'Bark band energies in onset transitions (22 BBE) [1] [mean]',
            'Bark band energies in onset transitions (22 BBE) [2] [mean]',
            'Bark band energies in onset transitions (22 BBE) [3] [mean]',
            'Bark band energies in onset transitions (22 BBE) [4] [mean]',
            'Bark band energies in onset transitions (22 BBE) [5] [mean]',
            'Bark band energies in onset transitions (22 BBE) [6] [mean]',
            'Bark band energies in onset transitions (22 BBE) [7] [mean]',
            'Bark band energies in onset transitions (22 BBE) [8] [mean]',
            'Bark band energies in onset transitions (22 BBE) [9] [mean]',
            'Bark band energies in onset transitions (22 BBE) [10] [mean]',
            'Bark band energies in onset transitions (22 BBE) [11] [mean]',
            'Bark band energies in onset transitions (22 BBE) [12] [mean]',
            'Bark band energies in onset transitions (22 BBE) [13] [mean]',
            'Bark band energies in onset transitions (22 BBE) [14] [mean]',
            'Bark band energies in onset transitions (22 BBE) [15] [mean]',
            'Bark band energies in onset transitions (22 BBE) [16] [mean]',
            'Bark band energies in onset transitions (22 BBE) [17] [mean]',
            'Bark band energies in onset transitions (22 BBE) [18] [mean]',
            'Bark band energies in onset transitions (22 BBE) [19] [mean]',
            'Bark band energies in onset transitions (22 BBE) [20] [mean]',
            'Bark band energies in onset transitions (22 BBE) [21] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [mean]',
            'Bark band energies in offset transitions (22 BBE) [0] [mean]',
            'Bark band energies in offset transitions (22 BBE) [1] [mean]',
            'Bark band energies in offset transitions (22 BBE) [2] [mean]',
            'Bark band energies in offset transitions (22 BBE) [3] [mean]',
            'Bark band energies in offset transitions (22 BBE) [4] [mean]',
            'Bark band energies in offset transitions (22 BBE) [5] [mean]',
            'Bark band energies in offset transitions (22 BBE) [6] [mean]',
            'Bark band energies in offset transitions (22 BBE) [7] [mean]',
            'Bark band energies in offset transitions (22 BBE) [8] [mean]',
            'Bark band energies in offset transitions (22 BBE) [9] [mean]',
            'Bark band energies in offset transitions (22 BBE) [10] [mean]',
            'Bark band energies in offset transitions (22 BBE) [11] [mean]',
            'Bark band energies in offset transitions (22 BBE) [12] [mean]',
            'Bark band energies in offset transitions (22 BBE) [13] [mean]',
            'Bark band energies in offset transitions (22 BBE) [14] [mean]',
            'Bark band energies in offset transitions (22 BBE) [15] [mean]',
            'Bark band energies in offset transitions (22 BBE) [16] [mean]',
            'Bark band energies in offset transitions (22 BBE) [17] [mean]',
            'Bark band energies in offset transitions (22 BBE) [18] [mean]',
            'Bark band energies in offset transitions (22 BBE) [19] [mean]',
            'Bark band energies in offset transitions (22 BBE) [20] [mean]',
            'Bark band energies in offset transitions (22 BBE) [21] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [mean]',
            'First formant Frequency [mean]',
            'First Derivative of the first formant frequency [mean]',
            'Second Derivative of the first formant frequency [mean]',
            'Second formant Frequency [mean]',
            'First derivative of the Second formant Frequency [mean]',
            'Second derivative of the Second formant Frequency [mean]',
            'Bark band energies in onset transitions (22 BBE) [0] [std]',
            'Bark band energies in onset transitions (22 BBE) [1] [std]',
            'Bark band energies in onset transitions (22 BBE) [2] [std]',
            'Bark band energies in onset transitions (22 BBE) [3] [std]',
            'Bark band energies in onset transitions (22 BBE) [4] [std]',
            'Bark band energies in onset transitions (22 BBE) [5] [std]',
            'Bark band energies in onset transitions (22 BBE) [6] [std]',
            'Bark band energies in onset transitions (22 BBE) [7] [std]',
            'Bark band energies in onset transitions (22 BBE) [8] [std]',
            'Bark band energies in onset transitions (22 BBE) [9] [std]',
            'Bark band energies in onset transitions (22 BBE) [10] [std]',
            'Bark band energies in onset transitions (22 BBE) [11] [std]',
            'Bark band energies in onset transitions (22 BBE) [12] [std]',
            'Bark band energies in onset transitions (22 BBE) [13] [std]',
            'Bark band energies in onset transitions (22 BBE) [14] [std]',
            'Bark band energies in onset transitions (22 BBE) [15] [std]',
            'Bark band energies in onset transitions (22 BBE) [16] [std]',
            'Bark band energies in onset transitions (22 BBE) [17] [std]',
            'Bark band energies in onset transitions (22 BBE) [18] [std]',
            'Bark band energies in onset transitions (22 BBE) [19] [std]',
            'Bark band energies in onset transitions (22 BBE) [20] [std]',
            'Bark band energies in onset transitions (22 BBE) [21] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [std]',
            'Bark band energies in offset transitions (22 BBE) [0] [std]',
            'Bark band energies in offset transitions (22 BBE) [1] [std]',
            'Bark band energies in offset transitions (22 BBE) [2] [std]',
            'Bark band energies in offset transitions (22 BBE) [3] [std]',
            'Bark band energies in offset transitions (22 BBE) [4] [std]',
            'Bark band energies in offset transitions (22 BBE) [5] [std]',
            'Bark band energies in offset transitions (22 BBE) [6] [std]',
            'Bark band energies in offset transitions (22 BBE) [7] [std]',
            'Bark band energies in offset transitions (22 BBE) [8] [std]',
            'Bark band energies in offset transitions (22 BBE) [9] [std]',
            'Bark band energies in offset transitions (22 BBE) [10] [std]',
            'Bark band energies in offset transitions (22 BBE) [11] [std]',
            'Bark band energies in offset transitions (22 BBE) [12] [std]',
            'Bark band energies in offset transitions (22 BBE) [13] [std]',
            'Bark band energies in offset transitions (22 BBE) [14] [std]',
            'Bark band energies in offset transitions (22 BBE) [15] [std]',
            'Bark band energies in offset transitions (22 BBE) [16] [std]',
            'Bark band energies in offset transitions (22 BBE) [17] [std]',
            'Bark band energies in offset transitions (22 BBE) [18] [std]',
            'Bark band energies in offset transitions (22 BBE) [19] [std]',
            'Bark band energies in offset transitions (22 BBE) [20] [std]',
            'Bark band energies in offset transitions (22 BBE) [21] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [std]',
            'First formant Frequency [std]',
            'First Derivative of the first formant frequency [std]',
            'Second Derivative of the first formant frequency [std]',
            'Second formant Frequency [std]',
            'First derivative of the Second formant Frequency [std]',
            'Second derivative of the Second formant Frequency [std]',
            'Bark band energies in onset transitions (22 BBE) [0] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [1] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [2] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [3] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [4] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [5] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [6] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [7] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [8] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [9] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [10] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [11] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [12] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [13] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [14] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [15] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [16] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [17] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [18] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [19] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [20] [skewness]',
            'Bark band energies in onset transitions (22 BBE) [21] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [0] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [1] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [2] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [3] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [4] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [5] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [6] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [7] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [8] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [9] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [10] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [11] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [12] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [13] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [14] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [15] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [16] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [17] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [18] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [19] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [20] [skewness]',
            'Bark band energies in offset transitions (22 BBE) [21] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [skewness]',
            'First formant Frequency [skewness]',
            'First Derivative of the first formant frequency [skewness]',
            'Second Derivative of the first formant frequency [skewness]',
            'Second formant Frequency [skewness]',
            'First derivative of the Second formant Frequency [skewness]',
            'Second derivative of the Second formant Frequency [skewness]',
            'Bark band energies in onset transitions (22 BBE) [0] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [1] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [2] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [3] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [4] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [5] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [6] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [7] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [8] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [9] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [10] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [11] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [12] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [13] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [14] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [15] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [16] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [17] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [18] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [19] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [20] [kurtosis]',
            'Bark band energies in onset transitions (22 BBE) [21] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [0] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [1] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [2] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [3] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [4] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [5] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [6] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [7] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [8] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [9] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [10] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [11] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [12] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [13] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [14] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [15] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [16] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [17] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [18] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [19] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [20] [kurtosis]',
            'Bark band energies in offset transitions (22 BBE) [21] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [kurtosis]',
            'First formant Frequency [kurtosis]',
            'First Derivative of the first formant frequency [kurtosis]',
            'Second Derivative of the first formant frequency [kurtosis]',
            'Second formant Frequency [kurtosis]',
            'First derivative of the Second formant Frequency [kurtosis]',
            'Second derivative of the Second formant Frequency [kurtosis]'
        ]

        self.mfcc_feature_headers = [
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [mean]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [mean]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [mean]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [mean]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [mean]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [mean]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [std]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [std]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [std]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [std]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [std]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [std]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [skewness]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [skewness]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [skewness]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [skewness]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [skewness]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [skewness]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [0] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [1] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [2] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [3] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [4] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [5] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [6] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [7] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [8] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [9] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [10] [kurtosis]',
            'Mel frequency cepstral coefficients in onset transitions (12 MFCC onset) [11] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [0] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [1] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [2] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [3] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [4] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [5] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [6] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [7] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [8] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [9] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [10] [kurtosis]',
            'First derivative of the MFCCs in onset transitions (12 DMFCC onset) [11] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [0] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [1] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [2] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [3] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [4] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [5] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [6] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [7] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [8] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [9] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [10] [kurtosis]',
            'Second derivative of the MFCCs in onset transitions (12 DDMFCC onset) [11] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [0] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [1] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [2] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [3] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [4] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [5] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [6] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [7] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [8] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [9] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [10] [kurtosis]',
            'MFCCC in offset transitions (12 MFCC offset) [11] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [kurtosis]',
            'First derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [0] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [1] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [2] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [3] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [4] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [5] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [6] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [7] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [8] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [9] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [10] [kurtosis]',
            'Second derivative of the MFCCs in offset transitions (12 DMFCC offset) [11] [kurtosis]',
        ]
    
        self.librosa_mfcc_headers = [
            'MFCC[1]',
            'MFCC[2]',
            'MFCC[3]',
            'MFCC[4]',
            'MFCC[5]',
            'MFCC[6]',
            'MFCC[7]',
            'MFCC[8]',
            'MFCC[9]',
            'MFCC[10]',
            'MFCC[11]',
            'MFCC[12]',
            'MFCC[13]',
            'MFCC[14]',
            'MFCC[15]',
            'MFCC[16]',
            'MFCC[17]',
            'MFCC[18]',
            'MFCC[19]',
            'MFCC[20]',
            'MFCC[21]',
            'MFCC[22]',
            'MFCC[23]',
            'MFCC[24]',
            'MFCC[25]',
            'MFCC[26]',
            'MFCC[27]',
            'MFCC[28]',
            'MFCC[29]',
            'MFCC[30]',
            'MFCC[31]',
            'MFCC[32]',
            'MFCC[33]',
            'MFCC[34]',
            'MFCC[35]',
            'MFCC[36]',
            'MFCC[37]',
            'MFCC[38]',
            'MFCC[39]',
            'MFCC[40]',
        ]

    def header_csv(self):
        header = ["filename", "emotion", "vocal channel (speech/song)", "emotion_intensity", "statement", "repretition", "actor_id", "gender_int"]
        line = header + self.prosody_features
        return ",".join(line)
    
    def header_articulation_csv(self):
        header = ["filename", "emotion", "vocal channel (speech/song)", "emotion_intensity", "statement", "repretition", "actor_id", "gender_int"]
        line = header + self.articulation_features
        return ",".join(line)
    
    def header_combined_csv(self):
        header = ["filename", "emotion", "vocal channel (speech/song)", "emotion_intensity", "statement", "repretition", "actor_id", "gender_int"]
        line = header + self.prosody_features + self.librosa_mfcc_headers
        # print(len(line))
        return ",".join(line)
    
    def header_mfcc_only(self):
        header = ["filename", "emotion", "vocal channel (speech/song)", "emotion_intensity", "statement", "repretition", "actor_id", "gender_int"]
        line = header + self.librosa_mfcc_headers
        # print(len(line))
        return ",".join(line)
    




def create_dataset():
    a = AudioParser()
    # print(a.audio_files[0].features)

    # Accoustic features
    with open(DATA_FILE, 'w') as outfile:
        outfile.write("{}\n".format(a.header_csv()))
        for audio_item in a.audio_files:
            outfile.write("{}\n".format(audio_item.to_csv_line()))
        
        for audio_item in a.song_files:
            outfile.write("{}\n".format(audio_item.to_csv_line()))
    
    # Articulation
    with open(ARTICULATION_DATA_FILE, 'w') as outfile:
        outfile.write("{}\n".format(a.header_articulation_csv()))
        for audio_item in a.audio_files:
            outfile.write("{}\n".format(audio_item.to_csv_articulation_line()))
        
        for audio_item in a.song_files:
            outfile.write("{}\n".format(audio_item.to_csv_articulation_line()))
    
    # Combined
    with open(COMBINED_DATA_FILE, 'w') as outfile:
        outfile.write("{}\n".format(a.header_combined_csv()))
        for audio_item in a.audio_files:
            outfile.write("{}\n".format(audio_item.to_csv_combined_line()))
        for audio_item in a.song_files:
            outfile.write("{}\n".format(audio_item.to_csv_combined_line()))

    # MFCC
    with open(MFCC_DATA_FILE, 'w') as outfile:
        outfile.write("{}\n".format(a.header_mfcc_only()))
        for audio_item in a.audio_files:
            outfile.write("{}\n".format(audio_item.to_csv_mfcc_line()))
        for audio_item in a.song_files:
            outfile.write("{}\n".format(audio_item.to_csv_mfcc_line()))


if __name__ == "__main__":
    create_dataset()
