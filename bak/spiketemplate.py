import preprocessing
import spikestats

def mk_template(spiketimes, ref_per, dt):
  _spiketimes = preprocessing.refractory_period.adjust_isi(spiketimes, ref_per)
  g_template = preprocessing.gaussian_filtering.fixed_gaussian_filtering(_spiketimes, dt)
  a_template = preprocessing.gaussian_filtering.adaptive_gaussian_filtering(_spiketimes, g_template, dt)
  fr_reg = spikestats.calculate(_spiketimes)[3:]
  return a_template, fr_reg
