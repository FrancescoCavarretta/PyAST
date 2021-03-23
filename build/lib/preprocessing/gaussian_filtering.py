import numpy
import spikebits

""" build a gaussian filter """
def mk_gaussian_filter(t, mean=0.0, std=0.0):
  return 1.0/(std*numpy.sqrt(2*numpy.pi)) * numpy.exp( -0.5 * (( (t-mean)/std )**2) )


""" convolution with gaussian filter """
def fixed_gaussian_filtering(spiketimes, dt, width=3.0):
  _spiketimes = spikebits.spikebits(spiketimes)

  # create a gaussian filter
  # see Paulin 1995 for Sigma Vs FR relation. *4)
  gwidth  = 1.0/(np.sqrt(2*np.pi)*width)
  gfilter = mk_gaussian_filter(numpy.arange(-1.0, 1.0+dt, dt), std=gwidth)

  # convolution
  z = numpy.convolve(_spiketimes,
                     gfilter,
                     mode='same')

  return np.arange(0, len(z), 1.0)*dt, z

                 



def adaptive_gaussian_filtering(spiketimes, fixed_gaussian_template, dt, width=4.0):
  z   = np.zeros(len(fixed_gaussian_template[0]))
  
  
  for tspk in spiketimes:
    i = np.int64(np.ceil(tspk/dt))

    
    ## create Gaussian filter
    gwidth = 1/(np.sqrt(2*np.pi)*fixed_gaussian_template[1][i])*width
    gfilter = mk_gaussian_filter(numpy.arange(-1.0, 1.0+dt, dt), std=gwidth) 

    # Check edge effects, and add in the current gauss/spike
    _filter_half_width = int(len(gfilter)/2)

    
    _min_i_z = i - _filter_half_width
    _min_i_f = 0
    if _min_i_z < 0:
      # never switch the order of min_i_f and min_i_z
      _min_i_f += -_min_i_z
      _min_i_z = 0
      
    _max_i_z = i + _filter_half_width
    _max_i_f = len(gfilter)-1
    if _max_i_z >= len(z):
      # never switch the order of max_i_f and max_i_z
      _max_i_f -= _max_i_z-(len(z)-1)
      _max_i_z = len(z)-1

    # convolve
    z[_min_i_z:_max_i_z] += gfilter[_min_i_f:_max_i_f]
    
  return np.arange(0, len(z), 1.0)*dt, z
