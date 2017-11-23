## Brief: set some points for observation and measure the completnes at each distance
## like a bullet in a onion

import pandas as pd
import matplotlib.pyplot as pd
import astropy as astro


class GLADECatalog:
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
    
        fig = plt.figure()
        ax1= fig.add_subplot(111)
        ax1.set_title("GLADE for %f to %f Mpc distance"%(min_dist,max_dist))
        ax1.hexbin(self.GLADE['RA'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist],self.GLADE['dec'][self.GLADE["dist"]>min_dist][self.GLADE["dist"]<max_dist])
        ax1.set_xlabel("ra [deg]")
        ax1.set_ylabel("dec [deg]")
        plt.show()


