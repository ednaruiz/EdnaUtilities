#  Brief: set some points for observation and measure the completnes at each distance
# like a bullet through an onion, yummy

import matplotlib.pyplot as plt
import random as random
import pandas as pd
import numpy as np

class GLADECatalog:
    global degtorad
    degtorad = np.pi/180.
    def __init__(self):
        # infile is for now the txt ascii catalog of glade
        infile = "GLADE_2.2.txt"
        names = ['RA','dec','dist','dist_err','z']
        usecols = [6,7,8,9,10]
        dtype = {'RA':float, 'dec':float, 'dist': float , 'dist_err': float, 'z': float}
        
        self.GLADE = pd.read_csv(infile,sep=' ', dtype=dtype, names = names, usecols = usecols, na_values = 'null' )

    def visualize(self):
        fig = plt.figure()
        ax1= fig.add_subplot(111)
       
        ax1.hexbin(self.GLADE['RA'],self.GLADE['dec'])
        ax1.set_xlabel("ra [deg]")
        ax1.set_ylabel("dec [deg]")
        plt.show()
     
    def visualize_shells(self,min_dist,max_dist):
    
        fig = plt.figure(figsize=(9,6))
        ax1= fig.add_subplot(111)
        ax1.set_title("GLADE for %0.1f to %0.1f Mpc distance"%(min_dist,max_dist))
        ax1.hexbin(self.GLADE['RA'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist],self.GLADE['dec'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist])
        ax1.set_xlabel("ra [deg]")
        ax1.set_ylabel("dec [deg]")
        plt.savefig("cipolla%f-%f.png"%(min_dist,max_dist))

    def count_galaxies(self,ra,dec,min_dist,max_dist):
        
        rFoV = 5. #CT5 field of view, but whatever actually...
        Ra = self.GLADE['RA'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist]
        Dec = self.GLADE['dec'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist]

        gamma = np.sqrt( ((ra-Ra)*np.cos(dec*degtorad))**2 + (dec - Dec)**2)
        gammain = gamma<rFoV

        return len(gammain[gammain == True])


a = GLADECatalog()

rand_ra = []
rand_dec = []

D = np.arange(0,300,5)

Count = []
for iDist in range (0,len(D)):
    cD = []
    for j in range (50):
        rra = float(random.randrange(0,360,1)+random.random())
        rdec = random.randrange(-180,180,1)+random.random()
        print(rra,rdec)
        rand_ra.append(rra)
        rand_dec.append(rdec)
        
        n = a.count_galaxies(ra = rra,dec = rdec, min_dist = D[iDist], max_dist = D[iDist]+5 )
        
        cD.append(n)
    print(np.asarray(cD))
    Count.append(cD)


plt.plot(D,np.std(Count,axis=1))
plt.show()


