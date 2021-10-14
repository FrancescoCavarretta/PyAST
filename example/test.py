"""
  a small example on the generation of artificial spike trains,
  using a template from an experimental one
"""

import numpy as np
from PyAST import IRate, SpikeTrainGeneratorIRate
import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 2)


def load(filename):
  vec = []
  with open(filename, 'r') as fi:
    l = fi.readline()
    while l:
      vec.append(float(l))
      l = fi.readline()
  return np.array(vec)


# read the spike times
# the time unit is in tenth of ms < ====================================
experimentalSpikeTimes = load('05252011_mice_630_chan_2_1220_PC_chan_3_575_MF_with_B_W_3_MF.txt')


# this object encapsulate the experimental spike times
objIRate = IRate(experimentalSpikeTimes, 0.003, TimeUnitIn='tenth_of_ms')

# statistics associated to the Exp. Spike Train
print (objIRate.getSpikeTrainStats())

# let's get a template
objIRateTemplate = objIRate.getIRateTemplate()

# plot the template
ax[0,0].plot(objIRateTemplate.IRateDistribution[:,0], objIRateTemplate.IRateDistribution[:,1], color='black', label='Template')
ax[0,0].eventplot(objIRateTemplate.IRateData.OriginalSpikeTime, lineoffsets=np.mean(objIRateTemplate.IRateDistribution[:,1]) * 0.5, label='Original Spike Times', color='blue')
ax[0,0].eventplot(objIRateTemplate.IRateData.SpikeTime, lineoffsets=np.mean(objIRateTemplate.IRateDistribution[:,1]) * 1.5, label='Preprocessed Spike Times', color='red')
ax[0,0].legend()
ax[0,0].set_xlabel('s')
ax[0,0].set_ylabel('Inst. F. Rate (Hz)')
ax[0,0].set_xlim([0,40])
ax[0,0].set_ylim([0,100])
ax[0,0].set_title('Template against the Exp. Spike Train')

ax[0,1].plot(objIRateTemplate.IRateDistribution[:,0], objIRateTemplate.IRateDistribution[:,1], color='black', label='Template')
ax[0,1].eventplot(objIRateTemplate.IRateData.OriginalSpikeTime, lineoffsets=np.mean(objIRateTemplate.IRateDistribution[:,1]) * 0.5, label='Original Spike Times', color='blue')
ax[0,1].eventplot(objIRateTemplate.IRateData.SpikeTime, lineoffsets=np.mean(objIRateTemplate.IRateDistribution[:,1]) * 1.5, label='Preprocessed Spike Times', color='red')
ax[0,1].set_xlabel('s')
ax[0,1].set_ylabel('Inst. F. Rate (Hz)')
ax[0,1].set_xlim([38,42])
ax[0,1].set_ylim([0,100])
ax[0,1].set_title('Template against the Exp. Spike Train: Zoom of the panel on the left')

# instantiate a spike train generator
objAST_Gen = SpikeTrainGeneratorIRate(253, objIRateTemplate)

# generate 50 spike trains
artificialSpikeTimes = objAST_Gen.get(n=50)

# plot the artificial spike trains
for irow, _objIRate_AST in enumerate(artificialSpikeTimes):
  ax[1,0].eventplot(_objIRate_AST.SpikeTime, lineoffsets=irow*2, color='black')
ax[1,0].set_xlabel('s')
ax[1,0].set_xlim([0,40])
ax[1,0].set_ylim([-1,100])
ax[1,0].set_title('Artificial Spike Trains')

# plot the artificial spike trains
for irow, _objIRate_AST in enumerate(artificialSpikeTimes):
  ax[1,1].eventplot(_objIRate_AST.SpikeTime, lineoffsets=irow*2, color='black')
ax[1,1].set_xlabel('s')
ax[1,1].set_xlim([38,42])
ax[1,1].set_ylim([-1,100])
ax[1,1].set_title('Artificial Spike Trains: Zoom of the panel on the left')

plt.tight_layout()
plt.show()
