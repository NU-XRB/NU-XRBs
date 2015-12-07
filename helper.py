FOLDER='/projects/b1011/chasebk/pyscripts/'


import sys
sys.path.append(FOLDER)
from numpy import *
import matplotlib.pyplot as plt
import scipy.constants as con
import sys
import Uconstraints as cstr
Msun =1.98855e30 #kg
Rsun = 6.955e8 #kg
G = 6.67384e-11
Gcgs=6.67384e-8
c=299792458.0 # m/s
ccgs =  2.99792458e10
days_per_year = 365.25
seconds_per_day = 60.0*60.0*24.0
sec_yer=3.1558149984e7

def getA(M_1,M_2,t):        #in Rsuns
      M1= M_1*Msun
      M2 = M_2*Msun
      T = t*seconds_per_day
      a = (T*sqrt(G*(M1+M2))/(2*pi))**(2.0/3.0)
      return (a/Rsun)
def getP(Mbh,Mdon,A): #Days
      M_bh = Mbh*Msun
      M_don = Mdon*Msun
      a = A*Rsun
      P=2*pi*sqrt((a**3.0)/(G*(M_bh+M_don)))    
      return P/seconds_per_day  
      

def getBox(XX,YY, fill_in = False, h = '/',flag = 0,color='black'):      #For a pretty specific plotting situation.
      C=color
      if flag == 'y':  xmin =XX[0] ; xmax = XX[1]
      else:   xmin = XX[0]-XX[1] ; xmax = XX[0]+XX[1]
      if flag == 'x':  ymin = YY[0] ; ymax = YY[1]
      else: ymin = YY[0]-YY[1] ;  ymax = YY[0]+YY[1]

      X = [xmin,xmin,xmax,xmax] ; Y=[ymin,ymax,ymax,ymin]
      return plt.fill(X,Y,hatch=h,fill = fill_in,color=C)


def getMdotCrit(Mdon,Mbh,p): #See, for instance, LMX-3 paper eq (13)
      P=p/days_per_year
      Mdotcrit = (10e-5)*(Mbh**0.5)*(Mdon**-0.2)*(P**1.4)
      return Mdotcrit

def getMeddingtonH(Mbh,surf_h):  #See MESA binary_mdot.f90
      medd =4.0*pi*Gcgs*Mbh/(ccgs*0.2*(1.0+surf_h))
      return medd*sec_yer

def getRZAMS(M):      #See Tout,Pols,Eggleton 1996 eq (2)
      theta = 1.71535900
      i=6.59778800
      k = 10.08855
      l = 1.012495
      u = 0.07490166
      v = 0.01077422
      eps = 3.08223400
      o = 17.84778
      p = 0.00022582

      R=((theta*(M**(2.5)))+(i*(M**(6.5)))+(k*(M**(11.0)))+(l*(M**(19.0)))+(u*(M**(19.5))))/ \
                                                                                           (v+(eps*(M**(2.0)))+(o*(M**(8.5)))+(M**18.5)+(p*(M**(19.5))))
      return R

def getRL(Mbh,Mdon,P): #RL given P
      A=getA(Mbh,Mdon,P)
      q = Mdon/Mbh
      return A*0.49*(q**(2.0/3.0)) / ((0.6*(q**(2.0/3.0))) + log(1.0+(q**(1.0/3.0))))
def getP_RL(Mbh,Mdon,RL): #P given RL
      q=Mdon/Mbh
      A = RL*((0.6*(q**(2.0/3.0))) + log(1.0+(q**(1.0/3.0))))/(0.49*(q**(2.0/3.0)))
      
      return getP(Mbh,Mdon,A)

def getHR_R(T,L):     #Black body T-L relation
      return sqrt((1.0/(8.97e-16))*L/(T**4.0))

def getKerr_Param(Mbh0,Mbh):
      Macc=Mbh-Mbh0
      
      
      MiM = (3.0*sin((Macc/(3.0*Mbh0))+arcsin(1.0/3.0)))**-1.0
      #if 1.0/MiM > sqrt(6): print 'help' +str(Mbh0)
      a_kerr = sqrt(2.0/3.0)*MiM*(4.0-sqrt((18.0*(MiM**2.0)) - 2.0))
      return a_kerr


      
def getP_i(Mdon0,Mbh,Mdon,P,beta,alpha=0):   #Rearranged Solution to LMX-3 paper eq(5)
      if not beta==1.0:
            if any(0>Mbh+((1.0-beta)*(Mdon-Mdon0))):
                  print 'help'
                  print Mdon0/Mdon
                  print(Mbh+(1.0-beta)*(Mdon-Mdon0))
                  print Mdon0+Mbh+((1.0-beta)*(Mdon-Mdon0))
            try:     
                  R= P*pow(Mdon0/Mdon,3.0*(alpha-1.0))*pow((Mbh+((1.0-alpha)*(1.0-beta)*(Mdon-Mdon0)))/Mbh,3.0/(beta-1.0))*pow((Mdon+Mbh)/(Mdon0+Mbh+((1.0-alpha)*(1.0-beta)*(Mdon-Mdon0))),2.0)
                  
            except: print('getP_i '+str(Mdon0)+' '+str(Mbh)+ ' '+str(Mdon))
                  
            
      else:R=P*pow(Mdon0/Mdon,3.0*(alpha-1.0))*pow((Mbh+Mdon)/(Mbh+Mdon0),2.0)*exp(3.0*(alpha-1)*(Mdon-Mdon0)/Mbh)
      return R
def Pcurr(Mdon0,Mbh,Mdon,P0,beta,alpha=0):#Rearranged Solution to LMX-3 paper eq(5)
      if not beta==1.0:
            try:
                  R=P0*pow(Mdon0/Mdon,-3.0*(alpha-1.0))*pow((Mbh+((1.0-alpha)*(1.0-beta)*(Mdon-Mdon0)))/Mbh,-3.0/(beta-1.0))*pow((Mdon+Mbh)/(Mdon0+Mbh+((1.0-alpha)*(1.0-beta)*(Mdon-Mdon0))),-2.0)
            except:  print('getPcurr  '+str(Mdon0)+' '+str(Mbh)+ ' '+str(Mdon))
                  
      else:
            try:
                  R=P0*pow(Mdon0/Mdon,-3.0*(alpha-1.0))*pow((Mbh+Mdon)/(Mbh+Mdon0),-2.0)*exp(-3.0*(alpha-1)*(Mdon-Mdon0)/Mbh)
            except:print('getPcurr Beta=1  '+str(Mdon0)+' '+str(Mbh)+ ' '+str(Mdon)+' '+str(beta))
      return R


def getMdonRange(Mbh):   #Observational limits on Mdon given constraints on Mbh/Mdon
      Rmin,Rmax =cstr.Mbh_Mdon[0]-cstr.Mbh_Mdon[1],cstr.Mbh_Mdon[0]+cstr.Mbh_Mdon[1]
      return [Mbh/Rmax,Mbh/Rmin]
      
      
