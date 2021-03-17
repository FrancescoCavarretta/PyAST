import numpy as np

def spikebits(spiketimes, dt):
  #print (spiketimes)
  #print ("dt", dt)
  spiketimes = np.int64(np.round(spiketimes/dt))
  spikebits = np.zeros( np.max(spiketimes) + 1 )
  spikebits[spiketimes] = 1.0
  #print (spikebits)
  return spikebits
