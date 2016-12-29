#coding: utf-8

import argparse
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from PIL import Image

from sptktools import w2r
from conv2vec import mcep2vec, pitch2vec
from extract import ext_mcep, ext_pitch
from record import record

parser = argparse.ArgumentParser(description='Voice Analysis APP')
parser.add_argument('--filename', '-f', type=str,
                    help='file name to evaluate score')
parser.add_argument('--cheaptrick', '-c', action='store_true', default=False,
                    help='fix score')
args = parser.parse_args()

gmmnames = [] # filenames of gmm files (pkl)
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

def analysis(canvas=None, device=0):
    if not args.filename:
        filename = 'file.wav'
        record(filename, 5, device)
    else:
        filename = args.filename

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
        scores[i] = score
    if args.cheaptrick:
        scoreave = np.average(scores)
        scores = scores * sampave / scoreave
    for i, score in enumerate(scores):
        samples = np.sort(allsamples[:, i])
        dist = np.array([abs(sample-score) for sample in samples])
        scores[i] = np.where(dist==np.min(dist))[0][0] * 5/30

    fig = plt.figure(figsize=(6, 6))
    titles = ['CUTE', 'YOUNG', 'COOL', 'MASCULINE', 'BOYISH', 'DANDY']

    labels = [ [1, 2, 3, 4, 5, 6] ] + [[]] * 5

    radar = Radar(fig, titles, labels)
    radar.plot(np.ndarray.tolist(scores),  "-", lw=2, color="black", alpha=1)
    plt.savefig('result.png')
    img = Image.open('result.png')
    img.save('result.gif')

    if __name__ != '__main__':
        canvas.delete('all')
        canvas.create_text(310, 310, anchor='center', justify='center',
                                       text='結果を見る！', font=(None, 40))
        canvas.create_text(310, 30, anchor='n', justify='center',
                                       text='↑\n↑\n↑\n↑\n', font=(None, 40))

if __name__ == '__main__':
    analysis()
