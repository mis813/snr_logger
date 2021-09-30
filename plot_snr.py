from os import name
from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.function_base import append
from datetime import datetime





def read_downsnr(lin):
    down = lin[lin.find(";")+1:lin.find(">")]
    return down




def read_upsnr(lin):
    up = lin[lin.find(">")+1:lin.find(">")+5]
    return up




def read_time(lin,tim):
    timbool = 0
    l = lin.find(":")
    h = float(lin[:l])
    m = float(lin[l+1:l+3])
    s = float(lin[l+4:l+6])
    time = h+(m/60)+(s/3600)
    
    for i in tim:
        if lin[:l+3] == i:
            timbool = 1
    return [time,timbool]






def plot_snr(down,up,tim,doave,upave,timave,updis,dodis,timdis,name):
    

    now = datetime.now().strftime("%H_%M")
    plt.clf()
    plt.title("SNR Margin "+ name)
    plt.xlabel("Time")
    plt.ylabel("SNR Margin in dB")
    plt.plot(tim,up,c = "blue",label = "UpStream")
    plt.plot(tim,down,c="r",label = "DownStream")
    plt.plot(timave,doave,c = 'black',label = "DownStream_Average")
    plt.plot(timave,upave,c = 'orange',label = "UpStream_Average")
    plt.plot(timdis,updis,'o',c = 'Yellow')
    plt.plot(timdis,dodis,'o',c = 'Yellow')
    plt.legend(loc='lower left')
    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    fig.canvas.manager.set_window_title('SNR Margin')
    plt.subplots_adjust(0.048,0.064,0.979,0.957)
    plt.grid()
    name = "plot_"+name+"_"+now+".png"
    
    
    #plt.xlim([-1.17,25.2])
    #plt.ylim([5,33])
    #plt.savefig(name,dpi = 720)
    plt.show()
    




def read_data(name,dis):
    up = []
    down = []
    time = []
    updis = []
    dodis = []
    timdis=[]
    name = "telnet_"+name+".txt"
    f = open(name,'r')
    l = 1
    for line in f:
        l= l + 1
       
        
        
        if line.find("<") == -1 or line.find(">") == -1 or line.find("%") == -1  :
            #print("dis pointed = "+str(l))
            continue
        upst = float(read_upsnr(line))
        up.append(upst)
        dost = float(read_downsnr(line))
        down.append(dost)
        [tim,booltim] = read_time(line,dis)
        time.append(tim)
        if booltim == 1:
            updis.append(upst)
            dodis.append(dost)
            timdis.append(tim) 
        
        

    
    f.close

    return [down,up,time,updis,dodis,timdis]



def plt_ave(down,up,tim):
    step = 10
    doave = []
    upave = []
    timave = []
    doave.append(down[0])
    upave.append(up[0])
    timave.append(tim[0])
    for i in range(step,len(tim),step):
        doave.append(np.average(down[i-step:i]))
        upave.append(np.average(up[i-step:i]))
        timave.append(tim[i])
    doave.append(down[len(down)-1])
    upave.append(up[len(up)-1])
    timave.append(tim[len(tim)-1])
    return [doave,upave,timave]





def disc_finder(name):
    disc = []
    name = "Log_"+name+".txt"
    f = open(name,'r')

    for i in f:
        
        line = i
        
        if line.find("<") == -1 or line.find(">") == -1 or line.find("%") == -1 :
            
            h = line.find(";")
            if h == -1:
                continue
            elif h != -1:
                # line.find(":",)
                disc.append(line[:h-3])
    
    return disc




#name = ["2021_08_29","2021_08_28","2021_08_27","2021_08_26","2021_08_25","2021_08_24","2021_08_23"]
name = ["2021_08_29"]
for i in name:

    disc = disc_finder(i)

    [down,up,time,updis,dodis,timdis] = read_data(i,disc)

    [doave,upave,timave] = plt_ave(down,up,time)


    plot_snr(down,up,time,doave,upave,timave,updis,dodis,timdis,i)