import os
import numpy as np
import argparse



parser = argparse.ArgumentParser("Process simple analysis")

parser.add_argument('--source',help = "Source Config File", dest = 'source',required = True)
parser.add_argument('--cuts',help="Cuts Config File",dest = 'cuts',required = True)
parser.add_argument('--out',help = "Outdir",dest="out",required = True)
parser.add_argument('--weight',help = "Weights file",dest="weight",required = True)

args = parser.parse_args()

os.system("mkdir %s "%(args.out))

nBins = len(np.loadtxt(args.cuts,dtype='str'))

dump = "simple-analysis-dump --outdir %s --source-file %s --cuts-file %s &&"%(args.out,args.source,args.cuts)

background = ""
smooth = ""
significance = ""
for iBins in range (0,nBins):
  background = background + "simple-analysis-background -o %s -b %i -e 1.0 && "%(args.out,iBins)
  smooth = smooth + "simple-analysis-smooth --outdir %s -b %i -r 0.2 --gauss && "%(args.out,iBins)
  significance = significance + "simple-analysis-significance --outdir %s -b %i -w %s && "%(args.out,iBins,args.weight)

final = "%s %s %s %s"%(dump,background,smooth,significance)
print(final[:-3])
os.system(final[:-3])
