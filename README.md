# emotion.classification

Download the The Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS) from https://zenodo.org/record/1188976.
Make sure to only download the Audio-Speech zip file (Audio_Speech_Actors_01-24.zip)
Unpack the contents into a folder titled 'audio' in this root folder.
Verify that audio contains 24 folders, one for each actor, and that each actor's folder contains 60 files.


##### Experiments  

Evaluation of MFCC and Prosody features
1. On speech / song / combined domains
2. For each domain on -
    1. Effect of speaker normalization (z normalization)
    2. Significance of features for emotion / activation / valence recognition
    3. Classification confusion for emotion / activation / valence recognition
