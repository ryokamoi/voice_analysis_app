import os
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.externals import joblib
from glob import glob

from sptktools import w2r
from conv2vec import mcep2vec, pitch2vec
from extract import ext_mcep, ext_pitch

COMPONENTS = 10

def gmm_train(mfcc, save_name):
	gmm = GaussianMixture(n_components = COMPONENTS, covariance_type='full')
	gmm.fit(mfcc)
	
	path = os.path.splitext(save_name)[0]
	save_dir = '/'.join(path.split('/')[:-1])
	
	try:
		os.mkdir(save_dir)
	except FileExistsError:
		pass
	
	joblib.dump(gmm, save_name)

if __name__ == '__main__':
	filenames = glob('voicesample/*')
	pitchave = np.zeros(len(filenames))
	
	for i, filename in enumerate(filenames):
		print('file%s' % (i+1))
		
		path = os.path.splitext(filename)[0]
		name = path.split('/')[-1]
		
		try:
			os.mkdir('features/' + name)
		except FileExistsError:
			pass
		
		fpath = 'features/' + name + '/' + name
		w2r(filename, fpath + '.raw')
		ext_pitch(fpath + '.raw', fpath + '.pitch')
		ext_mcep(fpath + '.raw', fpath + '.mcep')
		pitch = pitch2vec(fpath + '.pitch')
		mfcc = mcep2vec(fpath + '.mcep')
		pitch = pitch[np.where(pitch>0)]
		mfcc = mfcc[np.where(pitch>0)]
		features = mfcc[:, [1, 5, 10, 15]]
		
		save_name = 'gmm/' + name + '/' + name + '.pkl'
		gmm_train(features, save_name)
