import numpy as np
from . import IRate

"""
  Generate a spike train
"""
def GenerateSpikeTrain(templateIRate, UnGamma=None, Precision=3, MaxFRate=None, MinFRate=None, seed=None, RefractoryPeriod=0.003, Regularity=None):
##  print (templateIRate.IRateDistribution)
##  import matplotlib.pyplot as plt
##  plt.plot(templateIRate.IRateDistribution[:, 0], templateIRate.IRateDistribution[:, 1])
##  plt.show()



  
  """ check validity of the number and convert """
  def RateToISI(FRate, MaxFRate, MinFRate):
      # check
      if np.isnan(FRate) or np.isinf(FRate) or FRate > MaxFRate:
        FRate = MaxFRate
      elif FRate < MinFRate:
        FRate = MinFRate
        
      return 1.0/FRate    

  if MaxFRate is None:
    try:
      MaxFRate = 1.0/templateIRate.IRateData.RefractoryPeriod
    except AttributeError:
      MaxFRate = 1.0/RefractoryPeriod
      

  if MinFRate is None:
    MinFRate = 1e-5
    
  # this method return always a spike time in Hertz
  # The CurrentISI will be expressed in seconds
  # templateIRate = objIRate.getIRateTemplate()
  try:
    Reg = templateIRate.IRateData.getSpikeTrainStats()['Processed']['Regularity']
  except AttributeError:
    Reg = Regularity

  # Pull spike times from Gamma distribution to generate AST
  # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
  ISIs = []

  I = 0

  # instantiate random number generator
  if seed is None:
    seed = 0
  rng = np.random.Generator(np.random.Philox(seed))



  
  while I < len(templateIRate):
    # gamrnd = matlab fn for random arrays from gamma distribution. 
    # Given arguments get a mean firing rate of 1
    X = rng.gamma(Reg, scale=1.0/Reg) #np.random.gamma(Reg, scale=1.0/Reg)
        

    J = I
    for z in range(Precision):
      # calculate mean rate over expected mean interval
      MeanRate = np.mean(templateIRate.IRateDistribution[I:(J+1), 1])
      
      # Add refractory period back in
      CurrentISI = X*RateToISI(MeanRate, MaxFRate, MinFRate)   
      
      # calculate the interval boundary
      #print ("\tError: ", CurrentISI, X, MeanRate, 1.0/objIRate.RefractoryPeriod)
      try:
        J = min([ len(templateIRate)-1, I+int(round(CurrentISI/templateIRate.TimeBinSz)) ])
      except:
        print ("Error: ", CurrentISI, X, Reg, 1.0/Reg, RateToISI(MeanRate, MaxFRate, MinFRate)   )
    #print ("Spike interval", I, J)

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
        CurrentISI = X*RateToISI(MaxRate, MaxFRate, MinFRate)
    
    
    ISIs.append(CurrentISI)
    I += int(round(CurrentISI/templateIRate.TimeBinSz))


  # spike times
  SpikeTimes = np.cumsum(ISIs)
  SpikeTimes = SpikeTimes[SpikeTimes <= templateIRate.IRateDistribution[-1, 0]]
  try:
    return IRate.IRate(SpikeTimes, templateIRate.IRateData.RefractoryPeriod, 's')
  except AttributeError:
    return IRate.IRate(SpikeTimes, RefractoryPeriod, 's')
