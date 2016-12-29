import struct
import sys
import numpy as np

from sptktools import execute

def mcep2vec(filename):
    mceplist = []
    f = open(filename, "rb")
    while True:
        b = f.read(4)
        if b == b'':
            break
        m = struct.unpack("f", b)[0]
        mceplist.append(m)
    f.close()
    return np.reshape(np.array(mceplist), (-1, 26))

def pitch2vec(filename):
    pitchlist = []
    f = open(filename, "rb")
    while True:
        b = f.read(4)
        if b == b'':
            break
        p = struct.unpack("f", b)[0]
        pitchlist.append(p)
    f.close()
    return np.array(pitchlist)
