
from xcdf import XCDFFile
import ROOT as root
import numpy as np
import argparse 
import math
import random
#from gammapy.time import exptest
import root2matplot as r2m
import matplotlib.pyplot as plt
radtodeg = 180./math.pi

def exptest(time_delta):
  mean_time = np.mean(time_delta)
  normalized_time_delta = time_delta / mean_time
  mask = normalized_time_delta < mean_time
  sum_time = 1 - normalized_time_delta[mask] / mean_time
  sum_time_all = np.sum([sum_time])
  m_value = sum_time_all / len(time_delta)
  print("m_value",m_value)
  # the numbers are from Prahl(1999), derived from simulations
  term1 = m_value - (1 / 2.71828 - 0.189 / len(time_delta))
  term2 = 0.2427 / np.sqrt(len(time_delta))
  mr = term1 / term2
  return mr

parser = argparse.ArgumentParser(description='exp test for variability verification in DC gamma experiments')

parser.add_argument('-i' , '--input'   , help='Input XCDF' , dest="infile")
parser.add_argument('-o' , '--out'   , help='Output ROOT file' , dest="outfile")


args =  parser.parse_args()

infile = args.infile
outfile = args.outfile

#initialize the ROOT related stuff

#output
out = root.TFile(outfile,"RECREATE")

#histogram for poisson verif
hPoisson = root.TH1D("poisson","",75,0.,150.)
#hitogram of all sky rate
hRaDec = root.TH2D("sky","sky",200,0.,360.,100,18.,25.)

 
#function to fit eq 2 of arXiv:astro-ph/9909399
expfunc = root.TF1("fit_pois","expo",0.,150.)


#parameters to be extracted from xcdf file
params = "rec.ra, rec.dec, rec.gpsNanosec, rec.PINC, rec.CxPE40, rec.nHit"

#load the xcdf into xf object
xf = XCDFFile(infile)

#initialize varaibles for filling histograms
t0 = 0.
nev = 0

#loop over all the entries of xcdf file
dTimes = []
Ra = []
Dec = []

MR = []
MRT = []
alltimes = []

for vals in xf.fields(params):
 ra, dec, gpsSec, PINC, CxPE40, nHit = vals
 t = gpsSec - t0
 alltimes.append(gpsSec)
 if (nev<49):
  nev += 1
  hPoisson.Fill(t/100000.)
  dTimes.append(t/100000.)
  t0 = gpsSec
  #fill sky
  Ra.append(ra*radtodeg)
  Dec.append(dec*radtodeg)
 
  hRaDec.Fill(ra*radtodeg,dec*radtodeg)
 else:
  
  hPoisson.Fill(t/100000.)
  dTimes.append(t/100000.)
  print(len(dTimes))
  t0 = gpsSec
  #fill sky
  Ra.append(ra*radtodeg)
  Dec.append(dec*radtodeg)
 
  hRaDec.Fill(ra*radtodeg,dec*radtodeg)


  hPoisson.Fit("fit_pois","NQ")
  
  exp_const = expfunc.GetParameter(0)
  exp_slope = expfunc.GetParameter(1)
  #print(exp_const,exp_slope)

  hTPoisson = root.TH1D("tpoisson","",75,0.,150.)
 
  dTTimes=[]
  for i in range (0,nev+1): 
   a = random.expovariate(-1*exp_slope)
   hTPoisson.Fill(a)
   dTTimes.append(a)

  print(dTimes)
  print(dTTimes)
  # get the bin content of each histogram (teo and measured) 
  print(hTPoisson.GetNbinsX(),hPoisson.GetNbinsX())

  delta = []
  for iBin in range(0,hTPoisson.GetNbinsX()):
   delta.append(hTPoisson.GetBinContent(iBin)-hPoisson.GetBinContent(iBin))

  hist = r2m.Hist(hPoisson)
  histT = r2m.Hist(hTPoisson)

  '''
  plt.subplot(211)
  stack = r2m.HistStack() 
  stack.add(hist,label='All sky counts') 
  stack.add(histT, label='Poisson Porcess')
  stack.bar(alpha=0.5)
  stack.show_titles()
  plt.legend()
  plt.yscale('log')
  plt.ylabel('log(NEvents)')

  plt.subplot(212)
  plt.plot(delta)
  plt.ylabel('delta NEvents')
  plt.xlabel('delta T [ms]')
  plt.show()
  '''
  mr = exptest(dTimes)
  print(mr) 

  mrT = exptest(dTTimes)
  print(mrT)

  MR.append(mr)
  MRT.append(mrT)

  del hPoisson
  del expfunc  
  del hTPoisson
  del hRaDec
  del dTimes
  del dTTimes
  #histogram for poisson verif
  hPoisson = root.TH1D("poisson","",75,0.,150.)
  
  #hitogram of all sky rate
  hRaDec = root.TH2D("sky","sky",200,0.,360.,100,18.,25.)
  #function to fit eq 2 of arXiv:astro-ph/9909399
  expfunc = root.TF1("fit_pois","expo",0.,150.)
  
  dTimes = []
  dTTimes = []
  nev = 0 

deltas = []
for j in range(0,len(alltimes)-1):
 deltas.append(alltimes[j+1]-alltimes[j])
