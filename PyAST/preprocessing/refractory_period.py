import numpy

""" remove spike that occurs earlier than refractory period """
def adjust_isi(spiketimes, refractory_period):

  """ get positions of spike to remove """
  def get_spike_to_delete():
    idx = numpy.argwhere( (spiketimes[1:] - spiketimes[:-1]) <= refractory_period)
    if len(idx) > 0:
      idx += 1
    return idx

  spk_idx = get_spike_to_delete()
  while len(spk_idx):
      spiketimes = numpy.delete(spiketimes, spk_idx) 
      spk_idx = get_spike_to_delete()


  return spiketimes
