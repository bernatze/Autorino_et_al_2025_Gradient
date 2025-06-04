# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:14:38 2024

@author: Adrian
"""
# This script generates a .txt that's the input for running a series of Evolver simulations from the cluster Terminal
import random
import numpy as np
############### Simulation parameters and details ####################

SS=50 # Number of simulations (Total N initial tillings for each condition)
N= 0 # Index for the first tilling to create a simulator
L=12 # Size of the network (approximately L^2)

rho =[0.70] # Rho to simulate

t_min=0.005 # for final alpha
t_max=0.1 # for initial alpha

n_bins=12

# Control parameters for Weibull distribution
shape=1.5
scale=0.025

it=20 # Total
t_bigt=1
it_each=20 # Printed each x iterations

Name_exp='exp/' # Must contain / at the end
#Name_out_folder='TCJM22/'
t_label='tRandomWeibull'

# alphas = ['0.700','0.720','0.750','0.780','0.800','0.820','0.840','0.850','0.855','0.860','0.865','0.870','0.875','0.880','0.900','0.920','0.950','0.980']
# alphas = ['0.700','0.720','0.750','0.780','0.800','0.820','0.840','0.850','0.855','0.860','0.865','0.870','0.875','0.880','0.900','0.920','0.950','0.980']
alphas = ['0.725','0.750','0.775','0.800','0.825','0.850','0.860','0.864','0.868','0.872','0.880','0.890','0.905','0.920','0.935','0.950','0.975']
# alphas = ['0.900','0.940','0.990']
# alphas = ['0.690','0.750','0.800','0.840','0.850','0.860','0.865','0.870','0.880','0.900','0.940','0.990']
#alphas = ['0.690','0.750','0.800','0.840','0.855','0.865','0.875','0.900','0.950','0.990']
# alphas = ['0.720','0.780','0.820','0.850','0.860','0.865','0.870','0.880','0.920','0.970']
bins=np.linspace(t_min,t_max,n_bins)

Mono='On'
R=0.5

# alphas = ['0.600','0.625','0.650','0.675','0.700','0.725','0.750','0.775','0.800','0.825','0.850','0.875','0.900','0.925', '0.950', '0.975', '1.000']
# alphas = ['0.700','0.720','0.750','0.780','0.810','0.825','0.840','0.850','0.860','0.875','0.890', '0.920', '0.950']
# alphas = ['0.860','0.865','0.870', '0.875', '0.880','0.885']
# alphas = ['0.700','0.720','0.750','0.780','0.800','0.820','0.840','0.850','0.855','0.860','0.865','0.870','0.875','0.880','0.900','0.920','0.950','0.980']
# alphas = ['0.690','0.720','0.750','0.780','0.800','0.820','0.840','0.850','0.855','0.860','0.865','0.870','0.875','0.880','0.900','0.920','0.950','0.970','0.990']
# alphas = ['0.690','0.750','0.800','0.840','0.855','0.865','0.875','0.900','0.950','0.990']


# ----------------- CODE ---------------------- #


PathIn='/path_to_folder'+Name_exp
PathOut='/path_to_folder/'+Name_exp

Pathforfiles=PathIn

p_hole_string=[]
for m in rho:
    p_hole_string.append(str(m))
    
#Simulation generator begins here

N=N-1
for gg in range (0,SS-1-N):
    N = N + 1  
    for k in range (0,len(p_hole_string)):    

        # for aa in range(0,len(alphas)):
        if Mono=='On':
            MasterFileName = 'Simulator_L{}_Frac{}_Alphas_N{}_t{}_It{}_Mono.txt'.format(L,p_hole_string[k] ,N,t_label,it)  
        else:
            MasterFileName = 'test_Simulator_L{}_Frac{}_Alphas_N{}_t{}_It{}.txt'.format(L,p_hole_string[k] ,N,t_label,it)
        File=open(Pathforfiles+MasterFileName, 'w', newline='\n')
        #Use the following three lines only to run the visual snapshots
        #File.write('echo "s\n') #instructions to be passed to Evolver as input begin here
        #File.write('q\n') #evolver command
        #File.write('o\n') #evolver command
        File.write("echo 'o\n") #evolver command
        File.write('r\n') #evolver command to break segments
        File.write('r\n')
        File.write('r\n')

        File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
        File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*1.0)\n')
        File.write(f't {t_min}; g 100; o; g 100; r; o; g 100\n')
        File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
        File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*1.0)\n')
        File.write(f't {t_min}; g 100; o; g 100; r; o; g 100\n')
        # File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
        # File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(1.95)\n')
        # File.write(f't { t_1}; g 100; o; g 100; r; o; g 100\n')
        
        
        for aa in reversed(alphas):
                
            for l in range (0,it-t_bigt): #I use two loops instead of one in case you want to export data every it iterations
                # for j in range (0,it):
                n_rand=np.random.weibull(shape,1)*scale
                bin_index=np.digitize(n_rand+t_min/2,bins)-1
                t_rand=np.round(bins[bin_index],3)
                File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
                File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*{})\n'.format(aa))
                File.write(f't { t_rand[0]}; g 100; o; g 100; r; o; g 100\n')
                    # j= j+1                
                l = l+1 

            for l in range (it-t_bigt,it): #I use two loops instead of one in case you want to export data every it iterations
                # for j in range (0,it):
                    
                File.write('foreach edges ff where sum(ff.faces,1) == 1 do ff.tension:=1.0\n')
                File.write('foreach edges ff where sum(ff.faces,1) == 2 do ff.tension:=(2*{})\n'.format(aa))
                File.write(f't { t_min}; g 100; o; g 100; r; o; g 100\n')
                    # j= j+1                
                l = l+1
                
#                if (l) % it_each == 0:
                    
            if Mono=='On':
                filename = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}_Mono.txt'.format(L,R,p_hole_string[k], aa, N, l,t_label)
            else:
                filename = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.txt'.format(L,R,p_hole_string[k], aa, N, l,t_label)   
            File.write('foreach edges ff where sum(ff.faces,1) == 2 do list ff.facets >> "{}{}"\n'.format(PathOut, filename))
                    
            if Mono=='On':
                filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}_Mono.ps'.format(L,R,p_hole_string[k], aa, N, l,t_label)
            else:
                filename_ps = 'Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.ps'.format(L,R,p_hole_string[k], aa, N, l,t_label)                    
            File.write('FULL_BOUNDING_BOX ON; ps_stringwidth:=0.00004; POSTSCRIPT "{}{}"\n'.format(PathOut, filename_ps))
                   
            if Mono=='On':
                filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}_Mono.fe'.format(L,R,p_hole_string[k], aa, N, l,t_label)
            else:
                filename_fe ='Fcells_L{}_R{}_rho{}_Alpha{}_N{}_Iteration{}_t{}.fe'.format(L,R,p_hole_string[k], aa, N, l,t_label)
            File.write('DUMP "{}{}"\n'.format(PathOut, filename_fe))
        

        
        File.write('q\n') #evolver command
        
        # name='Lattice_L{}Cells_R{}_rho{}_N{}.fe'.format(L,R,rho[k],i)
        if Mono=='On':
            inputname = '/bin/evolver {}Lattice_L{}Cells_R{}_rho{}_N{}_Mono.fe'.format(PathIn,L,R,p_hole_string[k],N)
        else:
            inputname = '/bin/evolver {}Lattice_L{}Cells_R{}_rho{}_N{}.fe'.format(PathIn,L,R,p_hole_string[k],N)            
        File.write("q' | {}\n".format(inputname)) #evolver command
                      
    
        File.write('\n')
        # File.write('read')
        File.close()
