import PyAST.SpikeGenerationBurst as sgb



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
  objIRateBurst = sgb.IRate.IRate(SpikeTimes, 0.0001)
  templateBurst  = objIRateBurst.getIRateTemplate()
  templateBurst.IRateDistribution[:,1] /= np.mean(templateBurst.IRateDistribution[:,1])
  templateBurst.IRateDistribution[:,1] *= 300.0
  templateBurst.IRateDistribution[:,0] /= 8
  
  SpikeTimes = load('/home/francesco/Downloads/ASTGeneration_Main/MFdata/37/05252011_mice_630_chan_2_1220_PC_chan_3_575_MF_with_B_W_3_MF.txt')
  objIRateBaseline = sgb.IRate.IRate(SpikeTimes, 0.003, TimeUnitIn='tenth_of_ms')

  Reg = objIRateBaseline.getSpikeTrainStats()['Processed']['Regularity']
  templateBaseline = objIRateBaseline.getIRateTemplate()
  templateBaseline.IRateDistribution[:,1] /= np.mean(templateBaseline.IRateDistribution[:,1])
  templateBaseline.IRateDistribution[:,1] *= 7.5
  
  import matplotlib.pyplot as plt
  #plt.plot(syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,0],syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,1])

  for i in range(1):
    
    syntheticSpikeTrainBurst = []
    for i in range(10):
      syntheticSpikeTrainBurst.append(sgb._GenerateSpikeTrain(0.5, templateBurst, 0.0001))
      syntheticSpikeTrainBurst[i].SpikeTime += (i+1)*5.0+(np.random.random()*2.5-1.25)

    syntheticSpikeTrain = sgb._GenerateSpikeTrain(Reg, templateBaseline, 0.003)
    for i in range(0,6):
      syntheticSpikeTrain = sgb.MergeSpikeTrains(syntheticSpikeTrain, syntheticSpikeTrainBurst[i])


    
  
    #plt.eventplot(syntheticSpikeTrain.SpikeTime, lineoffsets=i, linewidth=0.2)
    print (i)
    isi = syntheticSpikeTrain.SpikeTime[1:]-syntheticSpikeTrain.SpikeTime[:-1]
    tmpCounts, tmpEdges = np.histogram(isi, bins=160, range = (0,2))
    tmpCounts = tmpCounts / np.sum(tmpCounts)
    #plt.plot(tmpEdges[:-1], tmpCounts)
    x=isi[:-1]
    y=isi[1:]
    tmpCounts, tmpEdges = np.histogram(syntheticSpikeTrain.SpikeTime, bins=160, range = (0.0,40.0))
    c=np.correlate(tmpCounts, tmpCounts,mode='same'); c =c/ np.sum(c)
    plt.plot(c)
    #plt.scatter(x,y)
    tmpCounts, tmpEdges = np.histogram(sgb.GenerateSpikeTrain(objIRateBaseline).SpikeTime, bins=160, range = (0.0,40.0))
    c=np.correlate(tmpCounts, tmpCounts, mode='same'); c =c/ np.sum(c)

    syntheticSpikeTrain_1 = sgb._GenerateSpikeTrain(Reg, templateBaseline, 0.003)
    isi = syntheticSpikeTrain_1.SpikeTime[1:]-syntheticSpikeTrain_1.SpikeTime[:-1]
    tmpCounts, tmpEdges = np.histogram(isi, bins=160, range = (0,2))
    tmpCounts = tmpCounts / np.sum(tmpCounts)
    #plt.plot(tmpEdges[:-1], tmpCounts,color='red')
    plt.plot(c,color='red')
    
    
    #plt.plot(syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,0],syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,1] )
    
  plt.show()
