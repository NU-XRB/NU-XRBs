import sys
import os
import shutil
import config.paths as paths
scriptfolder=paths['SCRIPTS']    #Change
FOLDER=os.path.join(paths['RunData'],'Beta_4')    #These Lines
os.system('cp '+os.path.join(scriptfolder,'history_columns.list')+ ' $MESA_DIR/star/defaults/')
os.system('cp '+os.path.join(scriptfolder,'binary_history_columns.list')+ ' $MESA_DIR/binary/defaults/')
DonFail = os.path.join(FOLDER,'DonFails.dat')
BinFail = os.path.join(FOLDER,'BinFails.dat')
GoodRuns=os.path.join(FOLDER,'GoodRuns.dat')
for bhfolder in os.listdir(FOLDER):
      try:i=bhfolder.index('_')
      except:continue
      Mbh = bhfolder[i+1:]
      bhpath = os.path.join(FOLDER,bhfolder)
      os.chdir(bhpath)
      for run in os.listdir(bhpath):
            flag=0
            try:os.chdir(os.path.join(bhpath,run,'Donor'))
	    except:continue
            os.system('./mk > 2D1log 2>&1')
            os.system('./rn > 2Dlog 2>&1')
            with open('2Dlog') as f:
                  for line in f.readlines():
                        if 'termination code' in line:
                              if not 'photosphere_r_upper_limit' in line:
                                    h=open(DonFail,'a+')
                                    h.write(Mbh+'-'+run+':  '+line+'\n')
                                    h.close()
                                    
                                    break
                              break
            f.close()


            try:
                  shutil.copy(os.path.join(bhpath,run,'Donor/RLO.mod'),os.path.join(bhpath,run,'Binary'))
                  shutil.copy(os.path.join(bhpath,run,'Donor/LOGS/history.data'),os.path.join(bhpath,run,'DonHist.data'))
                  shutil.copy(os.path.join(bhpath,run,'Donor/LOGS/headers.data'),os.path.join(bhpath,run,'DonHeaders.data'))
            except: continue
            shutil.rmtree(os.path.join(bhpath,run,'Donor'))
            

            
            os.chdir(os.path.join(bhpath,run,'Binary'))
                        
            os.system('./mk > 2B1log 2>&1')
            os.system('./rn > 2Blog 2>&1')
            
            with open('2Blog') as f:
                  for line in f.readlines():
                        if 'termination code' in line:
                              if 'star_mass_min_limit' in line:
                                    h=open(GoodRuns,'a+')
                                    h.write(Mbh+'-'+run+'\n')
                                    h.close()
                                    shutil.copy(os.path.join(bhpath,run,'Binary/LOGS1/history.data'),os.path.join(bhpath,run,'BinHist.data'))
                                    
                                    break
                              else:
                                    h=open(BinFail,'a+')
                                    h.write(Mbh+'-'+run+': '+line+'\n')
                                    h.close()
                                    
                                    break
            f.close()
            shutil.rmtree(os.path.join(bhpath,run,'Binary'))
            
                  
                  
                  
            
                  
                  
            
            
            
                                    
                              
                              
            
            
      



