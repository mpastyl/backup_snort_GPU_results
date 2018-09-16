import sys
import matplotlib.pyplot as plt
import subprocess

versions = [3, 0, 1 ,2]
speeds=[10, 20, 30, 40, 50, 60, 70, 75, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 300, 350, 400, 450, 500, 550, 600]
repeat = [1, 2, 3, 4, 5]
send = 1000000

colors = ['lightsalmon','skyblue','steelblue','mediumseagreen','lightgreen','0.30','0.70','m']
hatches = ['/','\\\\','x','\\','//']

Data={}
for v in versions:
    for s in speeds:
        l = []
        for rep in repeat:
            #name = "/Users/mpastyl/snort_GPU_plots/logs_from_snort/result_proper_big_dataset_proper_config_"+str(v)+"_"+str(s)+"_"+str(rep)+".txt"
            name = "/Users/mpastyl/snort_GPU_plots/logs_from_snort/result_proper_big_dataset_proper_config_final_"+str(v)+"_"+str(s)+"_"+str(rep)+".txt"
            switch=1
            with open(name,'rb') as log:
                for row in log:
                    if " received" in row:
                        x = int(row.split(':')[1])
                    if (" analyzed" in row):
                        y = int(row.split(':')[1])
                    #if (" outstanding" in row):
                    #    y = int(row.split(':')[1])
                    #if (" rx_bytes" in row):
                    #    x = int(row.split(':')[1])
            l.append(100*y/float(x))
            #l.append(x)
        l = sorted(l)
        median = l[2] 
        #median = 100* float(median) / float(send)
        #median = 100*(float(send) - float(median))/float(send)
        if Data.has_key(str(v)):
            Data[str(v)].append(median)
        else:
            Data[str(v)] = [median]

FIG_SIZE=(7,3.5)
fig , ax = plt.subplots(1,1,figsize=FIG_SIZE)

ax.plot(speeds,Data['3'], label='Snort original',marker='.',markersize=3,color=colors[0])
ax.plot(speeds,Data['0'], label='Snort modified (CPU)',marker='v',markersize=3,color=colors[1])
ax.plot(speeds,Data['1'], label='CLort single buffer (GPU)',marker='+',markersize=3,color=colors[2])
ax.plot(speeds,Data['2'], label='CLort double buffer (GPU)', marker='*',markersize=3,color=colors[3])
lgd = plt.legend()
ax.set_xlabel("Produced traffic rate (Mbps)")
#plt.ylabel("Reception rate (%)")
#plt.ylabel( "Analyzed packets (%)")
#plt.ylabel( "Packets analyzed by Snort, over received packets (%)")
ax.set_ylabel( "Perc. of received packets analyzed (%)")
#plt.ylabel( "Received packets (%)")

name="/Users/mpastyl/Desktop/tcpreplay.pdf"
plt.savefig(name,bbox_extra_artists=(lgd,), bbox_inches = "tight")
subprocess.Popen("pdfcrop "+name+" "+name,shell=True)
subprocess.Popen("pdfcrop")

plt.show()

m = 0
for i in range(len(Data['0'])):
    x =  Data['2'][i] - Data['0'][i]
    if x>m:
        m=x
print m
