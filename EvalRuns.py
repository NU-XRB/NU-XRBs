from config import paths
import pickle
import helper as h
import Uconstraints as cstr
from numpy import *
import columns as v
import os
pth=os.path.join
from scipy.interpolate import interp1d
RUNS,OUTPUT,BINHIST=paths['RunData'],paths['Output'],paths['History']
v.getColumns(paths['Headers'])
Betas=['Beta_'+str(i) +'Finished' for i in range(10)]
Tmin=cstr.Teff[0]-cstr.Teff[1]
Tmax=cstr.Teff[0]+cstr.Teff[1]
gmin = cstr.g[0]-cstr.g[1]
gmax = cstr.g[0]+cstr.g[1]
Mbhmin=cstr.Mbh[0]-cstr.Mbh[1]
Mbhmax = cstr.Mbh[0]+cstr.Mbh[1]
spinmax=cstr.aKerr[0]+cstr.aKerr[1]
Results=['Spin Fail','Mbh Fail','Mdon Fail','Teff Fail','g Fail','Mdot Fail','Win','P Fail','DNF']
FailFile=pth(OUTPUT,'AllBinFails.dat')
GoodFile=pth(OUTPUT,'AllGoodRuns.dat')
def checkWins(runpath):
	edd=0
	if not BINHIST in os.listdir(pth(runpath)):
		return [['DNF'],[]]
	
	rundata=loadtxt(pth(runpath,BINHIST))
	atPCross=[]
	for k in range(len(rundata)):
		
		
		edd=max(10.0**rundata[k][v.logMdot_bh]/h.getMeddingtonH(rundata[k][v.Mbh],rundata[k][v.surf_h]),edd)
			
		if rundata[k][v.P]>cstr.P[0]-cstr.P[1] and rundata[k][v.P]<cstr.P[0]+cstr.P[1]:
			atPCross.append(rundata[k])
		elif k>0 and rundata[k-1][v.P]<cstr.P[0]-cstr.P[1] and rundata[k][v.P]>cstr.P[0]-cstr.P[1]:
			atPCross.append(rundata[k-1])
			atPCross.append(rundata[k])
		elif k>0 and rundata[k-1][v.P]<cstr.P[0]+cstr.P[1] and rundata[k][v.P]>cstr.P[0]+cstr.P[1]:
			atPCross.append(rundata[k])
	if len(atPCross)==0:
		return [['P Fail'],array(transpose(rundata))]
   
	intervars=[[] for i in range(len(rundata[0]))]
	varlist=[v.logTeff,v.logg,v.Mbh,v.Mdon,v.logMdot_bh]
	per=[point[v.P] for point in atPCross]


	
	for i in varlist:
		
		val=[point[i] for point in atPCross]
	    
     
		intervars[i]=interp1d(per,val)
	
	P=linspace(max(cstr.P[0]-cstr.P[1],per[0]),cstr.P[0]+cstr.P[1],num=100,endpoint=True)
	Labels=[]
	Mbh_at_Plist=[]
	Mdon_at_Plist=[]
	for p in P:
		pscore=[]
		Mbh_at_Plist.append(intervars[v.Mbh](p))
		Mdon_at_Plist.append(intervars[v.Mdon](p))
		if h.getKerr_Param(rundata[0][v.Mbh],intervars[v.Mbh](p))<spinmax:pass
		else:pscore.append('Spin Fail')
		if intervars[v.Mbh](p)>Mbhmin and intervars[v.Mbh](p)<Mbhmax:pass
		else:pscore.append('Mbh Fail')
		MdonRange=h.getMdonRange(intervars[v.Mbh](p))
		if intervars[v.Mdon](p)>MdonRange[0] and intervars[v.Mdon](p)<MdonRange[1]:pass
		else:pscore.append('Mdon Fail')
		if pow(10.0,intervars[v.logTeff](p))>Tmin and pow(10.0,intervars[v.logTeff](p))<Tmax:pass
		else:pscore.append('Teff Fail')
		if pow(10.0,intervars[v.logg](p))>gmin and pow(10.0,intervars[v.logg](p))<gmax:pass
		else:pscore.append('g Fail')
		if pow(10.0,intervars[v.logMdot_bh](p))<h.getMdotCrit(intervars[v.Mdon](p),intervars[v.Mbh](p),p):pass
		else:pscore.append('Mdot Fail')
		if len(pscore)==0:
			Labels=['Win']
			
			break
		elif len(pscore)>len(Labels):Labels=pscore
	print edd                            
	return [Labels,array(transpose(rundata)),mean(Mbh_at_Plist),mean(Mdon_at_Plist),edd]
			
		
		
T={}
Hists={}
MDON_P={'Win':[],'All':[]}
MBH_P={'Win':[],'All':[]}
EDD=[]
for result in Results:
	T[result]=[]
	Hists[result]={}


n=0
for betafolder in Betas:
	beta=betafolder.strip('Beta_')
	beta=float(beta.strip('Finished'))/10.0
	print "Beta = " + str(beta)
	
	for bhfolder in os.listdir(pth(RUNS,betafolder)):
		if not 'Mbh' in bhfolder:
			if bhfolder =='BinFails.dat':
				dummyfile=open(pth(RUNS,betafolder,bhfolder),'r')
				lines=dummyfile.readlines()
				dummyfile.close()
				g=open(FailFile,'a+')
				g.write(betafolder+'\n')
				for line in lines:g.write(line)
				g.close()
				continue
			elif bhfolder =='GoodRuns.dat':
				dummyfile=open(pth(RUNS,betafolder,bhfolder),'r')
				lines=dummyfile.readlines()
				dummyfile.close()
				g=open(GoodFile,'a+')
				g.write(betafolder+'\n\n')
				for line in lines:g.write(line)
				g.close()
				continue
			else:continue
				
				
		Mbh=float(bhfolder.strip('Mbh_'))
		
		for runfolder in os.listdir(pth(RUNS,betafolder,bhfolder)):
			
			print n
			n+=1
			run=[beta,Mbh]
			run.extend([float(num) for num in runfolder.rsplit('-')])
			outcome=checkWins(pth(RUNS,betafolder,bhfolder,runfolder))
			for label in outcome[0]:
		  	
				T[label].append(run)
				Hists[label][str(run)]=outcome[1]
				if label=='Win':
					
					MBH_P[label].append(outcome[2])
					MDON_P[label].append(outcome[3])
					
			try:
				MBH_P['All'].append(outcome[2])
				MDON_P['All'].append(outcome[3])
				EDD.append(outcome[4])
			except:pass
			
				


	
with open(pth(OUTPUT,'Processed_Runs.dat'),'wb') as outfile:
	pickle.dump(T,outfile,protocol=pickle.HIGHEST_PROTOCOL)
outfile.close()
with open(pth(OUTPUT,'Processed_Hists.dat'),'wb') as outfile1:
	pickle.dump(Hists,outfile1,protocol=pickle.HIGHEST_PROTOCOL)
outfile1.close()
with open(pth(OUTPUT,'MBHS_P.dat'),'wb') as outfile2:
	pickle.dump(MBH_P,outfile2,protocol=pickle.HIGHEST_PROTOCOL)
outfile2.close()
with open(pth(OUTPUT,'MDONS_P.dat'),'wb') as outfile3:
	pickle.dump(MDON_P,outfile3,protocol=pickle.HIGHEST_PROTOCOL)
outfile3.close()
with open(pth(OUTPUT,'EDDS.dat'),'wb') as outfile4:
	pickle.dump(EDD,outfile4,protocol=pickle.HIGHEST_PROTOCOL)
outfile4.close()
