#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 13:22:29 2021

@author: bernat
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../../../')

import Lattice
import pebble

if __name__ == '__main__':

    origin = 0
    N = 200
    for n in range(origin, N):

######################### Create the gradient probability
    
        levels=8    #9
        prob_link_del_gradient=[]
        a0=0.1    #0.1
        a=0.  #0.1

        """prob_link_del_gradient.append(a0)
    
        for i in range(1, levels):
            prob_link_del_gradient.append(a0+a*i)
            print(a0+a*i)"""

######################### Create lattice heterogeneous prob of link
    
        L=35   
        c=3.9              #L=15 c=3.64        #L=20 c=3.7   L=35 c=3.9     ####critical point
        g=[]
        region=[]
        Nodes_Region=[]
        
        if a == 0.0:
            g = Lattice.Blastocyst_Model(L,0.,c) 

            Empirical_levels=c*np.ones(levels)                
            y_pos=[]
            for i in range(0, len(g[2])):
                y_pos.append(g[2][i][1])
            
            min_y=min(y_pos)
            max_y=max(y_pos)
            D=max_y-min_y
            
            region=[]
            Nodes_Region=[]   ### number of nodes x region
            Nodes_Region=[0]*levels  #len(gradient)
            for i in range(0, len(g[2])):     #### region the node belongs to:
                if y_pos[i]<max_y:
                    re=int(((y_pos[i]-min_y)/D)*levels)   #len(gradient)
                    region.append(re)
                    Nodes_Region[re]=Nodes_Region[re]+1
                else: 
                    re=levels-1   #len(gradient)-1
                    region.append(re)
                    Nodes_Region[re]=Nodes_Region[re]+1  
            
            #print("nodes region ", Nodes_Region)
                    
        else:
            prob_link_del_gradient.append(a0)
            for i in range(1, levels):
                prob_link_del_gradient.append(a0+a*i)
                print(a0+a*i)
            #print("len prob_link_del_gradient ", len(prob_link_del_gradient))
                
            g, region, Nodes_Region=Lattice.Lattice_gradient(prob_link_del_gradient, c, L) 
        
            Empirical_levels=[]
            Empirical_levels=Lattice.Empirical_Gradient_Conn(g, levels, region)
            #print("len Empirical levels ", len(Empirical_levels))
            
        print("Empirical levels ", Empirical_levels)
            
        xx=[]
        xx=np.arange(0.07,1.07,1/len(Empirical_levels))
        print('***')
        plt.figure()
        plt.plot(xx, Empirical_levels, color='blue', linewidth=4, alpha=0.2)
        plt.ylim(0,5)
        plt.xlabel('Node Position y in the network', fontsize=17)
        plt.ylabel('Region average connectivity', fontsize=17)
        plt.show()
        plt.close()
        print('***')
        
    ###########################################################
    ###########################################################
    ############ Print the rigid cluster ######################
    
        Global_G=[]
        file=[]    
        #file=g[0]
        #print("g[0] ", g[0])
        filtered_g0 = [pair for pair in g[0] if pair != [-1, -1]]
        file = filtered_g0
        #print("file ", file)
        fileGeo=[]
        fileGeo=g[2]    
        #filtered_g2 = [item for i, item in enumerate(g[2]) if g[0][i] != [-1, -1]]  # I think it is not necessary
        
        ###############################################################
        #####             END Loading data                        #####
        ###############################################################
    
        ###############################################################        
        ########          Rigidity topological                  #######
        ###############################################################
        
        G = pebble.lattice() # initialize a lattice for the 'pebble' library
    
        bond=[]
        for i in range(0,len(file)):
            if (file[i][0]<file[i][1]):            
                #bond.append((np.int(file[i][0]),np.int(file[i][1])))
                bond.append((int(file[i][0]),int(file[i][1])))
        
        for i in bond:             # add bond within the G class
            G.add_bond(i[0],i[1])
        
    
        ##########################################################################
        ######## Finding rigid clusters of the network using 'pebble.py' library #
        ##########################################################################
    
        G.decompose_into_cluster() #### decomposing the network into rigid clusters
    
        ##########################################################################
        #####      Identifying the different clusters and their size          ####
        ##########################################################################
        
        ###### Giant Rigid Cluster
        
        subgraph=[]#giantcluster
        size=0
        size2=0
        K=0 #### Index of the GRC --to be indentified 
        Ks=[]
        sizes=[]
        K2=0
        Percolation_Cluster=[]
        
        ####### Running to all rigid clusters to find the largest one
    
        for key,value in G.cluster['index'].items():
                
            SubG=[]
            sizeSubG=0
                        
            for i in value:
                SubG.append(i)
                    
            sizeSubG=np.size(np.unique(SubG))
    
            if sizeSubG>2:
                
                for i in value:
                    Percolation_Cluster.append(i)
    
            if sizeSubG>size:
                size=sizeSubG
                K=key #### ID of the GRC
                
        Giant_Cluster=[]### Nodes in the giant cluster
        for i in G.cluster['index'][K]:
            Giant_Cluster.append(i)
        
        ####### presence in the giant cluster in terms of region
        
        Nodes_GRC=[]
        Nodes_GRC=np.unique(Giant_Cluster)
        #print("Nodes GRC ", Nodes_GRC)
    
        Nodes_Occupation_GRC=[]
        Nodes_Occupation_GRC=[0]*levels
        
        for i in range(0, len(Nodes_GRC)):
            #print("i ", i, "Nodes_GRC[i] ", Nodes_GRC[i], "region[Nodes_GRC[i]] ", region[Nodes_GRC[i]])
            re=region[Nodes_GRC[i]]
            Nodes_Occupation_GRC[re]=Nodes_Occupation_GRC[re]+1
        #print("Nodes_Occupation_GRC ", Nodes_Occupation_GRC)
        
        for i in range(0, levels):
            #print("Nodes_Occupation_GRC[i] ", Nodes_Occupation_GRC[i])
            #print("Nodes_Region[i] ", Nodes_Region[i])
            Nodes_Occupation_GRC[i]=Nodes_Occupation_GRC[i]/Nodes_Region[i]
    
        #print(Nodes_GRC)
        print(Nodes_Occupation_GRC)
        
                 
        ############# computing the ID of the second cluster #########  
        
        Non_Giant=[]
        size_G=0
        for key,value in G.cluster['index'].items():
            if key!=K:
                SubG=[]
                sizeSubG=0
                for i in value:
                    SubG.append(i)
                sizeSubG=np.size(np.unique(SubG))
                if sizeSubG>2:
                    Global_G.append(sizeSubG)
    
                if sizeSubG>size_G:
                    size_G=sizeSubG
                    K2=key   ### ID of the 2nd GRC
    
        ############# End computing the ID of the second cluster #####   
    
        size2=size_G
    
        ### Checking the cluster counting #####
        sizes_hist_Num=np.zeros(30)
            
    #    for i in range(0, len(Global_G)):
    #        sizes_hist_Num[Global_G[i][1]]=sizes_hist_Num[Global_G[i][1]]+1
         
    #    print(Global_G)
    
        ###  END Checking the cluster counting #####
        
        sys.stdout.write("\n")
    
        
        ###### Building the subgraphs corresponding to the GRC and the 2nd GRC
        Giant_Cluster=[]
        for i in G.cluster['index'][K]:
            Giant_Cluster.append(i)
    
        Second_Giant_Cluster=[]
        for i in G.cluster['index'][K2]:
            Second_Giant_Cluster.append(i)
                        
        #################################################################
        ####### Map the graph into the geometrical embedding in R2 ######
        #################################################################
        
        #################### The whole graph ############################
            
        Geo=[]
        BondA=np.array(bond)
        
        for i in range(0,len(fileGeo)):
            Geo.append((fileGeo[i][0],fileGeo[i][1]))
        
        GeoNet=[]
        
        for i in range(0,len(BondA)):#Geolocation of the whole graph
            Nod1=BondA[i][0]
            Nod2=BondA[i][1]
            GeoNet.append([Geo[Nod1],Geo[Nod2]])       
                
        #################### The rigidity cluster graph #################
        
        GeoNet_Rigidity=[]
        
        PC=np.array(Percolation_Cluster)
        
        for i in range(0,len(PC)):#Geolocation of the whole graph
            Nod1=PC[i][0]
            Nod2=PC[i][1]
            GeoNet_Rigidity.append([Geo[Nod1],Geo[Nod2]])     
        
        #################### The Giant rigidity cluster graph #############
        
        GeoNet_Rigidity_Giant=[]
        
        GC=np.array(Giant_Cluster)
        
        for i in range(0,len(GC)):#Geolocation of the whole graph
            Nod1=GC[i][0]
            Nod2=GC[i][1]
            GeoNet_Rigidity_Giant.append([Geo[Nod1],Geo[Nod2]])     
        
        #################### The second rigidity cluster graph #############
    
        GeoNet_Second_Rigidity_Giant=[]
        
        GC2=np.array(Second_Giant_Cluster)
        
        for i in range(0,len(GC2)):#Geolocation of the whole graph
            Nod1=GC2[i][0]
            Nod2=GC2[i][1]
            GeoNet_Second_Rigidity_Giant.append([Geo[Nod1],Geo[Nod2]])     
    
        ##################################################################
        ################## Drawing the graphs   ##########################             
        ##################################################################
        
        plt.figure(figsize=(10,10))
        plt.axis('off')
        plt.axis('equal')
    
    #    plt.title(Experiment+'%d | g' %q)
        for i in range(0,len(GeoNet)):#Plot of the whole graph
            coord1=[]
            coord2=[]
            coord1=np.array(GeoNet[i][0])
            coord2=np.array(GeoNet[i][1])
            plt.plot([coord1[0],coord2[0]],[coord1[1],coord2[1]], '-k', alpha=.2)
                    
        for i in range(0,len(GeoNet_Rigidity)): #Plot of the rigidity cluster
            coord1=[]
            coord2=[]
            coord1=np.array(GeoNet_Rigidity[i][0])
            coord2=np.array(GeoNet_Rigidity[i][1])
            plt.plot([coord1[0],coord2[0]],[coord1[1],coord2[1]], color='orange')
        
        for i in range(0,len(GeoNet_Rigidity_Giant)): #Plot of the giant rigidity cluster
            coord1=[]
            coord2=[]
            coord1=np.array(GeoNet_Rigidity_Giant[i][0])
            coord2=np.array(GeoNet_Rigidity_Giant[i][1])
            plt.plot([coord1[0],coord2[0]],[coord1[1],coord2[1]], '-r')
        
        if len(GeoNet_Second_Rigidity_Giant)>2:
            for i in range(0,len(GeoNet_Second_Rigidity_Giant)): #Plot of the giant rigidity cluster
                coord1=[]
                coord2=[]
                coord1=np.array(GeoNet_Second_Rigidity_Giant[i][0])
                coord2=np.array(GeoNet_Second_Rigidity_Giant[i][1])
                plt.plot([coord1[0],coord2[0]],[coord1[1],coord2[1]], '-b')                
     
        for i in range(0,len(g[2])):#Plot of the Nodes        
            plt.plot(g[2][i][0],g[2][i][1], 'o', fillstyle='full', markeredgecolor='black', markerfacecolor='white')
    
        
        Picture=0
        #Picture=str("Gradient_L20_c3.7_a0_01/a_"+str(a)+"/Pic_Gradient_a0_"+str(a0)+"_a_"+str(a)+"_N"+str(n)+".png")
        Picture=str("Gradient_L35_c3.9_a0_01/a_"+str(a)+"/Pic_Gradient_a0_"+str(a0)+"_a_"+str(a)+"_N"+str(n)+".pdf")
        plt.savefig(Picture, transparent=False)  #True  
        plt.show()  
        plt.close()
    
        f=open("name_folder"+str(a)+"/name_file"+str(a0)+"_a_"+str(a)+"_N"+str(n)+".csv", "a")
        f.write("Level_NW; Region_Av_Connectivity; Nodes_Occupation_GRC")
        f.write("\n")
        for k in range(0, len(Empirical_levels)):
            f.write(str(xx[k]))
            f.write("; ")
            f.write(str(Empirical_levels[k]))
            f.write("; ")
            f.write(str(Nodes_Occupation_GRC[k]))
            f.write("\n")
        f.close()
    
