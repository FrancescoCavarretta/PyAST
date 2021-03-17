import numpy as np
from . import IRate


irnd = 0
max_irnd = 10

def gamma(a,b):
  global irnd
  X = np.random.gamma(a, scale=b)
  irnd += 1
  if irnd % max_irnd:
    np.random.seed(irnd)
  return X


def _GenerateSpikeTrain(Reg, templateIRate, RefractoryPeriod, UnGamma=None, Precision=3, MaxFRate=None, MinFRate=None):

  """ check validity of the number and convert """
  def RateToISI(X, FRate, MaxFRate, MinFRate):
      # check
      if np.isnan(FRate) or np.isinf(FRate):
        FRate = MaxFRate

      ISI = X/FRate
      
      if ISI < 1.0/MaxFRate:
        ISI = 1.0/MaxFRate
      elif ISI > 1.0/MinFRate:
        ISI = 1.0/MinFRate
        
      return ISI  

  if MaxFRate is None:
    MaxFRate = 1.0/RefractoryPeriod

  if MinFRate is None:
    MinFRate = 1e-5
    

  # Pull spike times from Gamma distribution to generate AST
  # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
  ISIs = []

  I = 0
  
  while I < len(templateIRate):
    # gamrnd = matlab fn for random arrays from gamma distribution. 
    # Given arguments get a mean firing rate of 1
    X = gamma(Reg, 1.0/Reg)
        

    J = I
    for z in range(Precision):
      # calculate mean rate over expected mean interval
      MeanRate = np.mean(templateIRate.IRateDistribution[I:(J+1), 1])
      
      # Add refractory period back in
      CurrentISI = RateToISI(X, MeanRate, MaxFRate, MinFRate)   
      
      # calculate the interval boundary
      #print ("\tError: ", CurrentISI, X, MeanRate, 1.0/objIRate.RefractoryPeriod)
      #try:
      J = min([ len(templateIRate)-1, I+int(round(CurrentISI/templateIRate.TimeBinSz)) ])
      #except:
      #  print ("Error: ", CurrentISI)
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
        CurrentISI = RateToISI(X, MaxRate, MaxFRate, MinFRate)
    
    
    ISIs.append(CurrentISI)
    I += int(round(CurrentISI/templateIRate.TimeBinSz))


  # spike times
  SpikeTimes = np.cumsum(ISIs)
  SpikeTimes = SpikeTimes[SpikeTimes <= templateIRate.IRateDistribution[-1, 0]]

  return IRate.IRate(SpikeTimes, RefractoryPeriod, 's')




"""
  Generate a spike train
"""
def GenerateSpikeTrain(objIRate, UnGamma=None, Precision=3, MaxFRate=None, MinFRate=None):
  # this method return always a spike time in Hertz
  # The CurrentISI will be expressed in seconds
  templateIRate = objIRate.getIRateTemplate()
  Reg = objIRate.getSpikeTrainStats()['Processed']['Regularity']
  RefractoryPeriod = objIRate.RefractoryPeriod
  return _GenerateSpikeTrain(Reg, templateIRate, RefractoryPeriod, UnGamma=UnGamma, Precision=Precision, MaxFRate=MaxFRate, MinFRate=MinFRate)



"""
  Merge two spike trains
"""
def MergeSpikeTrains(objIRateBaseline, objIRateModulation):
  SpikeTimeRes = []
  i = 0
  j = 0

  
  while i < len(objIRateBaseline):
    if objIRateBaseline[i] <= objIRateModulation[j]:
      SpikeTimeRes.append(objIRateBaseline[i])
      i += 1
    else:
      break

  
  while j < len(objIRateModulation):
    SpikeTimeRes.append(objIRateModulation[j])
    j += 1

      
  while i < len(objIRateBaseline):
    if objIRateBaseline[i] <= SpikeTimeRes[-1]:
      i += 1
    else:
      break

  while i < len(objIRateBaseline):
    SpikeTimeRes.append(objIRateBaseline[i])
    i += 1

  return IRate.IRate(SpikeTimeRes, min([objIRateModulation.RefractoryPeriod, objIRateBaseline.RefractoryPeriod]))
