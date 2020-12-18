import numpy

""" remove spike that occurs earlier than refractory period """
def AdjustISIs(SpikeTime, RefPeriod):

  """ get positions of spike to remove """
  def spikes_to_delete():
    try:
      return numpy.argwhere( ( SpikeTime[1:] - SpikeTime[:-1] ) <= RefPeriod) + 1
    except:
      return []

    
  """ adjust """
  idx = spikes_to_delete()
  while len(idx):
    SpikeTime = numpy.delete(SpikeTime, idx) 
    idx = spikes_to_delete()

  return SpikeTime
