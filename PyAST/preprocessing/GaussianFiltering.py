import numpy
from . import spikebits

""" build a gaussian filter """
def mk_gaussian_filter(t, mean=0.0, std=0.0):
  return 1.0/(std*numpy.sqrt(2*numpy.pi)) * numpy.exp( -0.5 * (( (t-mean)/std )**2) )

def convolve(src, f):
  z = numpy.convolve(src, f, mode='same')
  if len(f) > len(src):
    diff = int((len(f)-len(src))/2)
    z = z[diff:-diff]
  return z
    

""" convolution with gaussian filter """
def FixedGaussianFiltering(spiketimes, dt, width=3.0):
  
  _spiketimes = spikebits.spikebits(spiketimes, dt)

  #import matplotlib.pyplot as plt
  #plt.eventplot(spiketimes)
  #plt.eventplot(_spiketimes)
  #plt.show()

  # create a gaussian filter
  # see Paulin 1995 for Sigma Vs FR relation. *4)
  gwidth  = 1.0/(numpy.sqrt(2*numpy.pi)*width)
  gfilter = mk_gaussian_filter(numpy.arange(-1.0, 1.0+dt, dt), std=gwidth)

  # convolution
  #z = numpy.convolve(_spiketimes,
  #                   gfilter,
  #                   mode='same')
  z = convolve(_spiketimes, gfilter)
  return numpy.arange(0, len(z), 1.0)*dt, z

                 



def AdaptiveGaussianFiltering(spiketimes, fixed_gaussian_template, dt, width=4.0):
  z   = numpy.zeros(len(fixed_gaussian_template[0]))
  
  #import matplotlib.pyplot as plt
  #plt.plot(range(len(fixed_gaussian_template[1])),fixed_gaussian_template[1])
  #plt.show()
  
  for tspk in spiketimes:
    i = numpy.int64(numpy.round(tspk/dt))
    #print ("i=%g %g"%(i,len(z)))
    
    ## create Gaussian filter
    gwidth = 1/(numpy.sqrt(2*numpy.pi)*(fixed_gaussian_template[1][i]/width))
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
    z[_min_i_z:(_max_i_z+1)] += gfilter[_min_i_f:(_max_i_f+1)]
    #plt.plot(range(len(gfilter)),gfilter)
  #plt.show()
  return numpy.arange(0, len(z), 1.0)*dt, z
