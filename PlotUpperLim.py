import numpy as np
import matplotlib.pyplot as plt
#plt.style.use('classic')



data = np.loadtxt("UppLim_cornelia.txt",dtype = np.float32, skiprows=1)
nR = 1
GRBname = "GRB_HAP"
print(data)


# DIFF Flux in band (evaluation at log middle)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useOffset=False, useMathText=True, useLocale = False)
plt.errorbar(x= np.log10(data[:,2]), y = data[:,3], xerr=1./12., yerr=5.0e-12  , uplims = True, linestyle='none')
#plt.xscale("log")
plt.xlabel("log(Energy/TeV)")
plt.ylabel("Differential Flux Upper Limit 95\% CL [TeV-1 cm^-2 s^-1]")
plt.title("%s_%i HAP Differential upper limits"%(GRBname,nR))
plt.savefig("diff%s%i.png"%(GRBname,nR))
plt.clf()



#Integral in band
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useOffset=False, useMathText=True, useLocale = False)
plt.errorbar(x= np.log10(data[:,2]), y = data[:,4], xerr=1./12., yerr=5.0e-13  , uplims = True, linestyle='none')
#plt.xscale("log")
plt.xlabel("log(Energy/TeV)")
plt.ylabel("Integral Flux Upper Limit 95\% CL [cm^-2 s^-1]")
plt.title("%s_%i HAP Integral upper limits"%(GRBname,nR))
plt.savefig("int%s%i.png"%(GRBname,nR))
plt.clf()


#integral above
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useOffset=False, useMathText=True, useLocale = False)
plt.errorbar(x= np.log10(data[:,2]), y = data[:,5], xerr=1./12., yerr=1.0e-12  , uplims = True, linestyle='none')
#plt.xscale("log")
plt.xlabel("log(Energy/TeV)")
plt.ylabel("Integral Flux E> Upper Limit 95\% CL [cm^-2 s^-1]")
plt.title("%s_%i HAP Integral upper limits"%(GRBname,nR))
plt.savefig("intabove%s%i.png"%(GRBname,nR))
plt.clf()

'''
x= np.arange(0.1, 4, 0.5)
y = np.exp(-x)
yerr = 0.1 + 0.2*np.sqrt(x)
xerr = 0.1 + yerr

plt.errorbar(x, y, yerr=[yerr, 2*yerr], xerr=[xerr, 2*xerr], fmt='--o')
plt.show()
'''

