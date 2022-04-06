'''
Created on 21 Nov 2016

@author: kkuzn
'''
import sys
import getopt

import GC.GC as GC
import GC.GC_plots as GC_plots
# program to plot two graphs on same canvas
inputFile=""

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:d:o:r:vh",["filelist=", "dir="])
except getopt.GetoptError:
    # print help information and exit:
    print ' enter file name'
    sys.exit()

verb = False
dir  = False
pdfname=""
fn=""
fn_ref=""
fnames_ref=""
for o,a in opts:
    if o=='-f':
        print "proceeding for files", a
        fn = a
    if o=='-d':        
        print "proceeding for directory", a
        fn = a    
        dir = True
    if o=='-r':
        print "proceeding for reference file", a
        fn_ref = a
    if o=='-o':        
        print "output pdf/root files", a
        pdfname = a    
    if o=="-v":
        verb = True
    if o=="-h":
        print "here"
        exit()

# to plot GC for original curve
gcs = GC.GSset(fn, dir, verb, pdfname)

#Defines the names to be used for each peak
name={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon+CF_{4}","CO_{2}"],"C":["Argon","CO_{2}"]}

#defines the user range to be used to narrow the search for peaks
ranges={"B":[0.2,0.8],"C":[0.1,0.5]}
fnames = sorted(gcs.gcsets.keys())

for fn in fnames:
   print " files fn :  ",fn
   print "running for file inside"
   for column in ("B", "C"):
       print("column : ", column)
#      for fn in fnames:
   for column in("B"):
       print" calling Set Peak valley  function"
       gcs.setPeak(fn,column,name[column],ranges[column])
#       print" calling get Peak valley  function not useful now"
#       gcs.getPeakValley(fn,column,name[column])
       print "calling Multi plot function now"
       gcs.plotMulti(fn,column)
       print "done with Multi plot function now"

# for plotting reference curve GC individually    
gcs_ref = GC.GSset(fn_ref, dir, verb, pdfname)
name_ref={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon","CO_{2}"],"C":["Argon","CO_{2}"]}
ranges_ref={"B":[0.2,0.8],"C":[0.1,0.5]}
fnames_ref = sorted(gcs.gcsets.keys())
print "running for ref file : printing function ref " , fn_ref
print "function reference fnames_ref ", fnames_ref
#for fn_ref in fnames_ref:
print "reference files fn_ref  ", fn_ref
print "running for ref file inside"
#              for column in ("B","C"):
#                print("column : ", column)
#              for fn_ref in fnames_ref :

for column in("B"):
    print" calling set Peak  function"
    gcs_ref.setPeak(fn_ref,column,name_ref[column],ranges_ref[column])
    print" calling get Peak valley  function"
#    gcs_ref.getPeakValley(fn_ref,column,name_ref[column])
#    print" calling multi plot function"
    gcs_ref.plotMulti(fn_ref,column)
    print" done with  multi plot function"

#initialize to plot two curve from original and reference files on the same canvas
#from here on the function that will be first called is stored in GC_plots
gcs_plot = GC_plots.plots(fn, dir, verb, pdfname,fn_ref, dir, verb, pdfname)
gcs_plot.setPeak(fn,fn_ref, "B", name["B"], name_ref["B"] ,ranges_ref["B"])
#plot on the same canvas both original and reference files
#gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","first")

# now shift the baselines and plot on same canvas
# when you plot the function by just shifting to common baseline
print"starting shfiting baseline"
gcs_plot.shiftGC_baseline(fn, fn_ref, "B")
#gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","second")

# scale your Ar peak to fit the org
# do not run setPeak again , just modify values only for reference not for original
gcs_plot.scaleGC_first_peak(fn, fn_ref, "B")
gcs_plot.evaluate_integral(fn, fn_ref, "B")
#gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","third")

# to shift along the x axis and then evaluate integral and plot on same plot
gcs_plot.shiftGC_x(fn,fn_ref,"B")
gcs_plot.setPeak_positions_ref(fn_ref,"B",ranges_ref["B"])
gcs_plot.evaluate_integral(fn, fn_ref, "B")
gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","fourth_new")

# store values of peak and valleys for both reference and original plots
#    for column in ("B","C"):
#        gcs.plotDrift(column)
