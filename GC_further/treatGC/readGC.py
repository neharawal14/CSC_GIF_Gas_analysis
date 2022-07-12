'''
Created on 21 Nov 2016

@author: kkuzn
'''
import sys
import time
import argparse
import GC.GC as GC
import GC.GC_plots as GC_plots
# program to plot one graphs on one canvas


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--input_org',type=str, required=True, help="input file name org")
parser.add_argument('-r', '--input_ref',type=str, required=True, help="input file name ref")
args = parser.parse_args()

input_file_name_org = args.input_org
input_file_name_ref = args.input_ref
print("input file name : ",input_file_name_org)
print("input ref file name : ",input_file_name_ref)


#fn =  "CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018_0001.AXY"
# creating an object to study the plots of input file
# this object will be used to open the file and read and do all other operations

#Defines the names to be used for each peak
name={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon+CF_{4}","CO_{2}"],"C":["Argon","CO_{2}"]}
#defines the user range to be used to narrow the search for peaks
ranges={"B":[0.2,0.8],"C":[0.1,0.5]}

#output file name for the root file
output_root_file_org = "Plot_org.root"
gcs_org = GC.GSset(input_file_name_org, output_root_file_org)
print"fnames : ", input_file_name_org
print "running for file inside"
column="B" 
print" calling Set Peak valley  function"
gcs_org.setPeak(input_file_name_org,"B",name["B"],ranges["B"])
# print" calling get Peak valley  function not useful now"
print"calling Multi plot function now"
gcs_org.plotMulti(input_file_name_org,"B")
print"done with Multi plot function now"

output_root_file_ref = "Plot_ref.root"
gcs_ref = GC.GSset(input_file_name_ref, output_root_file_ref)
print"fnames ref: ", input_file_name_ref
print "running for file inside"
column="B" 
print" calling Set Peak valley  function"
gcs_ref.setPeak(input_file_name_ref,"B",name["B"],ranges["B"])
# print" calling get Peak valley  function not useful now"
print"calling Multi plot function now"
gcs_ref.plotMulti(input_file_name_ref,"B")
print"done with Multi plot function now"

gc_object = GC_plots.plots(gcs_org, gcs_ref)
gc_object.plot_org_ref_new(gcs_org, gcs_ref,"output_first.root")
gc_object.shiftGC_baseline(gcs_org, gcs_ref,"B")
gc_object.shiftGC_baseline_CO2(gcs_org, gcs_ref,"B")

gcs_org.initialize_plot_Multi()
gcs_ref.initialize_plot_Multi()
gcs_org.plotMulti(input_file_name_org,"B")
gcs_ref.plotMulti(input_file_name_ref,"B")
gc_object.plot_org_ref_new(gcs_org, gcs_ref,"output_second.root")

#gcs_org.delete_lists()
#gcs_ref.delete_lists()

        #print"error in file read"
          #
          #fn_ref =  "CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY"
          ## for plotting reference curve GC individually    
          #gcs_ref = GC.GSset(fn_ref, dir, verb, pdfname)
          #name_ref={"A":["1","2","3","4","5","6","7","8","9","10"],"B":["Argon","CO_{2}"],"C":["Argon","CO_{2}"]}
          #ranges_ref={"B":[0.2,0.8],"C":[0.1,0.5]}
          #fnames_ref = sorted(gcs.gcsets.keys())
          #print "running for ref file : printing function ref " , fn_ref
          #print "function reference fnames_ref ", fnames_ref
          ##for fn_ref in fnames_ref:
          #print "reference files fn_ref  ", fn_ref
          #print "running for ref file inside"
          #
          #column = "B"
          #print" calling set Peak  function"
          #gcs_ref.setPeak(fn_ref,column,name_ref[column],ranges_ref[column])
          #print" calling get Peak valley  function"
          ##gcs_ref.getPeakValley(fn_ref,column,name_ref[column])
          #print" calling multi plot function"
          #gcs_ref.plotMulti(fn_ref,column)
          #print" done with  multi plot function"
          #
          ##initialize to plot two curve from original and reference files on the same canvas
          ##from here on the function that will be first called is stored in GC_plots
          #gcs_plot = GC_plots.plots(fn, dir, verb, pdfname,fn_ref, dir, verb, pdfname)
          #gcs_plot.setPeak(fn,fn_ref, "B", name["B"], name_ref["B"] ,ranges_ref["B"])
          #                 
          #gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","first")
          ##plot on the same canvas both original and reference files #gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","first")
          #            #
          ## now shift the baselines and plot on same canvas
          ## when you plot the function by just shifting to common baseline
          #print"starting shfiting baseline"
          ###gcs_plot.setPeak(fn,fn_ref, "B", name["B"], name_ref["B"] ,ranges_ref["B"])
          ###gcs_plot.evaluate_integral(fn, fn_ref,"B")
          #gcs_plot.shiftGC_baseline(fn, fn_ref, "B")
          #gcs_plot.shiftGC_baseline_CO2(fn, fn_ref, "B")
          #gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","first")
          #        #
          #        ##scale your Ar peak to fit the org
          #        ## ifnot run setPeak again , just modify values only for reference not for original
          #        #gcs_plot.scaleGC_first_peak(fn, fn_ref, "B")
          #        #gcs_plot.evaluate_integral(fn, fn_ref, "B")
          #        ##gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","third")
          #        #
          #        ### to shift along the x axis and then evaluate integral and plot on same plot
          #        #gcs_plot.shiftGC_x(fn,fn_ref,"B")
          #        #gcs_plot.setPeak_positions_ref(fn_ref,"B",ranges_ref["B"], name_ref["B"])
          #        #gcs_plot.evaluate_integral(fn, fn_ref, "B")
          #        #gcs_plot.plot_org_ref(fn, "B", fn_ref, "B","fourth")
          #
          #
          # ## store values of peak and valleys for both reference and original plots
          # ##    for column in ("B","C"):
          # ##        gcs.plotDrift(column)
          #