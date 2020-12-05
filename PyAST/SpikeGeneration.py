import numpy as np
from . import IRate

"""
  Generate a spike train
"""
def GenerateSpikeTrain(objIRate, UnGamma=None, Precision=3):

  """ check validity of the number and convert """
  def RateToISI(FRate, MaxFRate):
      # check
      if np.isnan(FRate) or np.isinf(FRate) or FRate > MaxFRate:
        FRate = MaxFRate
      return 1.0/FRate    

  
  # this method return always a spike time in Hertz
  # The CurrentISI will be expressed in seconds
  templateIRate = objIRate.getIRateTemplate()
  Reg = objIRate.getSpikeTrainStats()['Processed']['Regularity']
  
  # Pull spike times from Gamma distribution to generate AST
  # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
  ISIs = []

  I = 0
  while I < len(templateIRate):


    # gamrnd = matlab fn for random arrays from gamma distribution. 
    # Given arguments get a mean firing rate of 1
    X = np.random.gamma(Reg, scale=1.0/Reg)
        

    J = I
    for z in range(Precision):
      # calculate mean rate over expected mean interval
      MeanRate = np.mean(templateIRate.IRateDistribution[I:(J+1), 1])
      
      # Add refractory period back in
      CurrentISI = X*RateToISI(MeanRate, 1.0/objIRate.RefractoryPeriod)   
      
      # calculate the interval boundary
      J = min([ len(templateIRate)-1, I+int(round(CurrentISI/templateIRate.TimeBinSz)) ])


    if UnGamma:
      # for cases where templates have sudden large
      # increases in rate, which leads to very slow catchup performance wiht
      # default algorithm.  If algorithmflag==2 then the current interval is
      # examied for rate changes of factor > ungam, and if one is found, the
      # maximal rate for the original interval is determined.  Then the
      # original interval is shortened to the time where the rate exceeds
      # ungam, and a 2nd interval for the new max rate is added.
      MaxRate = np.max(templateIRate.IRateDistribution[I:(J+1), 1])
      if MaxRate > UnGamma*templateIRate.IRateDistribution[I, 1]:
        CurrentISI = X*RateToISI(MaxRate, 1.0/objIRate.RefractoryPeriod)
    
    
    ISIs.append(CurrentISI)
    I += int(round(CurrentISI/templateIRate.TimeBinSz))


  # spike times
  SpikeTimes = np.cumsum(ISIs)
  SpikeTimes = SpikeTimes[SpikeTimes <= templateIRate.IRateDistribution[-1, 0]]

  return IRate.IRate(SpikeTimes, objIRate.RefractoryPeriod, 's')
