


import numpy as np
def load(filename):
  vec = []
  with open(filename, 'r') as fi:
    l = fi.readline()
    while l:
      vec.append(float(l))
      l = fi.readline()
  return np.array(vec)



SpikeTimes = load('/home/francesco/Downloads/ASTGeneration_Main/MFdata/37/05252011_mice_630_chan_2_1220_PC_chan_3_575_MF_with_B_W_3_MF.txt');

# create an object that encapsulate the instantaneous firing rate
# and generate a spike template
from PyAST import IRate
objIRate = IRate.IRate(SpikeTimes, 0.003, 'tenth_of_ms')


templateIRate = objIRate.getIRateTemplate()
x=[]
y=[]
with open('/home/francesco/curves.txt', 'r') as fi:
  l=fi.readline()
  while l:
    tk=l.split()
    x.append(float(tk[0]))
    y.append(float(tk[1]))
    l=fi.readline()
import matplotlib.pyplot as plt
plt.plot(templateIRate.IRateDistribution[:, 0], templateIRate.IRateDistribution[:, 1])
plt.plot(x,y,color='green')
plt.xlabel('s')
plt.ylabel('Inst F Rate (Hz)')

# generate one spike train
from PyAST import SpikeGeneration
templateIRate_1 = None
n=10
for k in range(n):
  ArtificialSpikeTrain = SpikeGeneration.GenerateSpikeTrain(objIRate, UnGamma=8, Precision=3)
  templateIRate_2 = ArtificialSpikeTrain.getIRateTemplate()
  if templateIRate_1 is None:
    templateIRate_1 = templateIRate_2.IRateDistribution
  else:
    L = min([len(templateIRate_1),len(templateIRate_2.IRateDistribution)])
    templateIRate_1 = templateIRate_1[:L, :]+templateIRate_2.IRateDistribution[:L, :]
    
templateIRate_1 /= n

plt.plot(templateIRate_1[:,0], templateIRate_1[:,1], color='red')
plt.show()
plt.eventplot(ArtificialSpikeTrain.SpikeTime, linewidth=.5, linelengths=0.5)
plt.show()
#print (ArtificialSpikeTrain.getSpikeTrainStats())
