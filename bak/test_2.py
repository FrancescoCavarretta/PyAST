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



  #SpikeTimes = load('example/wichmann_data.txt')*0.001
  SpikeTimes = np.arange(0.0, 0.2, 0.005)
  objIRateBurst = sgb.IRate.IRate(SpikeTimes, 0.0001)
  templateBurst  = objIRateBurst.getIRateTemplate()
  templateBurst.IRateDistribution[:,1] /= np.mean(templateBurst.IRateDistribution[:,1])
  templateBurst.IRateDistribution[:,1] *= 200.0
  #templateBurst.IRateDistribution[:,0] /= 8
  
  SpikeTimes = load('/home/francesco/Downloads/ASTGeneration_Main/MFdata/37/05252011_mice_630_chan_2_1220_PC_chan_3_575_MF_with_B_W_3_MF.txt')
  #SpikeTimes = np.arange(0.0, 100.0, 0.2)
  objIRateBaseline = sgb.IRate.IRate(SpikeTimes, 0.003, TimeUnitIn='tenth_of_ms')

  Reg = objIRateBaseline.getSpikeTrainStats()['Processed']['Regularity']
  templateBaseline = objIRateBaseline.getIRateTemplate()
  templateBaseline.IRateDistribution[:,1] /= np.mean(templateBaseline.IRateDistribution[:,1])
  templateBaseline.IRateDistribution[:,1] *= 5.0
  
  import matplotlib.pyplot as plt
  #plt.plot(templateBaseline.IRateDistribution[:,0],templateBaseline.IRateDistribution[:,1])
  #plt.show()
  #plt.plot(syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,0],syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,1])

  for i in range(1):
    
    syntheticSpikeTrainBurst = []
    for i in range(40):
      syntheticSpikeTrainBurst.append(sgb._GenerateSpikeTrain(0.5, templateBurst, 0.0001)) #, MaxFRate=400.0, MinFRate=200.0))
      syntheticSpikeTrainBurst[i].SpikeTime += (i+1)*1.0+(np.random.random()*1.0-0.5)

    syntheticSpikeTrain = sgb._GenerateSpikeTrain(Reg, templateBaseline, 0.003) #, MaxFRate=15.0, MinFRate=5.0)
    plt.eventplot(syntheticSpikeTrain.SpikeTime, lineoffsets=1, linewidth=0.2, linelengths=0.75)
    
    for i in range(40):
      syntheticSpikeTrain = sgb.MergeSpikeTrains(syntheticSpikeTrain, syntheticSpikeTrainBurst[i])


    
  
    plt.eventplot(syntheticSpikeTrain.SpikeTime, lineoffsets=2, linewidth=0.2, linelengths=0.75)

    plt.show()

    
    #print (i)
    isi = syntheticSpikeTrain.SpikeTime[1:]-syntheticSpikeTrain.SpikeTime[:-1]
    tmpCounts, tmpEdges = np.histogram(isi, bins=200, range = (0,2))
    #tmpCounts = tmpCounts / np.sum(tmpCounts)
    plt.plot(tmpEdges[:-1], tmpCounts)

    syntheticSpikeTrain_1 = sgb._GenerateSpikeTrain(Reg, templateBaseline, 0.003)
    isi = syntheticSpikeTrain_1.SpikeTime[1:]-syntheticSpikeTrain_1.SpikeTime[:-1]
    tmpCounts, tmpEdges = np.histogram(isi, bins=160, range = (0,2))
    plt.plot(tmpEdges[:-1], tmpCounts, color='red')
    plt.xlim([0, 0.5])
    plt.ylim([0,100])
    plt.show()
    

    
    tmpCounts, tmpEdges = np.histogram(syntheticSpikeTrain.SpikeTime, bins=200, range = (0.0,40.0))
    c=np.correlate(tmpCounts, tmpCounts,mode='same'); c =c/ np.sum(c)
    plt.plot(np.arange(-len(c)/2, len(c)/2, 1)*(40.0/200.0), c)

    tmpCounts, tmpEdges = np.histogram(syntheticSpikeTrain_1.SpikeTime, bins=200, range = (0.0,40.0))
    c=np.correlate(tmpCounts, tmpCounts,mode='same'); c =c/ np.sum(c)
    plt.plot(np.arange(-len(c)/2, len(c)/2, 1)*(40.0/200.0), c, color='red')
    plt.show()
    
    isi = syntheticSpikeTrain.SpikeTime[1:]-syntheticSpikeTrain.SpikeTime[:-1]
    x=isi[:-1]
    y=isi[1:]
    plt.scatter(x,y)
    #plt.scatter(x,y)
    tmpCounts, tmpEdges = np.histogram(sgb.GenerateSpikeTrain(objIRateBaseline).SpikeTime*1000, bins=400, range = (0.0,40.0))
    c=np.correlate(tmpCounts, tmpCounts, mode='same'); c =c/ np.sum(c)


    isi = syntheticSpikeTrain_1.SpikeTime[1:]-syntheticSpikeTrain_1.SpikeTime[:-1]
    x=isi[:-1]
    y=isi[1:]
    plt.scatter(x,y,color='red')
    #tmpCounts, tmpEdges = np.histogram(isi, bins=160, range = (0,2))
    #tmpCounts = tmpCounts / np.sum(tmpCounts)
    #plt.plot(tmpEdges[:-1], tmpCounts,color='red')
    #plt.plot(np.arange(-len(c)/2, len(c)/2, 1)*(40.0/400.0), c,color='red')
    #plt.xlim([-30,30])
    
    #plt.plot(syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,0],syntheticSpikeTrain.getIRateTemplate().IRateDistribution[:,1] )
    
  plt.show()
