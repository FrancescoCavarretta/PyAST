import numpy as np


## LV
def LV(ISIs):
  num   = np.power(ISIs[1:]-ISIs[:-1], 2.0)
  denom = np.power(ISIs[1:]+ISIs[:-1], 2.0)
  
  num = np.delete(num, denom <= 0)
  denom = np.delete(denom, denom <= 0)
  lv = 3*np.mean(num/denom)
  return lv




def getStats(SpikeTime):
  stats = {}
  ISIs = SpikeTime[1:] - SpikeTime[:-1]
  MeanRate = 1.0/np.mean(ISIs)
  MeanCV   = np.std(ISIs)/np.mean(ISIs)
  MeanLV   = LV(ISIs)
  Reg      = (3-MeanLV)/(2*MeanLV)
  stats['Mean'] = MeanRate
  stats['ISI_CV'] = MeanCV
  stats['LV'] = MeanLV
  stats['Regularity'] = Reg
  return stats
