"""
@ Name: Abhishek Dhital
  ID  : 1001548204
"""

import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf


def applyShelvingFilter(inName, outName, g, fc) :
    mu=10**(g/20)
    inp=sf.read(inName)
    d=inp[0]    #original signal
    fs=inp[1]   #sampling frequency
    theta=2*np.pi*fc/fs
    gamma=(1-(4/(1+mu))*np.tan(theta/2))/(1+(4/(1+mu))*np.tan(theta/2))
    alpha=(1-gamma)/2
    y=[]
    u=[]
    i=-1
    
    for x in d:
        if(i<0):
            prevIn=0
            prevOut=0
        u=alpha*(x+prevIn)+gamma*prevOut
        out=x+(mu-1)*u
        y.append(out)
        prevIn=x
        prevOut=u
        i+=1
        
    y=np.array(y)
    d=np.array(d)

    
    figure1=plt.figure()
    fft_In=np.fft.fft(d)    #fft of original signal
    fft_Out=np.fft.fft(y)   #fft of filtered signal
    print(fft_Out)
    
    maximum=max(max(abs(fft_In)),max(abs(fft_Out)))+100  #maximum y axis size
    
    #plotting original signal fft
    plt1=figure1.add_subplot(121)
    plt1.plot(abs(fft_In))
    plt.xlim(0,fft_In.size/4)
    plt.ylim(0,maximum)
    plt.title("original signal")
    plt.xlabel("Hz")
    
    #plotting filtered signal fft
    plt2=figure1.add_subplot(122)
    plt2.plot(abs(fft_Out))
    plt.xlim(0,fft_In.size/4)
    plt.ylim(0,maximum)
    plt.title("filtered signal")
    plt.xlabel("Hz")
    
    plt.show()
    

    sf.write(outName,np.real(y),fs)
        
    


##########################  main  ##########################
if __name__ == "__main__" :
    inName = "P_9_1.wav"
    gain = -10 # can be positive or negative
                # WARNING: small positive values can greatly amplify the sounds
    cutoff = 300
    outName = "shelvingOutput.wav"

    applyShelvingFilter(inName, outName, gain, cutoff)
