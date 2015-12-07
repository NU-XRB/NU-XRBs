FOLDER = '/home/chase/MESA/pyscripts'
import sys
sys.path.append(FOLDER)
from fileIO import *
import os
from numpy import *
dM=0.2
Mbhmin=2.0

topdir = '/foo/bar/TheseAreTheRuns    #Specify where to put the Beta_X folders
Grid = list(load('Grid.npy'))
nruns=0
for b in range(len(Grid)):
    newtop = os.path.join(topdir,'Beta_'+str(b))
    os.makedirs(newtop)
    for m in range(len(Grid[b])):
        
        if not (len(Grid[b][m])==0 or max([len(a) for a in Grid[b][m]])==0):
            
            BHfolder= os.path.join(newtop,'Mbh_'+str(Mbhmin+(m*dM)))
            os.makedirs(BHfolder)
            for md in range(len(Grid[b][m])):
                for datpoint in Grid[b][m][md]:
                    newRun(datpoint,BHfolder,str(datpoint[2])+'-'+str(datpoint[3]))
                    nruns=nruns+1
print nruns
        
