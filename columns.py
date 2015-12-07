import sys
sys.path.append('/home/chase/MESA/pyscripts/')
#Get index of variables from a header file
def getColumns(folderpath):
      
      f= open(folderpath)
      the_line=f.readlines()[5]
      f.close()
      
      columns = the_line.strip('\n').split(' ')
      v = [col for col in columns if not len(col) == 0]
      global logSys_Mdot_2,Mdon,Mbh,logTeff,logL,\
             RLdon,RLbh,P,A,logMdot_don,logMdot_bh,\
             bin_age,logR, surf_opacity,surf_h,logSys_Mdot_1,\
             logSys_Mdot_2, Jdot, jdot_mb, jdot_gr, jdot_ml, jdot_ls,logg
      Mdon = v.index('star_1_mass')
      Mbh = v.index('star_2_mass')
      logg = v.index('log_g')
      logTeff = v.index('log_Teff')
      logL = v.index('log_L')
      RLdon = v.index('rl_1')
      RLbh = v.index('rl_2')
      P = v.index('period_days')
      A = v.index('binary_separation')
      logMdot_don = v.index('lg_mstar_dot_1')
      logMdot_bh = v.index('lg_mstar_dot_2')
      #bin_age = v.index('age')
      #logR = v.index('log_R')
      #surf_opacity = v.index('surf_avg_opacity')
      surf_h = v.index('surface_h1')
      #logSys_Mdot_1=v.index('lg_system_mdot_1')
      # logSys_Mdot_2=v.index('lg_system_mdot_2')
      #Jdot = v.index('Jdot')
      #jdot_mb = v.index('jdot_mb')
      #jdot_gr = v.index('jdot_gr')
      #jdot_ml = v.index('jdot_ml')
      #jdot_ls = v.index('jdot_ls')
def getColumnsRL(folderpath):
	f=open(folderpath)
	the_line=f.readlines()[5]
	f.close()
	columns = the_line.strip('\n').split(' ')
      	v = [col for col in columns if not len(col) == 0]
	global logR
	logR=v.index('log_R')
      
      



