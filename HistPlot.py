OUPUT=
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
from matplotlib.widgets import Slider
h=open(os.path.join(OUTPUT,'Processed_Runs.dat'))
D=pickle.load(h)
h.close()
####Create arrays to be plotted##############
COND='Win'
together=0
Mass=np.arange(0.0,14.0,.2)
BhBucket={}
DonBucket={}
BETAS=[round(0.0+(i*0.1),1) for i in range(10)]
Norm = float(len(D[COND]))
dMEANS={}
bMEANS={}
pMEANS={}


for b in BETAS:
    BhBucket[b]=[0.0 for m in Mass]
    DonBucket[b]=[0.0 for m in Mass]
 
    Bhs=[run[1] for run in D[COND] if run[0]==b]
    Dons=[run[2] for run in D[COND] if run[0]==b]
    Pers=[run[3] for run in D[COND] if run[0]==b]
    dMEANS[b]=[round(mean(Dons),2),round(np.std(Dons),2)]
    bMEANS[b]=[round(mean(Bhs),2),round(np.std(Bhs),2)]
    pMEANS[b]=[round(mean(Pers),6),round(np.std(Pers),6)]
    
    for i in range(len(Mass)):
    
        BhBucket[b][i]=sum(run[1]==round(Mass[i],2) and run[0]==b for run in D[COND])/Norm
        DonBucket[b][i]=sum(run[2]==round(Mass[i],2) and run[0]==b for run in D[COND])/Norm


#######Initialize Data#######################

dB=0.1
Beta=0.7

ax=subplot(111)
dontext=ax.text(4,max(DonBucket[Beta]),r'$\mu_{DON}$=' + str(dMEANS[Beta][0])+'  $\sigma_{DON}$='+str(dMEANS[Beta][1]) +'$M_{sun}$')
bhtext=ax.text(12,max(BhBucket[Beta]),r'$\mu_{BH}$=' + str(bMEANS[Beta][0])+'  $\sigma_{BH}$='+str(bMEANS[Beta][1]) +'$M_{sun}$')
ptext=ax.text(6,(max(DonBucket[Beta])+max(BhBucket[Beta]))/2.0,r'$\mu_{PER}$=' + str(pMEANS[Beta][0])+'  $\sigma_{PER}$='+str(pMEANS[Beta][1]) +'$days$')
xlabel('Initial Mass (Msuns)')
ylabel('Normalized ' +COND+' Count')
DonHist=ax.bar(Mass,DonBucket[Beta],.1,color='b',label='$Mdon_0$')
BhHist=ax.bar(Mass,BhBucket[Beta],.1,color='r',label='$Mbh_0$')

legend()
######Create Axes and Sliders#############
subplots_adjust(left=0.25, bottom=0.25)
axB=axes([0.25, 0.15, 0.65, 0.03])
sB=Slider(axB,r'$\beta$',0.0,0.9,valinit=Beta)
#########Update() Definition############

def update(arg):


    Beta=round(sB.val,1)
    print Beta
    
    for rect,h in zip(BhHist,BhBucket[Beta]):rect.set_height(h)
        
        
    for rect2,h2 in zip(DonHist,DonBucket[Beta]): rect2.set_height(h2)
    dontext.set_text(r'$\mu_{don}$=' + str(dMEANS[Beta][0])+'  $\sigma_{don}$='+str(dMEANS[Beta][1]) +'$M_{sun}$')
    bhtext.set_text(r'$\mu_{bh}$=' + str(bMEANS[Beta][0])+'  $\sigma_{bh}$='+str(bMEANS[Beta][1]) +'$M_{sun}$')
    ptext.set_text(r'$\mu_{PER}$=' + str(pMEANS[Beta][0])+'  $\sigma_{PER}$='+str(pMEANS[Beta][1]) +'$days$')
    draw()
sB.on_changed(update)

show()

        
