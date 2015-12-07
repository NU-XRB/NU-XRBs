FOLDER='/home/chase/MESA/pyscripts/'
from scipy.interpolate import interp1d
import sys
sys.path.append(FOLDER)
import helper as h
import Uconstraints as cstr
from pylab import *

###########load P bounds#############
RLzams=load(FOLDER+'RLzams.npy')
RLterminal=load(FOLDER+'RLterminal.npy')
RLmrange=load(FOLDER+'RLmrange.npy')
#################################
############## set grid size###########
dM=0.20
dP=0.1
dBeta=0.1
Mbhmin,Mbhmax = 2.0,cstr.Mbh[0]+cstr.Mbh[1]
Mdonmin,Mdonmax=1.6,15.0#cstr.Mdon[0]-cstr.Mdon[1],15.0
Permin,Permax = 0.1,12.0
Bmin,Bmax=0.0,0.9
nMbh=((Mbhmax-Mbhmin)/dM)+1.0
nMdon=((Mdonmax-Mdonmin)/dM)+1.0
nP=((Permax-Permin)/dP)+1.0
nB=((Bmax-Bmin)/dBeta)+1.0
#############################
#########create block#############

Beta=linspace(Bmin,Bmax,nB)
Mbh0=linspace(Mbhmin,Mbhmax,nMbh)
Mdon0=linspace(Mdonmin,Mdonmax,nMdon)
P0=linspace(Permin,Permax,nP)
#############################
Fails={'Failed Spin Test':[],'Failed >P Test':[],'Failed Main Sequence Test':[],'Failed Mass Ratio Test':[],'Failed Pcurr Test':[]}
obs_mbh = linspace(cstr.Mbh[0]-cstr.Mbh[1],cstr.Mbh[0]+cstr.Mbh[1],1000)
obs_mdonlims=h.getMdonRange(obs_mbh)
GRID=[]
npoints=0
for beta in Beta:
      print beta
      B=[]
      for key in Fails.keys():
            Fails[key].append([])
      
      for mbh0 in Mbh0:
            MBH=[]
            Pmin=h.getP_RL(mbh0,RLmrange,RLzams)
            Pmax=h.getP_RL(mbh0,RLmrange,RLterminal)
            Pmax_i=interp1d(RLmrange,Pmax)
            Pmin_i=interp1d(RLmrange,Pmin)
            for key in Fails.keys():
                  Fails[key][-1].append([])
                  
            if h.getKerr_Param(mbh0,cstr.Mbh[0]-cstr.Mbh[1])<=cstr.aKerr[0]+cstr.aKerr[1]:       #Spin Test
                  for mdon0 in Mdon0:
                        MDON=[]
                        obs_mdon=(-obs_mbh+((1.0-beta)*mdon0)+mbh0)/(1.0-beta)  #Find Predicted range of don masses @ target Mbh range given mdon0,mbh0,and beta
                        
                        #Is a portion of this range in within the constraints? Find that portion
                        AtObs=transpose([[obs_mbh[i],obs_mdon[i]] for i in range(len(obs_mdon)) if (obs_mdon[i]>=obs_mdonlims[0][i] and obs_mdon[i]<=obs_mdonlims[1][i])])
                        
                        
                        
                        if len(AtObs)>0:                                                                                #Ratio Test
                              BhAtObs=AtObs[0]
                              DonAtObs=AtObs[1]
                              for p0 in P0:
                                    if p0>Pmin_i(mdon0) and p0<Pmax_i(mdon0):       #Main Sequence Test
                                          if not (mbh0>mdon0 and p0>cstr.P[0]-cstr.P[1]):   #p>p0 Test
                                                PAtObs=[h.Pcurr(mdon0,BhAtObs[i],DonAtObs[i],p0,beta) for i in range(len(DonAtObs))]
                                                Lesstf = [p<=cstr.P[0]+cstr.P[1] for p in PAtObs]
                                                Moretf=[p>=cstr.P[0]-cstr.P[1] for p in PAtObs]

                                                if (any(Lesstf) and any(Moretf)):                 #Pcurr Test
                                                      MDON.append([beta,mbh0,mdon0,p0])
                                                      npoints=npoints+1
                                                      
                                                else:Fails['Failed Pcurr Test'][-1][-1].append([beta,mbh0,mdon0,p0]) #End Pcurr Test

                                                
                                          else:Fails['Failed >P Test'][-1][-1].append([beta,mbh0,mdon0,p0])  #End p>p0 Test

                                    else:Fails['Failed Main Sequence Test'][-1][-1].append([beta,mbh0,mdon0,p0]) #End Main Sequence Test
                                    
                                    

                        else: Fails['Failed Mass Ratio Test'][-1][-1].extend([[beta,mbh0,mdon0,P] for P in P0])#End Ratio Test
                        
                        MBH.append(MDON)

                  
            else: Fails['Failed Spin Test'][-1][-1].extend([[beta,mbh0,M,P] for M in Mdon0 for P in P0]) #End Spin test
            B.append(MBH)
      GRID.append(B)
save(FOLDER+'Grid',GRID)
for key in Fails.keys():
      print key
      save(FOLDER+key,Fails[key])

                                                           
            
