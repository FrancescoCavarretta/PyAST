import numpy
from .preprocessing import RefractoryPeriod as RefPeriodProcessing, GaussianFiltering
from . import SpikeStats

""" embed a spike train recorded experimentally """
class IRate:
  def __init__(self, SpikeTime, RefractoryPeriod, TimeUnitIn='s'):   
    if type(SpikeTime) != numpy.ndarray:
      SpikeTime = numpy.array(SpikeTime)


    TimeScaleFactor =  { 's':1.0, 'ms':0.001, 'tenth_of_ms':0.0001 }[TimeUnitIn] 

    # convert to seconds
    self.RefractoryPeriod = RefractoryPeriod
    self.OriginalSpikeTime = SpikeTime * TimeScaleFactor

    # remove spikes occurring within an ISI smaller than RefPeriod 
    self.SpikeTime = RefPeriodProcessing.AdjustISIs(self.OriginalSpikeTime, self.RefractoryPeriod)
    

  """ return various statistics ofs spike trains """
  def getSpikeTrainStats(self):
    return { 'Diff':(len(self.OriginalSpikeTime)-len(self.SpikeTime)), 'Raw':SpikeStats.get(self.OriginalSpikeTime), 'Processed':SpikeStats.get(self.SpikeTime) }


  """ extract the firing template """
  def getIRateTemplate(self, TimeBinSz=.001):
    return IRateTemplate(self, TimeBinSz)

  """ length """
  def __len__(self):
    return len(self.SpikeTime)

  """ item """
  def __getitem__(self, i):
    return self.SpikeTime[i]


  




""" Spike Rate Template """
class IRateTemplate(IRate):
  def __init__(self, IRateData, TimeBinSz=0.001):
    self.TimeBinSz = TimeBinSz

    if isinstance(IRateData, IRate):
      self.IRateData = IRateData
      
      _IRateDistribution = GaussianFiltering.AdaptiveGaussianFiltering(
        self.IRateData.SpikeTime,
        GaussianFiltering.FixedGaussianFiltering(self.IRateData.SpikeTime, self.TimeBinSz),
        self.TimeBinSz)
    else:
      _IRateDistribution = IRateData
    
    # reshape
    _IRateDistribution = numpy.concatenate(([_IRateDistribution[0]], [_IRateDistribution[1]]), axis=0)
    self.IRateDistribution = _IRateDistribution.T
      

  def __getitem__(self, index):
    return self.IRateDistribution[index, :]


  def __len__(self):
    return len(self.IRateDistribution[:, 0])
