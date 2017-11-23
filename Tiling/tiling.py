try:
    import math
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from aplpy import FITSFigure
    from astropy.io import fits
    from astropy.wcs import WCS
    from astropy import units as u
    from astropy.convolution import *
    import pandas as pd
except:
    print("Could not import all required modules!\set a conda enviroment and install using pip!")


class GLADECatalog:
    

    def __init__(self):
        # infile is for now the txt ascii catalog of glade
        infile = "GLADE_2.2.txt"
        names = ['SDDSSname','flag1', 'RA','dec','dist','dist_err','z','B','Berr','J','Jerr','H','Herr','K','Kerr','flag2','flag3']
        usecols = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        dtype = {'SDDSSname':str , 'flag1': str,  'RA':float, 'dec':float, 'dist': float , 'dist_err': float, 'z': float, 'B' : float, 'Berr' : float , 'J':float , 'Jerr':float, 'H':float, 'Herr':float, 'K':float, 'Kerr':float, 'flag2':str, 'flag3':str}
        
        self.GLADE = pd.read_csv(infile,sep=' ', dtype=dtype, names = names, usecols = usecols, na_values = 'null' )

    def visualize(self):
        fig = plt.figure()
        ax1= fig.add_subplot(121)
       
        ax1.hexbin(self.GLADE['RA'],self.GLADE['dec'])
        ax1.set_xlabel("ra [deg]")
        ax1.set_ylabel("dec [deg]")
        ax2 = fig.add_subplot(122, projection = '3d')
        ax2.scatter(self.GLADE['RA'],self.GLADE['dec'],self.GLADE['z'])
        ax2.set_xlabel("ra [deg]"), ax2.set_ylabel("dec [deg]"), ax2.set_zlabel("z")
        plt.show()

class Tiling:
    global rFoV
    rFoV = 1.5
    global degtorad
    degtorad = math.pi/180.

    
    def __init__(self, infile):
        input = fits.open(infile)
        hdu = input[1]
        wcs = WCS(hdu.header)
        self.degperpix = abs(hdu.header['CDELT1'])
        self.pixperfov = np.ceil(rFoV/self.degperpix)

        #Start by convolving 
        kernel = Tophat2DKernel(self.pixperfov)
        hdu.data = convolve(hdu.data,kernel)
        
        self.hdu = hdu
        self.hdudata = hdu.data
        
        xbins = hdu.header['NAXIS1']
        ybins = hdu.header['NAXIS2']

        X, Y = np.meshgrid(np.arange(xbins),np.arange(ybins))
        lon , lat = wcs.all_pix2world(X,Y,0)# zero means start poin, 1 for fortran-like indexing
        self.lon = lon
        self.lat = lat
        print("hdu object")
        
    

    def get_max(self):
        
        max_byrow = [max(self.hdudata[i]) for i in range(0,len(self.hdudata))] #compute tha max proba in each row
        max_p = max(max_byrow) #get the max proba of the max in each row
    
        max_r = [i for i, j in enumerate(max_byrow) if j == max_p][0] # finds the index in row of the max proba
        max_c = [i for i,j in enumerate(self.hdudata[max_r]) if j ==max_p][0]# finds the index in column of the max proba

        return max_r,max_c #retunrs the INDEX for ra,dec array of max value
        
    def draw_circle(self,ra,dec,image,edgecolor='b',rFoV=rFoV):
        image.show_circles(ra,dec,rFoV,linewidth=0.5,edgecolor=edgecolor)

    def make_hessimage_circles(self):
        
        hess_image = FITSFigure(self.hdu, hdu=self.hdu, figsize=(6.5,6))#no me preguntes que hace hdu=hdu, boh
    
        max_r, max_c = self.get_max()
        
        max_ra = self.lon[max_r,max_c]
        max_dec = self.lat[max_r,max_c]

        self.draw_circle(max_ra,max_dec,hess_image)

        proba = self.proba_circ(max_ra,max_dec,hess_image)
        print ("Proba in max point;", proba)
        #estetics 
        hess_image.show_colorscale(cmap="afmhot")
        hess_image.add_colorbar()
        hess_image.axis_labels.set_xtext('Right Ascension (J2000)')
        hess_image.axis_labels.set_ytext('Declination (J2000)')
        hess_image.tick_labels.set_xformat('dd.dd')
        hess_image.tick_labels.set_yformat('dd.dd')
        plt.tight_layout()

        return hess_image
    
    def proba_circ(self,ra,dec,image):

        #first compute the distance from the center of the circle to each point in map
        gamma = np.sqrt( ((ra-self.lon)*np.cos(dec*degtorad))**2 + (dec - self.lat)**2) 
        gammain = gamma<rFoV #returns a matrix of Trues and Falses depending on if the distance is smaller than the rFoV value
        self.draw_circle(self.lon[gammain],self.lat[gammain],image,'g',0.02)

        inreg = self.hdudata[gammain]
        norm = inreg.shape[0]
        return sum(self.hdudata[gammain]/norm)
    def overlaycatalog(self,ra,dec,image):
        self.draw_circle(ra,dec,image,'r',0.02)
        

    '''
    def more_circles(self,ra_max,dec_max):
        # returns a numpy array with tree colums
        # ra, dec, proba

        # parameters
        steps = 10
        angdist = 2.8

        angles = np.arange(0,360,steps)
        dec = dec_max + angdist*np.sin(angles*degtorad)
        ra = ra_max + angdist*np.cos(angles*degtorad)/np.cos(dec*degtorad)

        dtype = [('index',int),('ra',float),('dec',float),('probability',float)]
        values = []

        for j in range(0,len(ra)):
            values.append((j,ra[j],dec[j],proba_circ(ra[j],dec[j])))

        return np.array(values,dtype = dtype)
    '''

def main():
    A =  ["fits/gbm_gnd_loc_map_531752087.fits" , "fits/gbm_gnd_loc_map_531833351.fits", "fits/gbm_gnd_loc_map_531766142.fits", "fits/gbm_gnd_loc_map_532212622.fits", "fits/gbm_gnd_loc_map_531799124.fits"]
    glade = GLADECatalog()
    #glade.visualize()
    for j in A:
        a = Tiling(j)
        
        hess_image = a.make_hessimage_circles()
        a.overlaycatalog(glade.GLADE['RA'][glade.GLADE['z']<1.6],glade.GLADE['dec'][glade.GLADE['z']<1.6],hess_image)
        
        plt.show()


if __name__ == "__main__":
    main()

