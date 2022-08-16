from __future__ import division
from cmath import pi
import random
import math
import csv

def Pdist(i,j):                                                                                 #Find distance between two points in a PBC setup
    dx=x[i]-x[j]
    dy=y[i]-y[j]
    return ((dx-round(dx))**2 + (dy-round(dy))**2)**.5
def Pvector(i,o):                                                                               #Find displacement between two points in a PBC setup
    dx=x[i]-o[0]
    dy=y[i]-o[1]
    return [dx-round(dx), dy-round(dy)]

def clstrChange(a,b):                                                                           #Merge clusters by updating all tries in them
    global cn
    cn-=1
    clstrPop[b]+=clstrPop[a]
    clstrPop[a]=0
    for k in range(0,n):
        if(clstr[k]==a):
            clstr[k]=b
            vector[k]=Pvector(k,origin[b])

file = open("result.txt", "w")
n=4000                                                                                          #Set the maximum value of circles to try
results=[[0]*12 for i in range(n)]
q = 0
span = True
trueno = []
microDensityList = []
falsno = 0
runno = 0
while runno <= 11:                                                                                  #Run the calculation multiple times
    m = .01                                                                                         #Set the mean radius value
    rv = .001                                                                                        #Set the radius variance
    x, y, R, clstr, clstrPop = [0]*n, [0]*n, [0]*n, [0]*n, [0]*(n+1)
    cn, new, = 0, 1
    origin = [[0]*2 for i in range(n+1)]
    vector = [[0]*2 for i in range(n)]
    span=False
    microDensity = 0
    for i in range(0,n):                                                                           #Add circles until they span or reach the maximum value 
        x[i]=random.random()
        y[i]=random.random()
        R[i]=random.lognormvariate(math.log(m/(1+rv)),(math.log(1+rv))**.5)                         #Pick the radius of the new circle from a Lognormal distribution
        microDensity += pi * (R[i] ** 2) 
        clstr[i]=new
        clstrPop[new]+=1
        vector[i] = [0,0]
        origin[new] = [x[i],y[i]]                                                                   #Remember the origin of each cluster
        cn, new = cn+1, new+1
        for j in range(0,i):
            if(Pdist(i,j) < R[i]+R[j]):                                                                #If it is connected to any existing circles
                if(clstr[j]>clstr[i]):                                                                  #Add it to that cluster       
                    clstrChange(clstr[j],clstr[i])                                                  #If it also connects to other clusetrs
                if(clstr[i]>clstr[j]):                                                              #Merge those clusters
                    clstrChange(clstr[i],clstr[j])
                else:
                    if([vector[i][0]-vector[j][0],vector[i][1]-vector[j][1]]!=Pvector(i,[x[j],y[j]])):      #If the connection wraps around the space
                       span=True                                                                            #We have reached a span
        results[i][3*q]=i+1
        results[i][3*q+1]=cn/n
        results[i][3*q+2]=max(clstrPop)/n
    
        if(span==True):                                                                           #If the span has been achieved
            trueno.append(i)                                                                      #remember the number of circles it took
            microDensityList.append(microDensity)                                                 #and the microdensity
            break                                                                                 #and finish this run
    runno+=1
    tot = 0
    for i in trueno:
        tot += i
        ave = tot/len(trueno)                                                                  #Calculate the avarage number of circles needed for the span
    tot = 0
    for i in microDensityList:
        tot += i
        microdenAve = tot/len(microDensityList)                                                #Calculate the avarage microDensity needed for the span
    print(ave)
    print(microdenAve)
writer = csv.writer(file, delimiter='\t')
writer.writerows(results)
file.close()
print("Done.")
