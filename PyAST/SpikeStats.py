import numpy as np

def get(SpikeTime):

  ## LV
  def LV(ISIs):
    return 3*np.mean(np.power(ISIs[1:]-ISIs[:-1], 2.0)/np.power(ISIs[1:]+ISIs[:-1], 2.0))





  stats = {}
  ISIs = SpikeTime[1:] - SpikeTime[:-1]
  MeanRate = 1.0/np.mean(ISIs)
  MeanCV   = np.std(ISIs)/np.mean(ISIs)
  MeanLV   = LV(ISIs)
  Reg      = (3-MeanLV)/(2*MeanLV)
  stats['Mean Rate (Hz)'] = MeanRate
  stats['ISI_CV'] = MeanCV
  stats['LV'] = MeanLV
  stats['Regularity'] = Reg
  return stats


###
# Tk = T(k-l) + F^(-1) ( 2^N(l,k) )
