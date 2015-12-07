SCRIPTS=
import os
import shutil
import sys
sys.path.append(SCRIPTS)
from helper import *


defaultBinDon = os.path.join(SCRIPTS,'Templates','defaultBinDon')
def addControls(inlist,newlines):
      if type(newlines)==str:
            newlines=[newlines]
      with open(inlist,'r') as old: oldlines=old.readlines()
      old.closed
      
      endsection=[line for line in oldlines if 'controls namelist' in line]
      if not len(endsection)==1: print 'can\'t find end'
      endControl = oldlines.index(endsection[0])
      
      for line in newlines:
            oldlines.insert(endControl,'   '+line+'\n')
            endControl=endControl+1

      with open(inlist,'r+') as new:
            new.seek(0)
            for line in oldlines:
                  
                  new.write(line)
            
            new.truncate()
      new.closed
      
def addJobs(inlist,newlines):
      if type(newlines)==str:
            newlines=[newlines]
      with open(inlist,'r') as old: oldlines=old.readlines()
      old.closed
      
      endsection=[line for line in oldlines if 'job namelist' in line]
      if not len(endsection)==1: print 'can\'t find end'
      endJobs= oldlines.index(endsection[0])
      
      for line in newlines:
            oldlines.insert(endJobs,'   '+line+'\n')
            endJobs=endJobs+1

      with open(inlist,'r+') as new:
            new.seek(0)
            for line in oldlines:
                  
                  new.write(line)
            
            new.truncate()
      new.closed

def newRun(params,pardir,newfolder,scheme='Ritter',max_tries=100):
	Mbh_i=params[1]
	Mdon_i=params[2]
	P_i=params[3]
	beta=params[0]
	if newfolder in os.listdir(pardir):
		print newfolder+'Already Exists in '+pardir
	
	else:
		
		newdir=os.path.join(pardir,newfolder)
		shutil.copytree(defaultBinDon,newdir)
	
	Rmax=getRL(Mbh_i,Mdon_i,P_i)
	DonorNewLines=['initial_mass = '+str(Mdon_i),'photosphere_r_upper_limit = '+str(Rmax)]
	addControls(os.path.join(newdir,'Donor/inlist_project'),DonorNewLines)
	
	BinaryProjectNewLines=['m2 = '+str(Mbh_i)+'d0','initial_period_in_days = '+str(P_i),'mdot_scheme = \''+scheme+'\'','max_tries_to_achieve = '+str(max_tries),'mass_transfer_beta = '+str(beta)]
	addControls(os.path.join(newdir,'Binary/inlist_project'),BinaryProjectNewLines)
	
	BinaryInlist1NewLines=['star_mass_min_limit=1.7']
	addControls(os.path.join(newdir,'Binary/inlist1'),BinaryInlist1NewLines)
	
	

