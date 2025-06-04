#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 10:05:07 2023

@author: Bernat modified by Adrian
"""

# import Generate_random_tiling as GRT
import numpy as np
import Generate_random_tiling_Mono_exact as GRT

######################### parameters
    
L=26 # size in cells
delta=4     
R=0.5
N=1 # number of tilings
Origin=89

rho =[0.80]
folder_to_save='path_to_folder/'

######################### create "it" tilings to be read by surface evolver

for i in range(0,N):
    print('N= ',i)
    for k in range(len(rho)):
        print('rho= ',rho[k])
        # for l in alphas:
        # name with my own criteria
        name='Lattice_L{}Cells_R{}_rho{}_N{}'.format(L,R,rho[k],i+Origin)
        # name='Lattice_L'+str(L)+'_R'+str(R).replace('.', '_')+'_rho'+str(rho).replace('.', '_')+'_N'+str(i)+'.fe'
        name_output=folder_to_save+name
        # GRT.create_random_tiling_2D(L, R,rho[k], name_output+'.fe')
        GRT.create_random_tiling_2D(L,R,rho[k],delta, name_output+'.fe')



