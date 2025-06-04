# -*- coding: utf-8 -*-
"""
@author: Elisa
"""
# This script generates a .txt that's the input for running a series of Evolver simulations from the cluster Terminal
import random
import numpy as np

############### Simulation parameters and details ####################
SS = 70 # Number of simulations (Total N initial tillings for each condition)
N = 0 # Index for the first tiling to create a simulator
L = 26 # Size of the network (approximately L^2)

t_min = 0.005 # min t for Weibull distrib and used for hard spheres iterations and concluding simulation
t_max = 0.14 # max t value for Weibull distrib
t_label='005p14'

n_bins = 12
it = 20     # number of iteration 
#t_bigt = 1
#it_each = 5 # Printed each x iterations

# Control parameters for Weibull distribution
shape=1.4
scale=0.035

rho = [0.80] # Rho to simulate
type='Mono'
Name_exp = 'exp34/'       # Must contain / at the end

bins=np.linspace(t_min,t_max,n_bins)

Mono='On'
R=0.5   # cell radius 

#linear gradient
#y_levels = ['27.45','24.4','21.35','18.3','15.25','12.2','9.15','6.1','3.05']       # L=35
y_levels = ['20.34','18.08','15.82','13.56','11.3','9.04','6.78','4.52','2.26']      # L=26
#y_levels = ['23.49','20.88','18.27','15.66','13.05','10.44','7.83','5.22','2.61']   # L=30
#y_levels = ['11.7','10.4','9.1','7.8','6.5','5.2','3.9','2.6','1.3']                # L=15 
alphas = ['0.950','0.930','0.910','0.890','0.870','0.850','0.830','0.810','0.790','0.770']


# ----------------- CODE ---------------------- #

#PathIn='/path_to_folder/'+Name_exp
#PathOut='/path_to_folder/'+Name_exp
#Pathforfiles=PathIn

p_hole_string=[]
for m in rho:
    p_hole_string.append(str(m))
    
#Simulation generator begins here
N=N-1
for gg in range (0,SS-1-N):
#for gg in range (0,1):
    
    N = N + 1  
    PathIn='/home/floris/evolver/input/'+Name_exp+'N'+str(N)+'/'
    PathOut='/home/floris/evolver/output/'+Name_exp+'N'+str(N)+'/'
    #Pathforfiles=PathIn
    Pathforfiles='/home/floris/evolver/input/'+Name_exp
    
    for k in range (0,len(p_hole_string)):    

        if Mono=='On':
            MasterFileName = 'Simulator_L{}_Frac{}_Alphas_N{}_t{}_It{}_Mono.txt'.format(L,p_hole_string[k],N,t_label,it)  
        else:
            MasterFileName = 'L26_Simulator_L{}_Frac{}_Alphas_N{}_t{}_It{}.txt'.format(L,p_hole_string[k],N,t_label,it)
        
        File = open(Pathforfiles+MasterFileName, 'w', newline='\n')
        File.write("echo 'o\n") # evolver command for nodes popping
        File.write('r\n')       # evolver command to break segments
        File.write('r\n')
        File.write('r\n')

        # hard spheres, fixed t
        for l in range(0,4):
            
            File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
            File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*1.0)\n')
            File.write(f't {t_min}; g 100; o; g 100; r; o; g 100\n')
        
        filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k],'1',N,4,t_label)
        File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
        filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k],'1',N,4,t_label)    
        File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))

        # decrease alpha in the whole tissue, t extracted from Weibull distrib
        for i in range(0,it):
            n_rand=np.random.weibull(shape,1)*scale
            bin_index=np.digitize(n_rand+t_min/2,bins)-1
            t_rand=np.round(bins[bin_index],3)
                
            File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
            File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*0.975)\n')
            File.write(f't {t_rand[0]}; g 100; o; g 100; r; o; g 100\n')
            l=l+1
        
        #filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k],'0.975',N,it,t_label)
        #File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
        #filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k],'0.975',N,it,t_label)
        #File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))

        # decrease alpha in the whole tissue, t extracted from Weibull distrib
        #for l in range(0,it):
            
         #   n_rand=np.random.weibull(shape,1)*scale
         #   bin_index=np.digitize(n_rand+t_min/2,bins)-1
         #   t_rand=np.round(bins[bin_index],3)
                
         #   File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
         #   File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*0.950)\n')
         #   File.write(f't {t_rand[0]}; g 100; o; g 100; r; o; g 100\n')
         #   l = l+1
        
        #filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k],'0.950',N,it,t_label)
        #File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
        #filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k],'0.950',N,it,t_label)
        #File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))
        
        for i in range(1,len(alphas)):  
            
            y_levels_tmp = y_levels[:i]
            alphas_tmp = alphas[:i+1]
    
            for l in range(it):

                n_rand=np.random.weibull(shape,1)*scale
                bin_index=np.digitize(n_rand+t_min/2,bins)-1
                t_rand=np.round(bins[bin_index],3)
            
                File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
                File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 > {y_levels_tmp[0]} do ff.tension:=(2*{alphas_tmp[0]})\n')
        
                for j in range(len(y_levels_tmp) - 1):
                    File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 < {y_levels_tmp[j]} AND (ff.vertex[1].y+ff.vertex[2].y)/2 > {y_levels_tmp[j+1]} do ff.tension:=(2*{alphas_tmp[j+1]})\n')
                    
                File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 < {y_levels_tmp[-1]} do ff.tension:=(2*{alphas_tmp[-1]})\n')
                File.write(f't {t_rand[0]}; g 100; o; g 100; r; o; g 100\n')
                l = l+1

            #filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k],alphas_tmp[-1],N,it,t_label)
            #File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
            #filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k],alphas_tmp[-1],N,it,t_label)
            #File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))

        # ending of the simulation with the same t used at the beginning (for resolution consistency)
        for l in range(1):     
            
            File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
            File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 > {y_levels_tmp[0]} do ff.tension:=(2*{alphas_tmp[0]})\n')
        
            for j in range(len(y_levels_tmp) - 1):
                File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 < {y_levels_tmp[j]} AND (ff.vertex[1].y+ff.vertex[2].y)/2 > {y_levels_tmp[j+1]} do ff.tension:=(2*{alphas_tmp[j+1]})\n')
                    
            File.write(f'foreach edges ff where sum(ff.faces,1) == 2 AND (ff.vertex[1].y+ff.vertex[2].y)/2 < {y_levels_tmp[-1]} do ff.tension:=(2*{alphas_tmp[-1]})\n')
            File.write(f't {t_min}; g 100; o; g 100; r; o; g 100\n')          

        filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k],alphas_tmp[-1],N,1,t_label)
        File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
        filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k],alphas_tmp[-1],N,1,t_label)
        File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))
    
    File.write('q\n') # evolver command
    
    if Mono=='On':
        inputname = '/usr/local/bin/evolver {}Lattice_L{}Cells_R{}_rho{}_N{}.fe'.format(PathIn,L,R,p_hole_string[k],N)
    else:
        inputname = '/usr/local/bin/evolver {}Lattice_L{}Cells_R{}_rho{}_N{}.fe'.format(PathIn,L,R,p_hole_string[k],N)            
    
    File.write("q' | {}\n".format(inputname)) # evolver command 
    File.write('\n')
    # File.write('read')
    File.close()
