


import numpy as np
def load(filename):
  vec = []
  with open(filename, 'r') as fi:
    l = fi.readline()
    while l:
      vec.append(float(l))
      l = fi.readline()
  return np.array(vec)



SpikeTimes = load('wichmann_data.txt')*0.001

# create an object that encapsulate the instantaneous firing rate
# and generate a spike template
import IRate
objIRate = IRate.IRate(SpikeTimes, 0.003)
templateIRate = list(objIRate.getIRateTemplate())
import matplotlib.pyplot as plt
plt.plot(templateIRate[0], templateIRate[1])
plt.xlabel('s')
plt.ylabel('Inst F Rate (Hz)')
plt.show()

# generate one spike train
import SpikeGeneration
ArtificialSpikeTrain = SpikeGeneration.GenerateSpikeTrain(objIRate, UnGamma=8.)


import matplotlib.pyplot as plt
plt.eventplot(ArtificialSpikeTrain.SpikeTime, linewidth=.5, linelengths=0.5)
plt.show()
