import ROOT as root
import numpy as np
import matplotlib.pyplot as plt
import root2matplot as r2m



def plot2DH(infile,vars,cut,drawopt = "COLZ"):
  file = root.TFile(infile)
  tree = file.Get("XCDF")
  tree.Draw(vars,cut,drawopt)
  hist = r2m.Hist2D(tree.GetHistogram())
  hist.colz()
  title = raw_input("Plot Title:")
  xlabel = raw_input("xlabel:")
  ylabel = raw_input("ylabel:")
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.show()
  
def plot1DH(infile,var,cut):
  file = root.TFile(infile)
  tree = file.Get("XCDF")
  tree.Draw(var,cut)
  hist2 = r2m.Hist(tree.GetHistogram())
  plt.figure(1,(8,6))
  title = raw_input("Plot Title:")
  xlabel = raw_input("xlabel:")
  ylabel = raw_input("ylabel:")
  plt.title(title)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.legend()
  hist2.bar()
  plt.show()
