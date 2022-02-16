
import neuron 


class NrnSpikeTrainGenerator:
  """
    (Online) Spike Train Generation
    Args:
      isi_gen: definition of the spike train distribution
      netcons(optional):netcons which should be activated at each spike time
  """
  def __init__(self, isi_gen, netcons={}):
    self.isi_gen = isi_gen # isi random generator
    self._netcons = netcons # netcons activated at each spike time by calling _spike_ev
    self.reset() # reset
    

  """
    add destination
  """
  def add_destination(self, dest):
    self._netcons[dest] = neuron.h.NetCon(None, dest)
    self._netcons[dest].weight[0] = 1.0

  """
    del destination
  """
  def del_destination(self, dest):
    del self._netcons[dest]
    

  """
    initiatialization
  """
  def reset(self):
    self.isi_gen.reset()
    self.spike_time = self.isi_gen.get() # spike time
    self._fih = neuron.h.FInitializeHandler(0.0, (self._init_spike_ev, (self.spike_time,))) # NEURON handle
    

  """
    initialization of spike event generation online by enqueuing the first spike
  """
  def _init_spike_ev(self, spike_time):
    neuron.h.cvode.event(spike_time, (self._spike_ev)) # enqueue in NEURON
    

  """
    spike event generation online
    one after another
  """
  def _spike_ev(self):
    # activate the netcons
    for nc in self._netcons.values():
      nc.event(neuron.h.t)

    isi = self.isi_gen.get() # if the ISI is None, means the spike train is over
    
    if isi is not None:
      self.spike_time +=  isi # generate next spike time
      neuron.h.cvode.event(self.spike_time, (self._spike_ev))
        
  
