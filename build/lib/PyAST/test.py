import SpikeGenerationBurst as sgb



if __name__ == '__main__':
  import numpy as np
  def load(filename):
    vec = []
    with open(filename, 'r') as fi:
      l = fi.readline()
      while l:
        vec.append(float(l))
        l = fi.readline()
    return np.array(vec)



  SpikeTimes = load('example/wichmann_data.txt')*0.001
  objIRate = sgb.IRate(SpikeTimes, 0.003)


  templateBurst = objIRate.getIRateTemplate()
  print ( templateBurst.IRateDistribution)
