import numpy as np
import IRate

"""
  Generate a spike train
"""
def GenerateSpikeTrain(objIRate, UnGamma=None, Precision=3):
  # this method return always a spike time in Hertz
  # The CurrentISI will be expressed in seconds
  templateIRateTemplate = objIRate.getIRateTemplate()
  
  # Time Scale Factor for the Y/X Axis of the template
  TimeScaleFactor = objIRate._getTimeScaleFactorXY()
  
  templateIRateTemplate = 1.0/(1.0/templateIRateTemplate - objIRate.RefractoryPeriod)
  
  Reg = objIRate.getSpikeTrainStats()['Regularity']
  
  # Pull spike times from Gamma distribution to generate AST
  # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
  ISIs = []

  I = 0
  while I < len(templateIRateTemplate):
    # gamrnd = matlab fn for random arrays from gamma distribution. 
    # Given arguments get a mean firing rate of 1
    X = np.random.gamma(Reg, 1.0/Reg)
        

    J = I
    for z in range(Precision):
      # calculate mean rate over expected mean interval
      MeanRate = np.mean(templateIRateTemplate[I:J])    
      CurrentISI = X/MeanRate 
        
      # calculate the interval boundary
      J = max([ len(templateIRateTemplate)-1, I + int(CurrentISI*TimeScaleFactor) ])
    
    

    if UnGamma:
      # for cases where templates have sudden large
      # increases in rate, which leads to very slow catchup performance with
      # default algorithm.  If algorithmflag==2 then the current interval is
      # examied for rate changes of factor > ungam, and if one is found, the
      # maximal rate for the original interval is determined.  Then the
      # original interval is shortened to the time where the rate exceeds
      # ungam, and a 2nd interval for the new max rate is added.      
      MaxRate = np.max(templateIRateTemplate[I:J])
      
      #found ungamfold increase in rate
      if MaxRate > UnGamma*templateIRateTemplate[I]:
        CurrentISI = X/MaxRate
    

    # Add refractory period back in
    CurrentISI += objIRate.RefractoryPeriod
    
    ISIs = [ ISIs, CurrentISI ]
    I += int(CurrentISI*TimeScaleFactor)

  # spike times
  SpikeTimes = np.cumsum(ISIs)

  return IRate.IRate(SpikeTimes, objIRate.RefractoryPeriod, objIRate.XUnit)
