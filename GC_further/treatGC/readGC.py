'''
Created on 21 Nov 2016

@author: kkuzn
'''
import sys
import getopt

import GC.GC as GC
import GC.GC_plots as GC_plots
#another program to plot two graphs on same canvas
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

#print(len(fn))
#print(len(fn_ref))
#if len(fn)==0:
#    #print "please provide file (-f filename) or directory (-d dirname) names"
#    gcs = GC.GSset(fn, False, False, "")
#    #gcs.addGCs("154_CSC_Mixer_0015.AXY")
#    #gcs.scaleGCx("154_CSC_Mixer_0015.AXY", "A", 1.19)
#    #gcs.shiftGC("154_CSC_Mixer_0015.AXY", "A", 0.334-0.282)
#    for column in ("A"):
#        gcs.plotGC(fn, column, True)
#    #gcs.plotGC("154_CSC_Mixer_0015.AXY", "A", False, "CSC_28Oct16_4lhfresh_P5onColdDirect_3_0009.AXY", "B")
#    gcs.setPeak(fn,"A","this one")
#    gcs.plotPeak(fn, column)
#    
#    h=raw_input()
#
#else:


#print " fn file: ",fn
#print " reference file initially : ",fn_ref

gcs = GC.GSset(fn, dir, verb, pdfname)

#Defines the names to be used for each peak
name={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon","CF_{4}","CO_{2}"],"C":["Argon","CO_{2}"]}

#defines the user range to be used to narrow the search for peaks
ranges={"B":[0.2,0.8],"C":[0.1,0.5]}
fnames = sorted(gcs.gcsets.keys())

#print "function  fnames ", fnames
#for fn in fnames:
#print "running the gcs original file"

for fn in fnames:
   print " files fn :  ",fn
   print "running for file inside"
   for column in ("B", "C"):
       print("column : ", column)
#      for fn in fnames:
   for column in("B"):
       print" calling Set Peak valley  function"
       gcs.setPeak(fn,column,name[column],ranges[column])
       print" calling get Peak valley  function not useful now"
       gcs.getPeakValley(fn,column,name[column])
       print "calling Multi plot function now"
       gcs.plotMulti(fn,column)
       print "done with Multi plot function now"

   # run same over refrence files
#if len(fn_ref)==0:
#    #print "please provide file (-f filename) or directory (-d dirname) names"
#    gcs_ref = GC.GSset(fn_ref, False, False, "")
#    #gcs.addGCs("154_CSC_Mixer_0015.AXY")
#    #gcs.scaleGCx("154_CSC_Mixer_0015.AXY", "A", 1.19)
#    #gcs.shiftGC("154_CSC_Mixer_0015.AXY", "A", 0.334-0.282)
#    for column in ("A"):
#        gcs_ref.plotGC(fn_ref, column, True)
#    #gcs.plotGC("154_CSC_Mixer_0015.AXY", "A", False, "CSC_28Oct16_4lhfresh_P5onColdDirect_3_0009.AXY", "B")
#    gcs_ref.setPeak(fn_ref,"A","this one")
#    gcs_ref.plotPeak(fn_ref, column)
#    
#    h_ref=raw_input()
#
#else:
    
gcs_ref = GC.GSset(fn_ref, dir, verb, pdfname)

#Defines the names to be used for each peak
name_ref={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon","CF_{4}","CO_{2}"],"C":["Argon","CO_{2}"]}

#defines the user range to be used to narrow the search for peaks
ranges_ref={"B":[0.2,0.8],"C":[0.1,0.5]}
#fnames_ref = sorted(gcs.gcsets.keys())
#print "running for ref file : printing function ref " , fn_ref
#print "function reference fnames_ref ", fnames_ref
#for fn_ref in fnames_ref:
   #print "reference files fn_ref  ", fn_ref
   #print "running for ref file inside"
#      for column in ("B","C"):
#        print("column : ", column)
#      for fn_ref in fnames_ref :

for column in("B"):
    print" calling set Peak  function"
    gcs_ref.setPeak(fn_ref,column,name_ref[column],ranges_ref[column])
    print" calling get Peak valley  function"
    gcs_ref.getPeakValley(fn_ref,column,name_ref[column])
    print" calling multi plot function"
    gcs_ref.plotMulti(fn_ref,column)
    print" done with  multi plot function"

#scale_peak_y = gcs.first_peak_x_value/gcs_ref.first_peak_x_value
#scale_valley_x = gcs.first_valley_x_value/gcs_ref.first_valley_x_value
#print "scale factor x and y: ", scale_peak_y, " ", scale_valley_x 
   # once we have reference peak and other peaks information
   # find scale factors
   #program to modify the y values for the reference file, lets call another program GC/ref_modify.py
#gcs_ref.scaleGCy(fn_ref,"B",scale_peak_y)
#gcs_ref.scaleGCx(fn_ref,"B",scale_valley_x)
#print "after scaling things"
#gcs_ref.plotMulti(fn_ref,column)

# program for both the functions together
print "plotting the functions fn and fn_org"
gcs_plot = GC_plots.plots(fn, dir, verb, pdfname,fn_ref, dir, verb, pdfname)

#print(fn)
#print(fn_ref)

gcs_plot.setPeak(fn,fn_ref, "B", name["B"], name_ref["B"] ,ranges_ref["B"])
print"plot both the functions again"
#gcs_plot.plot_org_ref(fn, "B", fn_ref, "B", "first")

#gcs_plot.plot_org_ref(fn,"B", fn_ref, "B")
#plot on the same canvas both original and reference files

# now shift the baselines and plot on same canvas
print"starting shfiting baseline"
gcs_plot.shiftGC_baseline(fn, fn_ref, "B")
#gcs_plot.scaleGC_first_peak(fn, fn_ref, "B")
gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","second")


# store values of peak and valleys for both reference and original plots
   # after shifting now plot on the same canvas , make some adjustment in plotMulti program and make a new program
#    for column in ("B","C"):
#        gcs.plotDrift(column)
