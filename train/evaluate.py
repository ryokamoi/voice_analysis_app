import os
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.externals import joblib
from glob import glob

from sptktools import w2r
from conv2vec import mcep2vec, pitch2vec
from extract import ext_mcep, ext_pitch

gmmnames = ['gmm/sr_f10/sr_f10.pkl', 'gmm/sr_f13/sr_f13.pkl', 'gmm/sr_f06/sr_f06.pkl',
                        'gmm/sr_m12/sr_m12.pkl', 'gmm/sr_m16/sr_m16.pkl', 'gmm/sr_m05/sr_m05.pkl']

mcepnames = glob('mcepsample/*')
pitchnames = glob('pitchsample/*')

if __name__ == '__main__':
    scores = np.zeros(6)
    gmms = [None] * 6
    for i, gmmname in enumerate(gmmnames):
        gmms[i] = joblib.load(gmmname)
    pitchave = np.zeros(len(mcepnames))
    
    for i in range(len(mcepnames)):
        score = np.zeros(6)
        mfcc = mcep2vec(mcepnames[i])
        pitch = pitch2vec(pitchnames[i])
        mfcc = mfcc[np.where(pitch>0)]
        pitch = pitch[np.where(pitch>0)]
        features = mfcc[:, [1, 5, 10 , 15]]
        
        for j, gmm in enumerate(gmms):
            score[j] = np.exp(gmm.score(features))
        scores = np.vstack((scores, score))
        pitchave[i] = np.average(pitch[np.where(pitch>0)])
    
    scores = scores[1:]
    np.save('scores.npy', scores)
    np.save('pitch_average.npy', pitchave)
