import sys
import matplotlib.pyplot as plt

versions = [0, 1 ,2 ,3]
#speeds = [10, 40, 70, 100, 150, 200, 250, 300]
speeds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]
repeat = [1, 2, 3, 4, 5]
send = 791615

Data={}
for v in versions:
    for s in speeds:
        l = []
        for rep in repeat:
            name = "/Users/mpastyl/snort_GPU_plots/logs_from_snort/result_proper_"+str(v)+"_"+str(s)+"_"+str(rep)+".txt"
            switch=1
            with open(name,'rb') as log:
                for row in log:
                    #if " received" in row:
                    #    x = int(row.split(':')[1])
                    if (" analyzed" in row):
                        x = int(row.split(':')[1])
                    #if (" outstanding" in row):
                    #    x = int(row.split(':')[1])
                    #if (" rx_bytes" in row):
                    #    x = int(row.split(':')[1])
            l.append(x)
        l = sorted(l)
        median = l[2] 
        median = 100* float(median) / float(send)
        #median = 100*(float(send) - float(median))/float(send)
        if Data.has_key(str(v)):
            Data[str(v)].append(median)
        else:
            Data[str(v)] = [median]

plt.plot(speeds,Data['0'], label='CPU')
plt.plot(speeds,Data['1'], label='GPU single')
plt.plot(speeds,Data['2'], label='GPU double')
plt.plot(speeds,Data['3'], label='CPU original')
plt.legend()
plt.xlabel("Traffic speed (Mbps)")
plt.ylabel("Reception rate (%)")
#plt.ylabel( "Analyzed packets")
plt.show()


