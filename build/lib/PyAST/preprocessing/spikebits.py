import numpy as np

def spikebits(spiketimes, dt):
  spiketimes = np.int64(np.ceil(spiketimes/dt))
  spikebits = np.zeros( np.max(spiketimes) + 1 )
  spikebits[spiketimes] = 1.0
  return spikebits
