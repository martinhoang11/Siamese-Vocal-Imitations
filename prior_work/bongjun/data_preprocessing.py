import numpy as np
import librosa
import os
import pickle
import pandas as pd

# There are 240 categories of vocal imitations in the current dataset
# The first half (1-120) for training and validation, the second half (120-240) for testing

# extract spectrograms of training imitations 
folders = os.listdir('./data/audio/1-120-imitation/train')

X_train = []
Y_train = []
for k in range(1, 121):
    if k%50==0:
        print k
    
    files_train = os.listdir('./data/audio/1-120-imitation/train/' + str("%03d" % (k,)) + '/')
    
    for f in files_train:
        y, sr = librosa.load('./data/audio/1-120-imitation/train/' + str("%03d" % (k,)) + '/' + f, sr=16000)
        
        # zero-padding 
        if y.shape[0] < 4*sr:
            pad = np.zeros((4*sr-y.shape[0]))
            y_fix = np.append(y, pad)
        else:
            y_fix = y[0:int(4*sr)]
        
        S = librosa.feature.melspectrogram(y=y_fix, sr=sr, n_fft=133, 
                                           hop_length=133, power=2, n_mels=39, 
                                           fmin=0.0, fmax=5000)
        S = S[:, :482]
        S_db = librosa.power_to_db(S, ref=np.max)
        
        X_train.append(S_db)
        Y_train.append(k-1) # label 0 to 120

X_train = np.array(X_train).astype('float32')
Y_train = np.array(Y_train).astype('uint8')

#save!
# np.save('./data/npy/TL/first_half_train_X.npy', X_train)
# np.save('./data/npy/TL/first_half_train_Y.npy', Y_train)




# extract spectrograms of validation imitations
folders = os.listdir('./data/audio/1-120-imitation/validation')
X_val = []
Y_val = []
for k in range(1, 121):
    if k%20==0:
        print k
    files_val = os.listdir('./data/audio/1-120-imitation/validation/' + str("%03d" % (k,)) + '/')
    
    for f in files_val:
        
        y, sr = librosa.load('./data/audio/1-120-imitation/validation/' + str("%03d" % (k,)) + '/' + f, sr=16000)
        
        # zero-padding 
        if y.shape[0] < 4*sr:
            pad = np.zeros((4*sr-y.shape[0]))
            y_fix = np.append(y, pad)
        else:
            y_fix = y[0:int(4*sr)]
        
        S = librosa.feature.melspectrogram(y=y_fix, sr=sr, n_fft=133, 
                                           hop_length=133, power=2, n_mels=39, 
                                           fmin=0.0, fmax=5000)
        S = S[:, :482]
        S_db = librosa.power_to_db(S, ref=np.max)
        #print f
        
        X_val.append(S_db)
        Y_val.append(k-1) # label 0 to 120

# np.save('./data/npy/TL/first_half_val_X.npy', X_val)
# np.save('./data/npy/TL/first_half_val_Y.npy', Y_val)




# extract spectrograms of testing imitations (each of 4 categories)
for categories in ['ai', 'cs', 'ed', 'ss']:
    folders = os.listdir('./data/audio/121-240-imitation/'+categories)
    if '.DS_Store' in folders:
    	folders.remove('.DS_Store')
    n_folders = len(folders)
    X_test = []
    Y_test = []
    for k in range(1, n_folders+1):
        if k%10==0:
            print k
        files_test = os.listdir('./data/audio/121-240-imitation/'+categories+'/' + str("%03d" % (k,)) + '/')

        for f in files_test:
            y, sr = librosa.load('./data/audio/121-240-imitation/'+categories +'/'+ str("%03d" % (k,)) + '/' + f, sr=16000)

            # zero-padding 
            if y.shape[0] < 4*sr:
                pad = np.zeros((4*sr-y.shape[0]))
                y_fix = np.append(y, pad)
            else:
                y_fix = y[0:int(4*sr)]

            S = librosa.feature.melspectrogram(y=y_fix, sr=sr, n_fft=133, 
                                               hop_length=133, power=2, n_mels=39, 
                                               fmin=0.0, fmax=5000)
            S = S[:, :482]
            S_db = librosa.power_to_db(S, ref=np.max)

            X_test.append(S_db)
            Y_test.append(k-1) # label 0 to 120

    X_test = np.array(X_test).astype('float32')
    Y_test = np.array(Y_test).astype('uint8')

    # np.save('./data/npy/TL/second_half_test_X_'+categories+'.npy', X_test)
    # np.save('./data/npy/TL/second_half_test_Y_'+categories+'.npy', Y_test)




# extract spectrograms of training reference recordings
files = os.listdir('./data/audio/1-120-recording/')
recording_label_info = {}
for k, file_name in enumerate(files):
    recording_label_info[file_name] = k

files = os.listdir('./data/audio/1-120-recording/')
X_ref = []
Y_ref = []
for f in files:
    y, sr = librosa.load('./data/audio/1-120-recording/'+f, sr=44100)
    
    # zero-padding 
    if y.shape[0] < 4*sr:
        pad = np.zeros((4*sr-y.shape[0]))
        y_fix = np.append(y, pad)
    else:
        y_fix = y[0:int(4*sr)]

    S = librosa.feature.melspectrogram(y=y_fix, sr=sr, n_fft=1024, hop_length=1024, power=2)
    S = librosa.power_to_db(S, ref=np.max)
    S_fix = S[:, 0:128]
    
    X_ref.append(S_fix)
    Y_ref.append(recording_label_info[f])
X_ref = np.array(X_ref).astype('float32')
Y_ref = np.array(Y_ref).astype('uint8')

# np.save('./data/npy/TL/first_half_ref_X.npy', X_ref)
# np.save('./data/npy/TL/first_half_ref_Y.npy', Y_ref)




# extract spectrograms of testing reference recordings
for category in ['ai', 'cs', 'ss', 'ed']:
    files = os.listdir('./data/audio/121-240-recording/'+category+'/')
    recording_label_info_second_half_ai = {}
    for k, file_name in enumerate(files):
        recording_label_info_second_half[file_name] = k

    files = os.listdir('./data/audio/121-240-recording/'+category+'/')
    X_ref = []
    Y_ref = []
    for f in files:
        y, sr = librosa.load('./data/audio/121-240-recording/'+category+'/'+f, sr=44100)

        # zero-padding 
        if y.shape[0] < 4*sr:
            pad = np.zeros((4*sr-y.shape[0]))
            y_fix = np.append(y, pad)
        else:
            y_fix = y[0:int(4*sr)]

        S = librosa.feature.melspectrogram(y=y_fix, sr=sr, n_fft=1024, hop_length=1024, power=2)
        S = librosa.power_to_db(S, ref=np.max)
        S_fix = S[:, 0:128]

        X_ref.append(S_fix)
        Y_ref.append(recording_label_info_second_half[f])
    X_ref = np.array(X_ref).astype('float32')
    #Y_ref = to_categorical(np.array(Y_ref), 120)
    Y_ref = np.array(Y_ref).astype('uint8')

    # np.save('./data/npy/second_half_ref_X_'+category+'.npy', X_ref)
    # np.save('./data/npy/second_half_ref_Y_'+category+'.npy', Y_ref)