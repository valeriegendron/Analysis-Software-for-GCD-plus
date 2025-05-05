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
#for nstep in range(355,501):
for nstep in range(len(gr.dump_steps)):

    gr.read_base(nstep)  #reads base data
    gr.read_dark()
    gr.convert_units() #convert to useful units
#create a big ass thing with all the data
    DM_data=pd.concat([
        gr.particles.x,gr.particles.y,gr.particles.z,
        gr.particles.vx,gr.particles.vy,gr.particles.vz,
        gr.particles.mass,gr.particles.rho,gr.particles.h,
        gr.particles.id,gr.particles.itype], axis=1)
#cut the big thing correspoding to the particle type
    dark_data=DM_data.loc[lambda df: df['itype']==3,:]
#write everything in s, g and f files

    np.savetxt(outpath+"d"+str(nstep).zfill(3),dark_data.to_numpy(),fmt="% .5e % .5e % .5e % .5e % .5e % .5e % .5e  % .5e % .5e % 7i % 1i")
