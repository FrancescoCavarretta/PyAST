import numpy
import preprocessing
import SpikeStats

""" embed a spike train recorded experimentally """
class IRate:
  def __init__(self, SpikeTime, RefractoryPeriod, TimeUnitIn, TimeUnitOut='ms'):   
    if type(SpikeTime) != numpy.ndarray:
      SpikeTime = numpy.array(SpikeTime)

    self._TimeScaleFactors = { 's':1.0, 'ms':0.001 }
    #self._FrequencyScaleFactors = { 'GHz':1.0e+6, 'MHz':1.0e+3, 'Hz':1.0 }
    
    TimeScaleFactorIn  = self._TimeScaleFactors[TimeUnitIn]
    TimeScaleFactorOut = self._TimeScaleFactors[TimeUnitOut]
    TimeScaleFactor = TimeScaleFactorOut/TimeScaleFactorIn
    
    self.SpikeTime = SpikeTime * TimeScaleFactor
    self.RefractoryPeriod = RefractoryPeriod*TimeScaleFactor

    # remove spikes occurring within an ISI smaller than RefPeriod   
    self.SpikeTime = preprocessing.refractory_period.adjust_isi(self.SpikeTime, self.RefractoryPeriod)
    
    self.XUnit = TimeUnitOut
    self.YUnit = 'Hz'


  """ extract the firing template """
  def getIRateTemplate(self, dt=0.001):
    g_template = preprocessing.gaussian_filtering.fixed_gaussian_filtering(self.SpikeTime, dt)
    a_template = preprocessing.gaussian_filtering.adaptive_gaussian_filtering(self.SpikeTime, g_template, dt)
    return a_template

  """ return various statistics of spike trains """
  def getSpikeTrainStats(self):
    return SpikeStats.getStats(self.SpikeTime)
  

  """ used during spike generation to scale the time """
  def _getTimeScaleFactor(self):
    return self._TimeScaleFactors[self.XUnit] #*self._FrequencyScaleFactors[self.YUnit]
