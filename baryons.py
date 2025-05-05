import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
import scipy
import pandas as pd
import gcd_tools

#set up directories for outputs and the data
outpath=''
data_path="../../"

#create object with data
gr = gcd_tools.gcd_data(data_path)

#loop over all time dumps
#for nstep in range(84,200):
for nstep in range(len(gr.dump_steps)):
#for nstep in range(457, 501):

    gr.read_base(nstep)  #reads base data
    gr.read_extra_hydro() #read hydro data with same step as base
    gr.read_age() #read stellar age data
    gr.read_metals() # read metal data
    gr.convert_units() #convert to useful units
    #print(len(gr.particles.age))
    #print(gr.particles.age[4], gr.particles.age[15])
    #print(gr.particles.age)
    gr.particles.age=(nstep*1e7-gr.particles.age)
    #print(gr.particles.age[4], gr.particles.age[15])
    #print(gr.particles.age)
#create a big ass thing with all the data
    full_data=pd.concat([
        gr.particles.x,gr.particles.y,gr.particles.z,
	gr.particles.vx,gr.particles.vy,gr.particles.vz,
	gr.particles.mass,gr.particles.ZHe,
        gr.particles.ZC,gr.particles.ZN,gr.particles.ZO,
        gr.particles.ZNe,gr.particles.ZMg,gr.particles.ZSi,
        gr.particles.ZFe,gr.particles.ZZ,gr.particles.rho,
        gr.particles.u,gr.particles.age,gr.particles.h,
        gr.particles.divv,gr.particles.alpv,gr.particles.alpu,
        gr.particles.myu,gr.particles.dtp,gr.particles.id,
        gr.particles.itype], axis=1)
    DM_data=pd.concat([
        gr.particles.x,gr.particles.y,gr.particles.z,
        gr.particles.vx,gr.particles.vy,gr.particles.vz,
        gr.particles.mass,gr.particles.rho,gr.particles.h,
        gr.particles.id,gr.particles.itype], axis=1)
#cut the big thing correspoding to the particle type
    gas_data=full_data.loc[lambda df: df['itype']==0,:]
    star_data=full_data.loc[lambda df: df['itype']==2,:]
    feed_data=full_data.loc[lambda df: df['itype']==1,:]
    dark_data=DM_data.loc[lambda df: df['itype']==3,:]
#write everything in s, g and f files

    np.savetxt(outpath+"g"+str(nstep).zfill(3),gas_data.to_numpy(),fmt="% .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % 7i % 1i")
    np.savetxt(outpath+"s"+str(nstep).zfill(3),star_data.to_numpy(),fmt="% .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % 7i % 1i") 
    np.savetxt(outpath+"f"+str(nstep).zfill(3),feed_data.to_numpy(),fmt="% .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % .5e % 7i % 1i")
    np.savetxt(outpath+"d"+str(nstep).zfill(3),dark_data.to_numpy(),fmt="% .5e % .5e % .5e % .5e % .5e % .5e % .5e  % .5e % .5e % 7i % 1i")
