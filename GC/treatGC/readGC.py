'''
Created on 21 Nov 2016

@author: kkuzn
'''
import sys
import getopt

import GC.GC as GC

inputFile=""

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:d:o:vh",["filelist=", "dir="])
except getopt.GetoptError:
    # print help information and exit:
    print ' enter file name'
    sys.exit()

verb = False
dir  = False
pdfname=""
fn=""

for o,a in opts:
    if o=='-f':
        print "proceeding for files", a
        fn = a
    if o=='-d':        
        print "proceeding for directory", a
        fn = a    
        dir = True
    if o=='-o':        
        print "output pdf/root files", a
        pdfname = a    
    if o=="-v":
        verb = True
    if o=="-h":
        print "here"
        exit()

print(len(fn))
if len(fn)==0:
    #print "please provide file (-f filename) or directory (-d dirname) names"
    gcs = GC.GSset(fn, False, False, "")
    #gcs.addGCs("154_CSC_Mixer_0015.AXY")
    #gcs.scaleGCx("154_CSC_Mixer_0015.AXY", "A", 1.19)
    #gcs.shiftGC("154_CSC_Mixer_0015.AXY", "A", 0.334-0.282)
    for column in ("A"):
        gcs.plotGC(fn, column, True)
    #gcs.plotGC("154_CSC_Mixer_0015.AXY", "A", False, "CSC_28Oct16_4lhfresh_P5onColdDirect_3_0009.AXY", "B")
    gcs.setPeak(fn,"A","this one")
    gcs.plotPeak(fn, column)
    
    h=raw_input()

else:
    
    gcs = GC.GSset(fn, dir, verb, pdfname)

    #Defines the names to be used for each peak
    name={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon","CF_{4}","CO_{2}"],"C":["Argon","CO_{2}"]}

    #defines the user range to be used to narrow the search for peaks
    ranges={"B":[0.2,0.8],"C":[0.1,0.5]}
    fnames = sorted(gcs.gcsets.keys())
    for fn in fnames:
      for column in ("B", "C"):
        print("column : ", column)
      for fn in fnames:
        for column in("B","C"):
            gcs.setPeak(fn,column,name[column],ranges[column])
            gcs.plotMulti(fn,column)

    for column in ("B","C"):
        gcs.plotDrift(column)
                

