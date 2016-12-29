from sptktools import execute

def ext_mcep(rawfile, mcepfile):
	mcepcmd = 'x2x +sf < %s | frame -l 400 -p 80 | window -l 400 -L 512 | mcep -l 512 -m 25 -a 0.54 -e 0.00001 > %s' % (rawfile, mcepfile)
	
	execute(mcepcmd)

def ext_pitch(rawfile, pitchfile):
	f0cmd = 'x2x +sf %s | pitch -a 1 -p 80 -s 44.1 -L 10 -H 500 > %s' \
	                                       % (rawfile, pitchfile)
	execute(f0cmd)
