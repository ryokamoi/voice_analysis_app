import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.externals import joblib
import matplotlib.pyplot as plt

from sptktools import w2r
from conv2vec import mcep2vec, pitch2vec
from extract import ext_mcep, ext_pitch
from record import record

gmmnames = ['gmm/sr_f10/sr_f10.pkl', 'gmm/sr_f13/sr_f13.pkl', 'gmm/sr_f06/sr_f06.pkl',
                        'gmm/sr_m12/sr_m12.pkl', 'gmm/sr_m16/sr_m16.pkl', 'gmm/sr_m05/sr_m05.pkl']
allsamples = np.load('scores.npy')
pitchave = np.load('pitch_average.npy')

class Radar(object):

    def __init__(self, fig, titles, labels, rect=None):
        if rect is None:
            rect = [0.1, 0.1, 0.8, 0.8]

        self.n = len(titles)
        self.angles =  [angle % 360 for angle in np.arange(90, 90+360, 360.0/self.n)]
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i) 
                         for i in range(self.n)]
        
        self.ax = self.axes[0]
        print(self.angles)
        self.ax.set_thetagrids(self.angles, labels=titles, fontsize=14)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, 6), angle=angle, labels=label)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(0, 5)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)

if __name__ == '__main__':
    
    filename = 'file.wav'
    record(filename, 5)
    w2r(filename, 'file.raw')
    ext_pitch('file.raw', 'file.pitch')
    ext_mcep('file.raw', 'file.mcep')
    
    mfcc = mcep2vec('file.mcep')
    pitch = pitch2vec('file.pitch')
    mfcc = mfcc[np.where(pitch>0)]
    pitch = pitch[np.where(pitch>0)]
    features = mfcc[:, [1, 5, 10, 15]]
    
    scores = np.zeros(6)
    sampave = np.average(allsamples)
    for i, gmmname in enumerate(gmmnames):
        gmm = joblib.load(gmmname)
        score = np.exp(gmm.score(features))
        print(score)
        scores[i] = score
    scoreave = np.average(scores)
    scores = scores * sampave / scoreave
    for i, score in enumerate(scores):
        samples = np.sort(allsamples[:, i])
        dist = np.array([abs(sample-score) for sample in samples])
        scores[i] = np.where(dist==np.min(dist))[0][0] * 5/33
    # print(scores)
    
    fig = plt.figure(figsize=(10, 10))
    titles = ['cute', 'young', 'cool', 'masculine', 'boyish', 'dandy']
    
    labels = [ [1, 2, 3, 4, 5, 6] ] + [[]] * 5
    
    radar = Radar(fig, titles, labels)
    radar.plot(np.ndarray.tolist(scores),  "-", lw=2, color="b", alpha=0.4)
    plt.show()
