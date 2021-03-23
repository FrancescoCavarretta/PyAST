import numpy
mean_isi_baseline = 20.0
l = 10

def get_isi(x, isi_mean, isi_min):
  # boundaries
  assert x > 0 and x < 1
  
  # upper bound for Novelty
  Nmax = -numpy.log(1-numpy.exp(-isi_min/isi_mean))/numpy.log(2)
  
  N = Nmax*x
  
  # look at novelty measure
  isi = -numpy.log(1 - 2 ** (-N) ) * isi_mean
  
  return isi


def spk_train(burst=False):
  tspk = [0.]

  for iteration in range(20):
    for i in range(20):
      tspk.append(tspk[-1]+numpy.random.poisson(mean_isi_baseline))
    
    if burst:
      for i in range(20):
        isi_mean = tspk[-1] - tspk[-1-l]
        isi_min  = tspk[-1] - tspk[-l]
        tspk.append(tspk[-l] + get_isi(0.95, isi_mean, isi_min))
  data = [tspk[i]-tspk[i-1] for i in range(1, len(tspk))]
  return tspk, data



import matplotlib.pyplot as plt
#plt.hist(spk_train(True)[1], bins=30)
#plt.hist(spk_train()[1], bins=30, color='red', histtype='step', linewidth=2.0)
plt.eventplot(spk_train(True)[0])
plt.show()
