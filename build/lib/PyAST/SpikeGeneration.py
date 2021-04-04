import numpy as np
from . import IRate


""" spike train generator """
class  SpikeTrainGenerator:
  def __init__(self, seed, time, frequency, RefractoryPeriod, Regularity, UnGamma=None, Precision=10, MaxFRate=None, MinFRate=None):
    self.seed = seed
    self.time = time
    self.frequency = frequency
    self.RefractoryPeriod = RefractoryPeriod
    self.Regularity = Regularity
    self.UnGamma = UnGamma
    self.Precision = Precision
    self.MaxFRate = MaxFRate
    self.MinFRate = MinFRate
    self._seed = seed
    
    
  """ reset the internal seed """
  def reset(self):
    self._seed = self.seed
    
    
  """ Generate a spike train """
  def get(self, n=1):
    spike_train = []
    
    for i in range(n):
      spike_train.append(self._GenerateSpikeTrain(self._seed,
                               self.time/1000.0,
                               self.frequency,
                               self.RefractoryPeriod,
                               self.Regularity,
                               UnGamma=self.UnGamma,
                               Precision=self.Precision,
                               MaxFRate=self.MaxFRate,
                               MinFRate=self.MinFRate))
      
      self._seed += 1 # increment the internal seed
    
    return spike_train
      

  """
    Generate a spike train
  """
  def _GenerateSpikeTrain(self, seed, time, frequency, RefractoryPeriod, Regularity, UnGamma=None, Precision=10, MaxFRate=None, MinFRate=None):
    """ let's test the consistency of the configuration """
    if MaxFRate is None:
      MaxFRate = 1.0/RefractoryPeriod
      
    if MinFRate is None:
      MinFRate = 1e-5
    
    assert MinFRate < MaxFRate
    assert MaxFRate <= 1.0/RefractoryPeriod
    
    # calculate time bin size
    TimeBinSz = time[1] - time[0]
    
    
    """ check validity of the number and convert """
    def RateToISI(FRate):
      if FRate > MaxFRate:
        FRate = MaxFRate
      elif FRate < MinFRate:
        FRate = MinFRate
        
      try:
        return 1.0/FRate 
      except:
        return 1.0/MaxFRate
  
  
    rng = np.random.Generator(np.random.Philox(seed))
  
    # Pull spike times from Gamma distribution to generate AST
    # Params for Gamma: rate from rate template (and k from Lv distribution = reg)
    ISIs = []
    I = 0
    while I < len(frequency):
      # gamrnd = matlab fn for random arrays from gamma distribution. 
      # Given arguments get a mean firing rate of 1
      X = rng.gamma(Regularity, scale=1.0/Regularity) #np.random.gamma(Reg, scale=1.0/Reg)
          
  
      J = I
      for z in range(Precision):
        MeanRate = np.mean(frequency[I:(J+1)]) # calculate mean rate over expected mean interval
        CurrentISI = X*RateToISI(MeanRate)  
        J = min([ len(frequency)-1, I+int(round(CurrentISI/TimeBinSz)) ])  # calculate the interval boundary
        
        
  
      if UnGamma:
        # for cases where templates have sudden large
        # increases in rate, which leads to very slow catchup performance wiht
        # default algorithm.  If algorithmflag==2 then the current interval is
        # examied for rate changes of factor > ungam, and if one is found, the
        # maximal rate for the original interval is determined.  Then the
        # original interval is shortened to the time where the rate exceeds
        # ungam, and a 2nd interval for the new max rate is added.
        MaxRate = np.max(frequency[I:(J+1)])
        if MaxRate > UnGamma*frequency[I]:
          CurrentISI = X*RateToISI(MaxRate)
      
      
      ISIs.append(CurrentISI)
      I += int(round(CurrentISI/TimeBinSz))
  
  
    # spike times
    SpikeTimes = np.cumsum(ISIs)
    SpikeTimes = SpikeTimes[SpikeTimes <= time[-1]]
    return SpikeTimes
  
  



""" extended version for templates """
class SpikeTrainGeneratorIRate(SpikeTrainGenerator):
  def __init__(self, seed, templateIRate, UnGamma=None, Precision=10, MaxFRate=None, MinFRate=None):
    SpikeTrainGenerator.__init__(self,
                                 seed,
                                 templateIRate.IRateDistribution[:,0],
                                 templateIRate.IRateDistribution[:,1],
                                 templateIRate.IRateData.RefractoryPeriod,
                                 templateIRate.IRateData.getSpikeTrainStats()['Processed']['Regularity'],
                                 UnGamma=UnGamma, Precision=Precision, MaxFRate=MaxFRate, MinFRate=MinFRate)
    
    
  def _GenerateSpikeTrain(self, seed, time, frequency, RefractoryPeriod, Regularity, UnGamma=None, Precision=10, MaxFRate=None, MinFRate=None):
    return IRate.IRate(super()._GenerateSpikeTrain(seed, 
                       time, frequency, RefractoryPeriod, 
                       Regularity, 
                       UnGamma=UnGamma, Precision=Precision, MaxFRate=MaxFRate, MinFRate=MinFRate), RefractoryPeriod, 's')

  