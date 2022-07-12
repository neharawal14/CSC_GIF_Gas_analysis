'''
Created on 21 Nov 2016

@author: kkuzn
'''
from ROOT import gStyle
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TGraph
from ROOT import TFile
from ROOT import gROOT
from ROOT import TMultiGraph
from ROOT import TF1
from ROOT import TLine
import ROOT
import math
import GCdata

gROOT.SetBatch(1)
 

class plots(object):
    '''
    classdocs
    '''

    # read files and make plots send two files and directories flag to initialize

    def __init__(self, org_obj, ref_obj):
        '''
        Constructor
        '''
        print"obj integral ",org_obj.integral
        #print"obj integral "
        np_org = org_obj.graphs.GetN()
        x_org  = org_obj.graphs.GetX()
        y_org  = org_obj.graphs.GetY()

        np_ref = ref_obj.graphs.GetN()
        x_ref  = ref_obj.graphs.GetX()
        y_ref  = ref_obj.graphs.GetY()

        npn_org = org_obj.avgraphs.GetN()
        xn_org  = org_obj.avgraphs.GetX()
        yn_org  = org_obj.avgraphs.GetY()

        npn_ref = ref_obj.avgraphs.GetN()
        xn_ref  = ref_obj.avgraphs.GetX()
        yn_ref  = ref_obj.avgraphs.GetY()

        print"number of points ", np_org
        self.c2_cmp=TCanvas("c2_cmp","canvases cmp log",1200,800)     
        self.canvases_cmp = TCanvas("canvases_cmp", "canvas cmp", 1200, 800)

        self.comparison_plot = TMultiGraph()
        self.comparison_log_plot = TMultiGraph()
       #self.colours = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
       #self.colours_ref = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
       #self.ncolours = 6

       #read and normalize both the files 
#        self.readGCs(input_file_org, input_file_ref)
#        self.normalize(input_file_org, input_file_ref)
    def colour_scheme_plot(self, org_obj, ref_obj):

        for i in range(org_obj.npPeaks):
             org_obj.gPeak[i].SetMarkerColor(org_obj.colours[i]);org_obj.gnPeak[i].SetMarkerColor(org_obj.colours[i])
             org_obj.gPeak[i].SetMarkerSize(2);org_obj.gnPeak[i].SetMarkerSize(2)
             org_obj.gPeak[i].SetMarkerStyle(8);org_obj.gnPeak[i].SetMarkerStyle(8)    
                    #
        for i in range(ref_obj.npPeaks):
             ref_obj.gPeak[i].SetMarkerColor(ref_obj.colours[i]);ref_obj.gnPeak[i].SetMarkerColor(org_ref.colours[i])
             ref_obj.gPeak[i].SetMarkerSize(2);ref_obj.gnPeak[i].SetMarkerSize(2)
             ref_obj.gPeak[i].SetMarkerStyle(8);ref_obj.gnPeak[i].SetMarkerStyle(8)    

        for i in range(org_obj.npWidth):
             iV_org=org_obj.width[i][2]
             print"the valley points final org",org_obj.width[i][2]
             org_obj.gWidth.SetPoint(i,x_org[iV_org],y_org[iV_org]);org_obj.gnWidth.SetPoint(i,xn_org[iV_org],yn_org[iV_org])
        org_obj.gWidth.SetMarkerColor(3);org_obj.gnWidth.SetMarkerColor(3)
        org_obj.gWidth.SetMarkerSize(2);org_obj.gnWidth.SetMarkerSize(2)
        org_obj.gWidth.SetMarkerStyle(8);org_obj.gnWidth.SetMarkerStyle(8)
 
        for i in range(ref_obj.npWidth):
             iV_ref=ref_obj.width[i][2]
             print"the valley points final org",ref_obj.width[i][2]
             ref_obj.gWidth.SetPoint(i,x_ref[iV_ref],y_ref[iV_ref]);ref_obj.gnWidth.SetPoint(i,xn_ref[iV_ref],yn_ref[iV_ref])
        ref_obj.gWidth.SetMarkerColor(28);ref_obj.gnWidth.SetMarkerColor(28)
        ref_obj.gWidth.SetMarkerSize(2);ref_obj.gnWidth.SetMarkerSize(2)
        ref_obj.gWidth.SetMarkerStyle(8);ref_obj.gnWidth.SetMarkerStyle(8)


    def plot_org_ref_new(self, org_obj, ref_obj, output_file_name):

        self.rfile = TFile(output_file_name,"RECREATE")
        self.comparison_plot.Add(org_obj.multi, "pl")
        self.comparison_plot.Add(ref_obj.multi, "pl")

        leg_cmp= TLegend(0.5,0.65,0.88,0.85)

        for i in range(org_obj.npPeaks):
            leg_cmp.AddEntry(org_obj.gPeak[i],org_obj.peakNames[i]+": "+org_obj.integral+" #pm ^{"+org_obj.integral_error[0]+"}_{"+org_obj.integral_error[1]+"} | "+org_obj.percentage+" #pm ^{"+org_obj.perc_error[0]+"}_{"+org_obj.perc_error[1]+"}%","p")
#            leg_cmp.AddEntry(org_obj.gPeak[i],org_obj.peakNames[i]+": "+org_obj.integral+" | "+org_obj.percentage+"%","p")
        for i in range(ref_obj.npPeaks):
            #leg_cmp.AddEntry(ref_obj.gPeak[i],ref_obj.peakNames[i]+": "+ref_obj.integral+" | "+obj.percentage+"%","p")
            leg_cmp.AddEntry(ref_obj.gPeak[i],ref_obj.peakNames[i]+": "+ref_obj.integral+" #pm ^{"+ref_obj.integral_error[0]+"}_{"+ref_obj.integral_error[1]+"} | "+ref_obj.percentage+" #pm ^{"+ref_obj.perc_error[0]+"}_{"+ref_obj.perc_error[1]+"}%","p")
           

        if self.rfile.GetDirectory("GC_cmp"):  print"yes dir GC_cmp"
        if not self.rfile.GetDirectory("GC_cmp"): self.rfile.mkdir("GC_cmp") ; print"makign dir GC_cmp"
        self.rfile.cd("GC_cmp")

        self.canvases_cmp.cd()
        self.comparison_plot.Draw("ap") 
        
        #Set range to zoom in on peaks for columns B and C, could probably be changed to use the user defined x range
        self.comparison_plot.GetXaxis().SetRangeUser(0.2,0.8)

        self.comparison_plot.GetXaxis().SetTitle("Time (sec)")
        self.comparison_plot.GetYaxis().SetTitle("Signal (#muV)")
        self.comparison_plot.GetYaxis().SetTitleOffset(1.2)
        leg_cmp.Draw()
        self.canvases_cmp.Write()
        
        self.c2_cmp.cd()
        self.c2_cmp.SetLogy()
        self.comparison_log_plot.Add(org_obj.logMulti, "p")
        self.comparison_log_plot.Add(ref_obj.logMulti, "p")
        self.comparison_log_plot.Draw("a") 
        self.comparison_log_plot.GetXaxis().SetRangeUser(0.2,0.8)
        
        self.comparison_log_plot.GetXaxis().SetTitle("Time (sec)")
        self.comparison_log_plot.GetYaxis().SetTitle("Signal (#muV)")
        self.comparison_log_plot.GetYaxis().SetTitleOffset(1.2)
        leg_cmp.Draw()
        self.c2_cmp.Write()
        self.rfile.Close()
   
    def shiftGC_baseline(self, org_obj,ref_obj, column):
          # to evaulate the value to shift 
          # first peak and first valley
         peak_org=org_obj.peaks[0][2]
         peak_ref=org_obj.peaks[0][2]
         valley_org=org_obj.width[0][2]
         valley_ref=org_obj.width[0][2]

         second_valley_ref = org_obj.width[2][2]
         second_valley_org = org_obj.width[2][2]

         third_valley_ref = org_obj.width[3][2]
         third_valley_org = org_obj.width[3][2]


         # values of graphs 
         x_org,y_org,np_org=org_obj.graphs.GetX(),org_obj.graphs.GetY(),org_obj.graphs.GetN()
         x_ref,y_ref,np_ref=ref_obj.graphs.GetX(),ref_obj.graphs.GetY(),ref_obj.graphs.GetN()

         # values of avgraphs
         xn_org,yn_org,npn_org=org_obj.avgraphs.GetX(), org_obj.avgraphs.GetY(),org_obj.avgraphs.GetN()
         xn_ref,yn_ref,npn_ref=ref_obj.avgraphs.GetX(),ref_obj.avgraphs.GetY(),ref_obj.avgraphs.GetN()
 
         shift_valley_org_graphs = y_org[valley_org] - 500.0
         shift_valley_ref_graphs = y_ref[valley_ref] - 500.0

         shift_valley_org_avgraphs = yn_org[valley_org] - 500.0
         shift_valley_ref_avgraphs = yn_ref[valley_ref] - 500.0
 
         print "************************************ all the valleys ( i, x, y )**********"
         print " first : ({}, {}, {})".format(valley_org, x_org[valley_org] , y_org[valley_org])
         print " second  : ({}, {}, {})".format(second_valley_org, x_org[second_valley_org] , y_org[second_valley_org])
         print " third  : ({}, {}, {})".format(third_valley_org, x_org[third_valley_org] , y_org[third_valley_org])
         print "************************************ printed all the valleys ( i, x, y )**********"
         
         print " np in plot org_ref function org graph ",np_org
         print " np in plot org_ref function ref graph ",np_ref

         print"shift valley org graph" ,shift_valley_org_graphs
         print"shift valley ref graph", shift_valley_ref_graphs


         print " np in plot org_ref function org ",npn_org
         print " np in plot org_ref function ref ",npn_ref

         print"shift valley org avgraph" ,shift_valley_org_avgraphs
         print"shift valley ref avgraph", shift_valley_ref_avgraphs

         print" printing x[i] - y[i] values  graphs org before shifting "
         for i in range(2000,2010):
          print "({},{})".format(x_org[i], y_org[i])
         print" printing x[i] - y[i] values graphs ref before shifting "
         for i in range(2000,2010):
          print "({},{})".format(x_ref[i], y_ref[i])
 
         print" printing x[i] - y[i] values avg graphs org before shifting graphs"
         for i in range(npn_org):
          print "({},{})".format(xn_org[i], yn_org[i])
         print" printing x[i] - y[i] values avg graphs ref before shifting graphs"
         for i in range(2000,2010):
          print "({},{})".format(xn_ref[i], yn_ref[i])
 

         print" printing x[i] - y[i] values between first valley and second valley graphs org before shifting"
         for i in range(valley_org, second_valley_org):
          print "({},{})".format(x_org[i], y_org[i])
         print" printing x[i] - y[i] values graphs ref between first valley and second valley before shifting"
         for i in range(valley_ref, second_valley_ref):
          print "({},{})".format(x_ref[i], y_ref[i])
 
         # since yn_org  already declared from before and so it is fine to use it here directly
         self.shiftGraph(column,ref_obj, shift_valley_org_graphs, shift_valley_org_avgraphs)
         self.shiftGraph(column,ref_obj, shift_valley_ref_graphs, shift_valley_ref_avgraphs)


    def shiftGC_baseline_CO2(self, org_obj,ref_obj, column):
                   # to evaulate the value to shift 
          # first peak and first valley
         peak_org  =org_obj.peaks[0][2]
         peak_ref  =ref_obj.peaks[0][2]
         valley_org=org_obj.width[0][2]
         valley_ref=ref_obj.width[0][2]

         second_valley_ref = org_obj.width[2][2]
         second_valley_org = ref_obj.width[2][2]

         third_valley_ref = org_obj.width[3][2]
         third_valley_org = ref_obj.width[3][2]

         # values of graphs 
         x_org,y_org,np_org=org_obj.graphs.GetX(),org_obj.graphs.GetY(),org_obj.graphs.GetN()
         x_ref,y_ref,np_ref=ref_obj.graphs.GetX(),ref_obj.graphs.GetY(),ref_obj.graphs.GetN()

         # values of avgraphs
         xn_org,yn_org,npn_org=org_obj.avgraphs.GetX(), org_obj.avgraphs.GetY(),org_obj.avgraphs.GetN()
         xn_ref,yn_ref,npn_ref=ref_obj.avgraphs.GetX(),ref_obj.avgraphs.GetY(),ref_obj.avgraphs.GetN()
 

         shift_valley_CO2_org_graphs = y_org[second_valley_org] - 500.0
         shift_valley_CO2_ref_graphs = y_ref[second_valley_ref] - 500.0

         shift_valley_CO2_org_avgraphs = yn_org[second_valley_org] - 500.0
         shift_valley_CO2_ref_avgraphs = yn_ref[second_valley_ref] - 500.0

         print "************************************ all the valleys ( i, x, y )**********"
         print " first : ({}, {}, {})".format(valley_org, x_org[valley_org] , y_org[valley_org])
         print " second  : ({}, {}, {})".format(second_valley_org, x_org[second_valley_org] , y_org[second_valley_org])
         print " third  : ({}, {}, {})".format(third_valley_org, x_org[third_valley_org] , y_org[third_valley_org])
         print "************************************ printed all the valleys ( i, x, y )**********"
         
         print" printing x[i] - y[i] values between first valley and second valley graphs org before shifting"
         for i in range(valley_org, second_valley_org):
          print "({},{})".format(x_org[i], y_org[i])
         print" printing x[i] - y[i] values graphs ref between first valley and second valley before shifting"
         for i in range(valley_ref, second_valley_ref):
          print "({},{})".format(x_ref[i], y_ref[i])
 
          # since yn_org  already declared from before and so it is fine to use it here directly  for CO2
         self.shiftGraph_CO2(column, ref_obj, shift_valley_CO2_org_graphs, shift_valley_CO2_org_avgraphs, second_valley_org, third_valley_org)
         self.shiftGraph_CO2(column, ref_obj, shift_valley_CO2_ref_graphs, shift_valley_CO2_ref_avgraphs, second_valley_ref, third_valley_ref)
 
    def shiftGraph(self, column, ref_obj, shift_graph, shift_avgraph):
        # shifting also the graph points
        np_graph  = ref_obj.graphs.GetN()
        x_graph   = ref_obj.graphs.GetX()
        y_graph   = ref_obj.graphs.GetY()
        print "shift value ", shift_graph
        print "number of values",np_graph
        print "column",column
        y_shifted_graph = []
        for i in range(2000,2010):
             print "i -  x - y values ({},{},{}) ".format(i, x_graph[i], y_graph[i])
        print("*********y shifted values *******")
        for i in range(0,np_graph):                
             y_shifted_graph = y_graph[i]-shift_graph
             print(y_shifted_graph, " type x ",x_graph[i], " type y ",y_shifted_graph)
             ref_obj.graphs_new.SetPoint(i,x_graph[i],y_shifted_graph)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting graphs ({},{},{}) ".format(i, x_graph[i], y_shifted_graph)
        print " after shifting number of values graphs", np_graph
 
        np  = ref_obj.avgraphs.GetN()
        x   = ref_obj.avgraphs.GetX()
        y   = ref_obj.avgraphs.GetY()
        print "shift value ", shift_avgraph
        print "number of values",np
        print "column",column
        print " average graph values before shifting " 
        #for i in range(2000,2010):
        #     print "i -  x - y avgraphs values before shifting to common baseline ({},{},{}) ".format(i, x[i], y[i])
        y_shifted = []
        for i in range (0,np): 
             y_shifted = y[i]-shift_avgraph
             ref_obj.avgraphs_new.SetPoint(i,x[i],y_shifted)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting avgraphs ({},{},{}) ".format(i, x[i], y_shifted)
        
        print" after shifting number of values avgraphs", np

      

# this function is to scale the Ar peak along y axis to match with the original curve
#peak_org_graphs , peak_org_avgraphs: peak point value for the original curve
#base_org_graphs , base_org_avgraphs : valley point value for the original curve
#peak_ref : peak point for the reference curve
#base_ref : valley point for the ref curve
#second_valley_ref_point : second valley point for the ref curve
    def shiftGraph_CO2(self, column,ref_obj, shift_graph, shift_avgraph, second_valley, third_valley):
        np  = ref_obj.avgraphs.GetN()
        x   = ref_obj.avgraphs.GetX()
        y   = ref_obj.avgraphs.GetY()
        print "shift value ", shift_avgraph
        print "number of values",np
        print "column",column
        print " average graph values before shifting " 
#        for i in range(np):
#           print "check here {},{} ".format(x[i] , y[i])

        for i in range(2000,2010):
             print "i -  x - y avgraphs values before shifting to common baseline ({},{},{}) ".format(i, x[i], y[i])
             y_shifted = []
        for i in range (0,np): 
           if i in range(second_valley, np):
             y_shifted = y[i]-shift_avgraph
             ref_obj.avgraphs_new.SetPoint(i,x[i],y_shifted)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting avgraphs ({},{},{}) ".format(i, x[i], y_shifted)

           else :
              y_shifted = y[i]
              ref_obj.avgraphs_new.SetPoint(i,x[i],y_shifted)
        
        print" after shifting number of values avgraphs", np

        # shifting also the graph points
        np_graph  = ref_obj.graphs.GetN()
        x_graph   = ref_obj.graphs.GetX()
        y_graph   = ref_obj.graphs.GetY()
        print "shift value ", shift_graph
        print "number of values",np_graph
        print "column",column

        y_shifted_graph = []
        for i in range(2000,2010):
             print "i -  x - y values ({},{},{}) ".format(i, x_graph[i], y_graph[i])
        for i in range (np_graph):                
           if i in range(second_valley, np_graph):
             y_shifted_graph = y_graph[i]-shift_graph
             ref_obj.graphs.SetPoint(i,x_graph[i],y_shifted_graph)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting graphs ({},{},{}) ".format(i, x_graph[i], y_shifted_graph)

           else : 
             y_shifted = y_graph[i]
             ref_obj.graphs.SetPoint(i,x[i],y_shifted)

        print " after shifting number of values graphs", np_graph
 
                    #    def initialize_plot(self, output_file_name): 
                    #self.peaks_org=[] self.peakNames_org=[] self.valleys_org=[] self.flat_org=[] self.flaterror_org=[] self.width_org=[] self.baselines_org=[] self.width_ref=[] self.baselines_ref=[] self.gPeak_org = [] #Used to overlay on raw GC data self.gnPeak_org= [] #Used to overlay on normalized GC data self.gPeak_ref = [] #Used to overlay on raw GC data self.gnPeak_ref= [] #Used to overlay on normalized GC data self.logMulti_org=TMultiGraph() self.logMulti_ref=TMultiGraph() self.logMulti_all= TMultiGraph() self.multi_org = TMultiGraph() self.multi_ref = TMultiGraph() self.multi_all= TMultiGraph() self.gWidth_org = TGraph() #Used to overlay on raw GC data self.gWidth_ref = TGraph() #Used to overlay on raw GC data self.gnWidth_org = TGraph() # Used to overlay on normalized GC data self.gnWidth_ref = TGraph() # Used to overlay on normalized GC data self.output=output_file_name self.rfile = TFile(self.output,"RECREATE") self.canvases_cmp = TCanvas(canvases_cmp, "canvas cmp", 1200, 800) self.c2_cmp=TCanvas("c2_cmp","canvases cmp log",1200,800) def readGCs(self,file_name_org, file_name_ref): # checking if the input file exists or not print "input file org name in readGC cmp ", file_name_org print "input file ref name in readGC cmp ", file_name_ref if ".AXY" in file_name_org: try: with open(file_name_org, 'r') as f: read_data = f.readlines() f.closed except: print "can't open file ", file_name_org, "exiting..." exit() N = len(read_data[0].split(", ")) if(N<=1): print "less than two column in file ", file_name_org, ", exiting..." exit() if(N>4): print "more than tree data columns in file ", file_name_org, ", will do only three of them..." N=4 # just setting the axis range and title for column B plots self.ranges_org=[100000000000000, -100000000000000] self.graphs_org.SetName("B") self.graphs_org.SetTitle("B") # what the new graph is for ?  self.graphs_org.SetMarkerStyle(20) self.graphs_org.SetMarkerSize(0.5) for datastring in read_data: dset = datastring.split(", ") # we are only reading for column B , so avoiding to do anything for column C np_org  = self.graphs_org.GetN() val = float(dset[2]) self.graphs_org.SetPoint(np_org, float(dset[0]), val) if(val>self.ranges_org[1]): self.ranges_org[1] = val if(val<self.ranges_org[0]): self.ranges_org[0] = val column_names ="B" print "read ", file_name_org, " for columns ", " ".join(cn for cn in column_names) if ".AXY" in file_name_ref: try: with open(file_name_ref, 'r') as f: read_data = f.readlines() f.closed except: print "can't open file ", file_name_ref, "exiting..." exit() N = len(read_data[0].split(", ")) if(N<=1): print "less than two column in file ", file_name_ref, ", exiting..." exit() if(N>4): print "more than tree data columns in file ", file_name_ref, ", will do only three of them..." N=4 # just setting the axis range and title for column B plots self.ranges_ref=[100000000000000, -100000000000000] self.graphs_ref.SetName("B") self.graphs_ref.SetTitle("B") # what the new graph is for ?  self.graphs_ref.SetMarkerStyle(20) self.graphs_ref.SetMarkerSize(0.5) for datastring in read_data: dset = datastring.split(", ") # we are only reading for column B , so avoiding to do anything for column C np_ref  = self.graphs_ref.GetN() val = float(dset[2]) self.graphs_ref.SetPoint(np_ref, float(dset[0]), val) if(val>self.ranges_ref[1]): self.ranges_ref[1] = val if(val<self.ranges_ref[0]): self.ranges_ref[0] = val # reading all the data points for the file is done #normalize the function now creating an avg graph between the range 0.2, 0.8 column_names ="B" print "read ", file_name_ref, " for columns ", " ".join(cn for cn in column_names) def normalize(self,column,x_range): if not(column in "B"): print "can't find graph ",column, "doing nothing" return ''' Set the most probable y value to 1000 so that there is an easier comparison between all the GC data ''' np_org = self.graphs_org.GetN() x_org  = self.graphs_org.GetX() y_org  = self.graphs_org.GetY() print "normalize function np values", np_org # for the moments lets not shift anything in avgraph y_list_org = [ y_org[i] for i in range(np_org) if x_range[0] <=  x[i] <= x_range[1]] #make a list of y values in the desired range self.yHisto_org = TH1F("y_org_value_B","",50000,min(y_list_org),max(y_list_org)) for i in range(len(y_list_org)):self.yHisto_org.Fill(y_list_org[i]) min_y2_org = self.yHisto_org.GetXaxis().GetBinCenter(self.yHisto_org.GetMaximumBin()) #Get most common y value #print ("minimum y value from which we are normalizing",min_y2) yshift_org = [y_org[i]-min_y2_org+1000 for i in range(np_org)] #Shift all y values to the required values # print " y shifted value over whole spectrum for avg graphs in normalize function " for i in range(np_org): self.avgraphs_org.SetPoint(i,x[i],yshift[i]) self.avgraphs_org.SetName(self.graphs_org.GetName()) np_ref = self.graphs_ref.GetN() x_ref  = self.graphs_ref.GetX() y_ref  = self.graphs_ref.GetY() print "normalize function np values", np_ref # for the moments lets not shift anything in avgraph y_list_ref = [ y_ref[i] for i in range(np_ref) if x_range[0] <=  x[i] <= x_range[1]] #make a list of y values in the desired range self.yHisto_ref = TH1F("y_ref_value_B","",50000,min(y_list_ref),max(y_list_ref)) for i in range(len(y_list_ref)):self.yHisto_ref.Fill(y_list_ref[i]) min_y2_ref = self.yHisto_ref.GetXaxis().GetBinCenter(self.yHisto_ref.GetMaximumBin()) #Get most common y value #print ("minimum y value from which we are normalizing",min_y2) yshift_ref = [y_ref[i]-min_y2_ref+1000 for i in range(np_ref)] #Shift all y values to the required values # print " y shifted value over whole spectrum for avg graphs in normalize function " for i in range(np_ref): self.avgraphs_ref.SetPoint(i,x[i],yshift[i]) self.avgraphs_ref.SetName(self.graphs_ref.GetName()) def setPeak(self, name, column, peakName,x_range): if not(name in self.input_file_org) or not(column in "B") : print "can't find ", name, ", column ", column, " in data; doing nothing" return if not(name in self.input_file_ref) or not(column in "B") : print "can't find ", name, ", column ", column, " in data; doing nothing" return print "Setting peaks for",name,"column",column self.normalize(column,x_range) #Set minimum point within range specified to 1000 self.setPeak_exact(column,x_range) #Set peaks self.getIntegral_modified(column) #Get the integrals of the peaks self.setPeakName(name,column,-1,peakName) #Set peak names that are specified def setPeak_exact(self, column,x_range): if not(column in "B"): print "can't find graph ",column, "doing nothing" return np_org = self.avgraphs_org.GetN() x_org  = self.avgraphs_org.GetX() y_org  = self.avgraphs_org.GetY() if type(x_range_org) != list or len(x_range_org) != 2:x_range=[0,5] y_list_org = [y_org[i] for i in range(np_org) if x_range[0] <= x_org[i] <= x_range[1]] #make list of y values in desired x range i_list_org = [i for i in range(np_org) if x_range[0] <= x_org[i] <= x_range[1]] self.yHisto_org=TH1F("y_org_value_B","",50,min(y_list_org),max(y_list_org)) for i in range(len(y_list_org)):self.yHisto_org.Fill(y_list_org[i]) #doubtful - not clear why last bin would be larger than anyone self.yHisto_org.SetBinContent(1,0) #remove the last bin because it is usually much larger than any other sp_org,ep_org=min(i_list_org),max(i_list_org) #Set start points based off x range base_y_org,base_x_org,base_i_org=y_org[sp],x_org[sp],sp_org #values to compare the size of peaks prev_y,prev_x = y_org[sp],x_org[sp] stdev_org=self.yHisto_org.GetRMS() print "Standard Deviation used",stdev_org threshold_org=0.1*stdev_org #anything above this threshold has the chance to be marked as a peak, value was choosen to fit data hill=False for i in range(sp_org,ep_org): nPeaks_org=len(self.peaks_org) nValleys_org=len(self.valleys_org) if not hill: #print "was not a hill in start" #the next y value after a peak should be lower than the peak if prev_y_org > y_org[i]: valPeak_org = prev_y_org #ignore any small bumps that are just noise if abs(valPeak_org - base_y_org) >= threshold_org: avgRise_org=0 atTop_org=True #check the average y value over the next 150 points, if it is a peak this should be lower than the peak height for j in range(150): avgRise_org+=y_org[i+j] if (valPeak_org < avgRise_org/float(j+1)): if (valPeak_org-y_org[i+j] < threshold_org): atTop=False break if (atTop): print "Found peak at",i-1,prev_x_org,prev_y_org,(prev_y_org-base_y_org)/stdev_org self.peaks_org.append([prev_x_org,prev_y_org,i-1]) self.peakNames_org.append(str(nPeaks_org)) #If no valleys have been found before a peak is found we use what ever the peaks height was compared to as the valley if (nValleys_org == 0):self.valleys_org.append([base_x_org,base_y_org,base_i_org]);print "Setting start valley at",base_i_org,base_x_org,base_y_org hill = True base_y_org=prev_y_org elif hill: #we want to set the valley at the lowest point possible if base_y > y_org[i]: base_y_org = y_org[i] base_x_org = x_org[i] base_i_org = i #the next y value after a valley should be higher than the valley elif prev_y_org < y_org[i]: valPeak_org = prev_y_org if abs(valPeak_org - base_y_org) >= threshold_org: avgFall_org=0 atBottom_org=True #check the average y value over the next 5 points, if it is a valley this should be higher than the valley height for j in range(5): avgFall_org+=y_org[i+j] if (valPeak_org > avgFall_org/float(j+1)): if (valPeak_org - y_org[i+j] < threshold_org): atBottom_org=False break if (atBottom_org): #The base values are better for marking valleys, not the prev values (not sure why) print "Found valley at",base_i_org,base_x_org,base_y_org,(prev_y_org-base_y_org)/stdev_org self.valleys_org.append([base_x_org,base_y_org,base_i_org]) hill=False prev_x_org=x_org[i] prev_y_org=y_org[i] #if we ended on a hill without finding a valley we take the last base values as the last valley if hill: self.valleys_org.append([base_x_org,base_y_org,base_i_org]);print "Setting end valley at",base_i_org,base_x_org,base_y_org #print("number of peaks and number of valleys for column :  ",column," before flatcheck") print(len(self.peaks_org)) print(len(self.valleys_org)) for i in range(len(self.peaks_org)): print"peak values : x and y", self.peaks_org[i][0]," ", self.peaks_org[i][1] for i in range(len(self.valleys_org)): print"peak values : x and y", self.valleys_org[i][0]," ", self.valleys_org[i][1] #move valleys as close to the peaks without getting on them flatcheck = 50 #amount of points that are considered in the linear fit for iV in range(len(self.peaks_org)): i_i,i_f = self.valleys_org[iV][2],self.valleys_org[iV+1][2] y_1,y_2 = self.valleys_org[iV][1],self.valleys_org[iV+1][1] i_peak = self.peaks_org[iV][2] # print "i peak and i final peak values here" , i_i, "  ", i_f, "peak values here ", i_peak prevflat=-1 fitslopeUp,fitslopeDo=-1,-1 #attempt at calculating uncertianty using physics analysis methods minChi2,minSlope=10**10,10**10 #debug variables for i in range(i_i,i_peak): # print "check values from first valley to the peak" if (y[i]-y_1 < threshold): #fit 50 points with a line and use chi2 and slope to determine how flat section is self.graphs.Fit('pol1','Q0','',x[i-flatcheck],x[i+flatcheck/5]) linearfit = self.graphs.GetFunction('pol1') if (minChi2 > linearfit.GetChisquare()/stdev):minChi2=linearfit.GetChisquare()/stdev if (minSlope > abs(linearfit.GetParameter(1))/stdev):minSlope=abs(linearfit.GetParameter(1))/stdev fiterror=linearfit.GetParError(1) #Uncertainty calculated by shifting slope up and down my the fit error if (abs(linearfit.GetParameter(1)+fiterror)/stdev < 0.5):fitslopeUp=[x[i],y[i],i] if (abs(linearfit.GetParameter(1)-fiterror)/stdev < 0.5):fitslopeDo=[x[i],y[i],i] if (abs(linearfit.GetParameter(1))/stdev < 0.5): #Slopes normalized to the stdev are choosen to be less than 0.5 to fit data fitslope=abs(linearfit.GetParameter(1))/stdev slopeErr=fiterror/stdev chi2=linearfit.GetChisquare()/stdev prevflat=[x[i],y[i],i] #                        print "prevflat value",prevflat #take the closest point to the peak #debug variables if not (minChi2==10**10 and minSlope==10**10): #print "Minimum Chi2:",minChi2 #print "Minimum Slope:",minSlope pass if (type(prevflat) != int): #print "Min ChiSquare:",minChi #print fitslope*stdev,fitslope,"+-",slopeErr,prevflat[0] #,"+-",abs(fitslopeUp[0]-fitslopeDo[0]) # print "previous flat appended in flat", prevflat self.flat.append(prevflat) self.flaterror.append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)]) #temporary Up and Down Uncertainty #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)]) minChi2,minSlope=10**10,10**10 prevflat,fitslopeUp,fitslopeDo=-1,-1,-1 for i in range(i_f,i_peak,-1): # print "check values from second valley to the peak" if (y[i]-y_2 < threshold):# and (i_f-i > flatcheck): avgY = [0.0,0.0] self.graphs.Fit('pol1','Q0','',x[i-flatcheck/5],x[i+flatcheck]) linearfit = self.graphs.GetFunction('pol1') if (minChi2 > linearfit.GetChisquare()/stdev):minChi2=linearfit.GetChisquare()/stdev if (minSlope > abs(linearfit.GetParameter(1))/stdev):minSlope=abs(linearfit.GetParameter(1))/stdev fiterror=linearfit.GetParError(1) if (abs(linearfit.GetParameter(1)+fiterror)/stdev < 0.005):fitslopeUp=[x[i],y[i],i] if (abs(linearfit.GetParameter(1)-fiterror)/stdev < 0.005):fitslopeDo=[x[i],y[i],i]
                    #                    if (abs(linearfit.GetParameter(1))/stdev < 0.005):
                    #                        fitslope=abs(linearfit.GetParameter(1))/stdev
                    #                        slopeErr=fiterror/stdev
                    #                        chi2=linearfit.GetChisquare()/stdev
                    #                        prevflat=[x[i],y[i],i]
                    #                      #  print "prev value from second valley to peak", prevflat        
                    #            if not (minChi2==10**10 and minSlope==10**10):
                    #                #print "Minimum Chi2:",minChi2
                    #                #print "Minimum Slope:",minSlope
                    #                pass
                    #            if (type(prevflat) != int):
                    #                #print "Min ChiSquare:",minChi
                    #                #print fitslope*stdev,fitslope,"+-",slopeErr,prevflat[0] #,"+-",abs(fitslopeUp[0]-fitslopeDo[0])
                    #               # print "previous flat value in last" ,prevflat
                    #                self.flat.append(prevflat)
                    #                self.flaterror.append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)])
                    #                #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)])
                    # 
                    #    def setPeakName(self,name,column,nPeak,peakName):
                    #        if nPeak == -1:
                    #            nPeak = len(self.peaks)
                    #            for i in range(nPeak):
                    #                self.peakNames[i] = peakName[i]
                    #
                    #
                    #
                    #
                    #    def plot_org_ref(self, name_org, column_org, name_ref, column_ref):
                    #        # def plotMulti(self,name,column):
                    #        # cname=name_org+"_cmp_"+name_ref+"_"+column_org
                    #        cname="cmp"+filename
                    #        if not column_org in "B":
                    #            print "can't find ", name_org, ", column ", column_org, " in data; doing nothing"
                    #            return
                    #       #Fill Peak points to be overlayed on the GC graphs
                    #        
                    #        print(" name ", name_org, " and other " , name_ref)
                    #        print("column name ", column_org, " and other " , column_ref)
                    #
                    #        npPeaks_ref = len(self.peaks_org) 
                    #        npPeaks_org = len(self.peaks_ref) 
                    #        x_org,y_org,np_org=self.graphs_org.GetX(),self.graphs_org.GetY(),self.graphs_org.GetN()
                    #        x_ref,y_ref,np_ref=self.graphs_ref.GetX(),self.graphs_ref.GetY(),self.graphs_ref.GetN()
                    #
                    #        xn_org,yn_org,npn_org=self.avgraphs_org.GetX(),self.avgraphs_org.GetY(),self.avgraphs_org.GetN()
                    #        xn_ref,yn_ref,npn_ref=self.avgraphs_ref.GetX(),self.avgraphs_ref.GetY(),self.avgraphs_ref.GetN()
                    #
                    #        # good thing is that from peak and valley list we just access the point value, and so if you are shifting graph along y axis , nothing  gonna change and you do not need to change peak and valley position
                    #        # you have to do only the time when you are changing x positions ? 
                    #        print " in org_ref function np org", npn_org
                    #        print " in org_ref function np ref", npn_ref
                    #
                    #        for i in range(npPeaks_org):
                    #            self.gPeak_org.append(TGraph());self.gnPeak_org.append(TGraph())
                    #            iP_org=self.peaks_org[i][2]
                    #            self.gPeak_org[i].SetPoint(0,x_org[iP_org],y_org[iP_org]);self.gnPeak_org[i].SetPoint(0,xn_org[iP_org],yn_org[iP_org])
                    #            self.gPeak_org[i].SetMarkerColor(self.colours[i]);self.gnPeak_org[i].SetMarkerColor(self.colours[i])
                    #            self.gPeak_org[i].SetMarkerSize(2);self.gnPeak_org[i].SetMarkerSize(2)
                    #            self.gPeak_org[i].SetMarkerStyle(8);self.gnPeak_org[i].SetMarkerStyle(8)    
                    #
                    #        for i in range(npPeaks_ref):
                    #            self.gPeak_ref.append(TGraph());self.gnPeak_ref.append(TGraph())
                    #            iP_ref=self.peaks_ref[i][2]
                    #            self.gPeak_ref[i].SetPoint(0,x_ref[iP_ref],y_ref[iP_ref]);self.gnPeak_ref[i].SetPoint(0,xn_ref[iP_ref],yn_ref[iP_ref])
                    #            self.gPeak_ref[i].SetMarkerColor(self.colours_ref[i]);self.gnPeak_ref[i].SetMarkerColor(self.colours_ref[i])
                    #            self.gPeak_ref[i].SetMarkerSize(2);self.gnPeak_ref[i].SetMarkerSize(2)
                    #            self.gPeak_ref[i].SetMarkerStyle(8);self.gnPeak_ref[i].SetMarkerStyle(8)    
                    #
                    #        npWidth_org = len(self.width_org)
                    #        npWidth_ref = len(self.width_ref)
                    #        for i in range(npWidth_org):
                    #            iV_org=self.width_org[i][2]
                    #            print"the valley points final org", self.width_org[i][2]
                    #            self.gWidth_org.SetPoint(i,x_org[iV_org],y_org[iV_org]);self.gnWidth_org.SetPoint(i,xn_org[iV_org],yn_org[iV_org])
                    #        self.gWidth_org.SetMarkerColor(3);self.gnWidth_org.SetMarkerColor(3)
                    #        self.gWidth_org.SetMarkerSize(2);self.gnWidth_org.SetMarkerSize(2)
                    #        self.gWidth_org.SetMarkerStyle(8);self.gnWidth_org.SetMarkerStyle(8)
                    #        
                    #        leg_org= TLegend(0.5,0.85,0.88,0.98)
                    #
                    #        self.logMulti_org.Add(self.avgraphs_org,"pl")
                    #        self.multi_org.Add(self.graphs_org)
                    #        
                    #        maxI_org = len(str(round(max(self.integrals_org),2)))
                    #        for i in range(npPeaks_org):
                    #            self.multi_org.Add(self.gPeak_org[i],"p")
                    #            self.logMulti_org.Add(self.gnPeak_org[i],"p")
                    #
                    #            #Calculate integrals and percentages as well as their respective errors
                    #            #note: errors are still a work in progress so these need to be changed to reflect actual errors
                    #            integral_org=str(round(self.integrals_org[i],2))
                    #            integral_error_org=(str(round(self.interror_org[i][0],2)),str(round(self.interror_org[i][1],2)))
                    #            percentage_org=str(round(100*self.integrals_org[i]/self.sums_org,2))
                    #            perc_error_org=(str(round(100*(self.integrals_org[i]/self.sums_org)*((self.interror_org[i][0]/self.integrals_org[i])**2+(sum(j*j for j in self.interror_org[0])/self.sums_org)),3))
                    #                  ,str(round(100*(self.integrals_org[i]/self.sums_org)*((self.interror_org[i][1]/self.integrals_org[i])**2+(sum(j*j for j in self.interror_org[1])/self.sums_org)),3)))
                    #
                    #            #Used for spacing in the legend entry
                    #            s_org=maxI_org-len(integral_org)+2
                    #            integral_org=" "*s_org+integral_org
                    #            
                    #            #leg_org.AddEntry(gPeak_org[i],self.gcsets[name_org].peakNames[column_org][i]+": "+integral_org+" #pm ^{"+integral_error_org[0]+"}_{"+integral_error_org[1]+"} | "+percentage_org+" #pm ^{"+perc_error_org[0]+"}_{"+perc_error_org[1]+"}%","p")
                    #            leg_org.AddEntry(self.gPeak_org[i],self.peakNames_org[i]+": "+integral_org+" | "+percentage_org+ "%","p")
                    #
                    #        self.multi_org.Add(self.gWidth_org,"p")
                    #        self.logMulti_org.Add(self.gnWidth_org,"p")
                    ##        self.gcsets[name_org].multi[column_org].SetName(name_org)
                    #
                    ## for other reference file calculating everything
                    #
                    #        #Fill Peak Width points to be overlayed on the GC graphs
                    #        npWidth_ref = len(self.width_ref)
                    #        npWidth_ref = len(self.width_ref)
                    #        for i in range(npWidth_ref):
                    #            iV_ref=self.width_ref[i][2]
                    #            print"the valley points final", self.width_ref[i][2]
                    #            self.gWidth_ref.SetPoint(i,x_ref[iV_ref],y_ref[iV_ref]);self.gnWidth_ref.SetPoint(i,xn_ref[iV_ref],yn_ref[iV_ref])
                    #        self.gWidth_ref.SetMarkerColor(28);self.gnWidth_ref.SetMarkerColor(28)
                    #        self.gWidth_ref.SetMarkerSize(2);self.gnWidth_ref.SetMarkerSize(2)
                    #        self.gWidth_ref.SetMarkerStyle(8);self.gnWidth_ref.SetMarkerStyle(8)
                    #        
                    #        leg_ref= TLegend(0.5,0.68,0.88,0.83)
                    #
                    #        self.avgraphs_ref.SetMarkerColor(2)
                    #        self.logMulti_ref.Add(self.avgraphs_ref,"pl")
                    #        self.multi_ref.Add(self.graphs_ref)
                    ##        self.gcsets[name_ref].multi[column_ref].SetMarkerColor(2)
                    #        self.graphs_ref.SetMarkerColor(2) 
                    #        maxI_ref = len(str(round(max(self.integrals_ref),2)))
                    #
                    #        for i in range(npPeaks_ref):
                    #            self.multi_ref.Add(self.gPeak_ref[i],"p")
                    #            self.logMulti_ref.Add(self.gnPeak_ref[i],"p")
                    #
                    #            #Calculate integrals and percentages as well as their respective errors
                    #            #note: errors are still a work in progress so these need to be changed to reflect actual errors
                    #            integral_ref=str(round(self.integrals_ref[i],2))
                    #            integral_error_ref=(str(round(self.interror_ref[i][0],2)),str(round(self.gcsets[name_ref].interror[column_ref][i][1],2)))
                    #            percentage_ref=str(round(100*self.integrals_ref[i]/self.sums_ref,2))
                    #            perc_error_ref=(str(round(100*(self.integrals_ref[i]/self.sums_ref)*((self.interror_ref[i][0]/self.integrals_ref[i])**2+(sum(j*j for j in self.interror_ref[0])/self.sums_ref)),3))
                    #                  ,str(round(100*(self.integrals_ref[i]/self.sums_ref)*((self.interror_ref[i][1]/self.integrals_ref[i])**2+(sum(j*j for j in self.interror_ref[1])/self.sums_ref)),3)))
                    #
                    #            #Used for spacing in the legend entry
                    #            s_ref=maxI_ref-len(integral_ref)+2
                    #            integral_ref=" "*s_ref+integral_ref
                    #            
                    #            #leg_ref.AddEntry(gPeak_ref[i],self.gcsets[name_ref].peakNames[column_ref][i]+": "+integral_ref+" #pm ^{"+integral_error_ref[0]+"}_{"+integral_error_ref[1]+"} | "+percentage_ref+" #pm ^{"+perc_error_ref[0]+"}_{"+perc_error_ref[1]+"}%","p")
                    #            leg_ref.AddEntry(self.gPeak_ref[i],self.gcsets[name_ref].peakNames[column_ref][i]+": "+integral_ref+" | "+percentage_ref+"%","p")
                    #
                    #        self.multi_ref.Add(self.gWidth_ref,"p")
                    #        self.logMulti_ref.Add(self.gnWidth_ref,"p")
                    ##        self.gcsets[name_ref].multi[column_ref].SetName(name_ref)
                    #         
                    # 
                    #        if not self.rfile.GetDirectory("GC_cmp"): self.rfile.mkdir("GC_cmp")
                    #        self.rfile.cd("GC_cmp")
                    #        print"created sub directory"
                    #        self.multi_all.Add(self.multi_org)
                    #        print"created sub directory"
                    #        self.multi_all.Add(self.multi_ref)
                    #        self.canvases.cd()
                    #        self.multi_all.Draw("ap")
                    #        print"setting range"
                    #        self.multi_all.GetXaxis().SetRangeUser(0.2,0.8)
                    #        self.multi_all.GetXaxis().SetTitle("Time (sec)")
                    #        print"range"
                    #        self.multi_all.GetYaxis().SetTitle("Signal (#muV)")
                    #        self.multi_all.GetYaxis().SetTitleOffset(1.2)
                    #        print"setting range"
                    #        leg_org.Draw()
                    #        print"setted org"
                    #        leg_ref.Draw()
                    #        print"setted ref"
                    #        self.canvases.Write()
                    ##        self.canvases[cname].Close()
                    #
                    #        print"logMulti function range"
                    #
                    #        self.c2.cd()
                    #        self.c2.SetLogy()
                    #        self.logMulti_all.Add(self.logMulti_org)
                    #        self.logMulti_all.Add(self.logMulti_ref)
                    #        self.logMulti_all.Draw("ap")
                    #         
                    #        print" printing x[i] - y[i] values avg graphs org "
                    #        for i in range(2000,2010):
                    #          print "({},{})".format(xn_org[i], yn_org[i])
                    #        print" printing x[i] - y[i] values avg graphs ref "
                    #        for i in range(2000,2010):
                    #          print "({},{})".format(xn_ref[i], yn_ref[i])
                    #
                    #        print"error just here"
                    #        #Set range to zoom in on peaks for columns B and C and y axis values, could probably be changed to use the user defined x range
                    #        if   (column_org == "B"): y_list_org=[yn_org[i] for i in range (npn_org) if 0.2 <= xn_org[i] <= 0.8 and yn_org[i] > 1]
                    #        if (column_ref == "B"): y_list_ref=[yn_ref[i] for i in range (npn_ref) if 0.2 <= xn_ref[i] <= 0.8 and yn_ref[i] > 1]
                    #        #print"error*** here"
                    #        if(column_org =="B") :
                    #          if (min(y_list_org)*10**(-0.5) > min(y_list_ref)*10**(-0.5)): 
                    #              print"error new here first"
                    #              self.logMulti_all.GetYaxis().SetRangeUser(min(y_list_ref)*10**(-0.5),max(y_list_org)*10**(2.2))
                    #          else:   
                    #              print"error new here second"
                    #              self.logMulti_all.GetYaxis().SetRangeUser(min(y_list_org)*10**(-0.5),max(y_list_org)*10**(2.2))
                    #              #logMulti_all.GetYaxis().SetRangeUser(500,10**7)
                    #              print"one more step"
                    #       
                    #        print" another more step"
                    #        self.logMulti_all.GetXaxis().SetRangeUser(0.2,0.8) 
                    #        self.logMulti_all.GetXaxis().SetTitle("Time (sec)")
                    #        self.logMulti_all.GetYaxis().SetTitle("Signal (#muV)")
                    #        self.logMulti_all.GetYaxis().SetTitleOffset(1.2)
                    #        leg_org.Draw()
                    #        leg_ref.Draw()
                    #        print" writing in file more step"
                    #        self.c2.Write()
                    ##        self.c2.Close()
                    #        print" closed file step"
                    #        #uncomment these to write y value histogram to file
                    #        #c.Write()
                    #        #self.canvases[cname].SaveAs(name+".png")
                    ##        self.rfile.Close()
                    #        print" closed file step"
                    #            
                    #   
                    ##    def plotGC(self, name, column, newflag, oldname="", oldcolumn=""):
                    ##        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
                    ##            print "can't find ", name, ", column ", column, " in data; doing nothing"
                    ##            return
                    ##        cname=name+"_"+column
                    ##        if newflag:
                    ##            print "creating canvas ", cname            
                    ##            self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
                    ##            self.gcsets[name].graphs[column].Draw("APL")
                    ##            self.graphcount[cname]=1
                    ##        else:
                    ##            oldcname=oldname+"_"+oldcolumn
                    ##            if not(oldcname in self.canvases.keys()):
                    ##                print "please first draw ", oldname, ", column ", oldcolumn, "; doing nothing"
                    ##                return 
                    ##            self.canvases[oldcname].cd()
                    ##            self.gcsets[name].graphs[column].SetLineColor(self.colours[self.graphcount[oldcname]])
                    ##            self.gcsets[name].graphs[column].SetMarkerColor(self.colours[self.graphcount[oldcname]])
                    ##            self.gcsets[name].graphs[column].Draw("PLsames")
                    ##            self.graphcount[oldcname]=self.graphcount[oldcname]+1
                    ##            if not(oldcname in self.legends.keys()):
                    ##                l=TLegend(0.4,0.75,0.9,0.9)
                    ##                l.SetFillStyle(0)
                    ##                l.SetBorderSize(0)
                    ##                l.AddEntry(self.gcsets[oldname].graphs[oldcolumn],oldcname,"PL")
                    ##                self.legends[oldcname]=l
                    ##            l.AddEntry(self.gcsets[name].graphs[column],cname,"PL")
                    ##            l.Draw()
                    ##            self.canvases[oldcname].Update()
                    #
                    #    def evaluate_integral(self, name_org,name_ref, column):
                    #
                    #        self.gcsets[name_org].getIntegral_modified(column)
                    #        self.gcsets[name_ref].getIntegral_modified(column)
                    #
                    #            
                   # 
                    #    def scaleGC_first_peak(self, name_org,name_ref, column):
                    #          # to evaulate the value to shift 
                    #          # first peak and first valley
                    #         peak_org=self.gcsets[name_org].peaks[column][0][2]
                    #         peak_ref=self.gcsets[name_ref].peaks[column][0][2]
                    #         valley_org=self.gcsets[name_org].width[column][0][2]
                    #         valley_ref=self.gcsets[name_ref].width[column][0][2]
                    #
                    #         valley_ref_second = self.gcsets[name_ref].width[column][1][2]
                    #         valley_org_second = self.gcsets[name_org].width[column][1][2]
                    #
                    #         # for Co2 curve
                    #         peak_org_Co2 = self.gcsets[name_org].peaks[column][1][2]
                    #         peak_ref_Co2 = self.gcsets[name_ref].peaks[column][1][2]
                    #
                    #         valley_org_Co2 = self.gcsets[name_org].width[column][2][2]
                    #         valley_org_Co2_second = self.gcsets[name_org].width[column][3][2]
                    # 
                    #         valley_ref_Co2 = self.gcsets[name_ref].width[column][2][2]
                    #         valley_ref_Co2_second = self.gcsets[name_ref].width[column][3][2]
                    #
                    #
                    #         x_org,y_org,np_org=self.gcsets[name_org].graphs[column].GetX(),self.gcsets[name_org].graphs[column].GetY(),self.gcsets[name_org].graphs[column].GetN()
                    #         x_ref,y_ref,np_ref=self.gcsets[name_ref].graphs[column].GetX(),self.gcsets[name_ref].graphs[column].GetY(),self.gcsets[name_ref].graphs[column].GetN()
                    #
                    #         xn_org,yn_org,npn_org=self.gcsets[name_org].avgraphs[column].GetX(),self.gcsets[name_org].avgraphs[column].GetY(),self.gcsets[name_org].avgraphs[column].GetN()
                    #         xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column].GetX(),self.gcsets[name_ref].avgraphs[column].GetY(),self.gcsets[name_ref].avgraphs[column].GetN()
                    #         print " before scaling Ar peak"
                    #         print"i values at peak org and ref : ",peak_org,"  ",peak_ref
                    #         print"x values at peak org and ref : ",x_org[peak_org],"  ",x_ref[peak_ref]
                    #         print"y values at peak org and ref : ",y_org[peak_org],"  ",y_ref[peak_ref]
                    #
                    #         # for first peak and first valley
                    #         y_peak_org_graphs = y_org[peak_org]
                    #         y_base_org_graphs = y_org[valley_org]
                    #         x_peak_org_graphs = x_org[peak_org]
                    #         x_base_org_graphs = x_org[valley_org]
                    #
                    #
                    #         y_peak_org_avgraphs = yn_org[peak_org]
                    #         y_base_org_avgraphs = yn_org[valley_org]
                    #         x_peak_org_avgraphs = xn_org[peak_org]
                    #         x_base_org_avgraphs = xn_org[valley_org]
                    #
                    #         #Co2  curve
                    #         y_peak_Co2_org_graphs = y_org[peak_org_Co2]
                    #         y_base_Co2_org_graphs = y_org[valley_org_Co2]
                    #         x_peak_Co2_org_graphs = x_org[peak_org_Co2]
                    #         x_base_Co2_org_graphs = x_org[valley_org_Co2]
                    #
                    #
                    #         y_peak_Co2_org_avgraphs = yn_org[peak_org_Co2]
                    #         y_base_Co2_org_avgraphs = yn_org[valley_org_Co2]
                    #         x_peak_Co2_org_avgraphs = xn_org[peak_org_Co2]
                    #         x_base_Co2_org_avgraphs = xn_org[valley_org_Co2]
                    #
                    ##         y_peak_ref_graphs = y_ref[peak_ref]
                    ##         y_base_ref_graphs = y_ref[valley_ref]
                    ##         x_peak_ref_graphs = x_ref[peak_ref]
                    ##         x_base_ref_graphs = x_ref[valley_ref]
                    ##
                    ##
                    ##         y_peak_ref_avgraphs = yn_ref[peak_ref]
                    ##         y_base_ref_avgraphs = yn_ref[vallley_ref]
                    ##         x_peak_ref_avgraphs = xn_ref[peak_ref]
                    ##         x_base_ref_avgraphs = xn_ref[vallley_ref]
                    #
                    #
                    #       
                    #         # scaling each point on ref curve to make comparable to the 
                    #
                    #
                    #         print " np in plot org_ref function org ",npn_org
                    #         print " np in plot org_ref function ref ",npn_ref
                    #
                    #         print" peak org x , y ({},{})".format(x_peak_org_graphs,y_peak_org_graphs)
                    #         print" valley org x , y ({},{})".format(x_base_org_graphs,y_base_org_graphs)
                    #
                    #         print" peak ref x , y ({},{})".format(x_ref[peak_ref],y_ref[peak_ref])
                    #         print" valley ref x , y ({},{})".format(x_ref[valley_ref],y_ref[valley_ref])
                    #
                    #         print" peak org avg x , y ({},{})".format(x_peak_org_avgraphs,y_peak_org_avgraphs)
                    #         print" valley org avg x , y ({},{})".format(x_base_org_avgraphs,y_base_org_avgraphs)
                    #
                    #         print" peak ref avg x , y ({},{})".format(xn_ref[peak_ref],yn_ref[peak_ref])
                    #         print" valley ref avg x , y ({},{})".format(xn_ref[valley_ref],yn_ref[valley_ref])
                    #
                    #
                    #
                    #         print" printing x[i] - y[i] values  graphs org before scaling , shifted once to baseline"
                    #         for i in range(2000,2010):
                    #          print "({},{})".format(x_org[i], y_org[i])
                    #         print" printing x[i] - y[i] values  graphs ref before scaling, shifted once to baseline"
                    #         for i in range(2000,2010):
                    #          print "({},{})".format(x_ref[i], y_ref[i])
                    # 
                    #         print" printing x[i] - y[i] values  graphs org between first valley and second valley before scaling , shifted once to baseline"
                    #         for i in range(valley_org, valley_org_second):
                    #          print "({},{})".format(x_org[i], y_org[i])
                    #         print" printing x[i] - y[i] values  graphs ref between first valley and second valley before scaling, shifted once to baseline"
                    #         for i in range(valley_ref, valley_ref_second):
                    #          print "({},{})".format(x_ref[i], y_ref[i])
                    #         # since we need to only scale reference curve
                    #         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
                    #             print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
                    #             return
                    #         self.gcsets[name_ref].scaleGC_peak(column, y_peak_org_graphs, y_base_org_graphs, y_peak_org_avgraphs, y_base_org_avgraphs,peak_ref, valley_ref, valley_ref_second)
                    #         self.gcsets[name_ref].scaleGC_peak(column, y_peak_Co2_org_graphs, y_base_Co2_org_graphs, y_peak_Co2_org_avgraphs, y_base_Co2_org_avgraphs,peak_ref_Co2, valley_ref_Co2, valley_ref_Co2_second)
                    # 
                    #    ##         # checking chi-square after scaling
                    #    ##         chi_square_Ar = 0 
                    #    ##         chi_square_Co2 = 0
                    #    ##         length_range_Ar = 0 
                    #    ##         length_range_Co2 = 0
                    #    ##            
                    #    ##         # Chi-square for Ar peak
                    #    ##         for it in range(valley_org, peak_org): 
                    #    ##            length_range_Ar+=1
                    #    ##            print"y_ref and y_org",y_new_ref[it]," -  ",y_org[it]
                    #    ##            chi_square_Ar = float(chi_square_Ar+ (pow((y_new_ref[it] - y_org[it]),2)/(pow( (0.05*y_org[it]) ,2))))
                    #    ##            print"chi_square ",chi_square_Ar
                    #    ##          print " total chi square ",chi_square_Ar 
                    #    ##          chi_square_ndf_Ar = chi_square_Ar/(length_range_Ar -1)
                    #    ##          chi_square_list_Ar.append(chi_square_ndf_Ar)
                    #    ##          print"chi_square per ndf ",chi_square_ndf_Ar 
                    #    ##
                    #    ##          # Chi-square for Co2 peak
                    #    ##          for it in range(valley_org_Co2, peak_org_Co2): 
                    #    ##            length_range_Co2+=1
                    #    ##            print"y_ref and y_org",y_new_ref[it]," -  ",y_org[it]
                    #    ##            chi_square_Co2 = float(chi_square_Co2+ (pow((y_new_ref[it] - y_org[it]),2)/(pow((0.05 * y_org[it]),2))))
                    #    ##            print"chi_square Co2 ",chi_square_Co2
                    #    ##          print " total chi square Co2 ",chi_square_Co2 
                    #    ##          chi_square_ndf_Co2 = chi_square_Co2/(length_range_Co2 -1)
                    #    ##          chi_square_list_Co2.append(chi_square_ndf_Co2)
                    #    ##          print "chi_square per ndf _Co2",chi_square_ndf_Co2 
                    #    ##            
                    #    ##            #exiting the shift i value loop
                    #    ##
                    #    ##         # make chi square value plot
                    #    ##         print"type chi square ", type(chi_square_ndf_Ar)
                    #    ##       
                    #    ##         for i in range(1,11):
                    #    ##          chi_plot_Ar.SetPoint(i,shift_i_value_list[i], chi_square_list_Ar[i])
                    #    ##         canvas_chi_square_Ar = TCanvas("chi_square_shift_x : Ar","canvas_chi_square_Ar",1200,800)
                    #    ##         chi_plot_Ar.GetXaxis().SetRangeUser(-6,6)
                    #    ##         chi_plot_Ar.SetMarkerColor(2)
                    #    ##         chi_plot_Ar.SetMarkerSize(2)
                    #    ##         chi_plot_Ar.SetMarkerStyle(8)
                    #    ##         chi_plot_Ar.GetYaxis().SetRangeUser(0.,10000)
                    #    ##         canvas_chi_square_Ar.SetLogy()
                    #    ##         chi_plot_Ar.Draw("ap")
                    #    ##         canvas_chi_square_Ar.SaveAs("chi_square_Ar.pdf") 
                    #    ##         print"i values at peak  ref, valley, second valley_Ar : ",peak_ref,"  ",valley_ref, "  ",valley_ref_second
                    #    ##
                    #    ##         min_chi_square_Ar = min(chi_square_list_Ar)
                    #    ##         index_min_chi_square_Ar = chi_square_list_Ar.index(min_chi_square_Ar)
                    #    ##
                    #    ##         print"minimum chi-square is with shift value Ar  ",index_min_chi_square_Ar," with chi-square ",min_chi_square_Ar
                    #    ## 
                    #    ##
                    #    ##            # make chi square value plot
                    #    ##
                    #    ##         for i in range(1,11):
                    #    ##          chi_plot_Co2.SetPoint(i,shift_i_value_list[i], chi_square_list_Co2[i])
                    #    ##         canvas_chi_square_Co2 = TCanvas("chi_square_shift_x : Co2","canvas_chi_square_Co2",1200,800)
                    #    ##         chi_plot_Co2.SetMarkerColor(2)
                    #    ##         chi_plot_Co2.GetXaxis().SetRangeUser(-6,6)
                    #    ##         chi_plot_Co2.SetMarkerSize(2)
                    #    ##         chi_plot_Co2.SetMarkerStyle(8)
                    #    ##         chi_plot_Co2.GetYaxis().SetRangeUser(10000,100000000)
                    #    ##         canvas_chi_square_Co2.SetLogy()
                    #    ##         chi_plot_Co2.Draw("ap")
                    #    ##         canvas_chi_square_Co2.SaveAs("chi_square_Co2.pdf") 
                    #    ##         print"i values at peak  ref, valley, second valley : ",peak_ref_Co2,"  ",valley_ref_Co2, "  ",valley_ref_second_Co2
                    #    ##
                    #    ##         # peak minimum chi-square shift value
                    #    ##
                    #    ##         min_chi_square_Co2 = min(chi_square_list_Co2)
                    #    ##         index_min_chi_square_Co2 = chi_square_list_Co2.index(min_chi_square_Co2)
                    #    ##
                    #    ##         print"minimum chi-square is with shift value  Co2 ",index_min_chi_square_Co2," with chi-square ",min_chi_square_Co2
                    #
                    #
                    #   #  shift along X and check chi-square and find optimum shift value
                    #    def shiftGC_x(self, name_org, name_ref, column):
                    #         print"length of peak list ", len(self.gcsets[name_org].peaks[column])
                    #         peak_org=self.gcsets[name_org].peaks[column][0][2]
                    #         peak_ref=self.gcsets[name_ref].peaks[column][0][2]
                    #         valley_org=self.gcsets[name_org].width[column][0][2]
                    #         valley_ref=self.gcsets[name_ref].width[column][0][2]
                    #
                    #         valley_ref_second = self.gcsets[name_ref].width[column][1][2]
                    #         valley_org_second = self.gcsets[name_org].width[column][1][2]
                    # 
                    #         peak_org_CO2=self.gcsets[name_org].peaks[column][1][2]
                    #         peak_ref_CO2=self.gcsets[name_ref].peaks[column][1][2]
                    #         valley_org_CO2=self.gcsets[name_org].width[column][2][2]
                    #         valley_ref_CO2=self.gcsets[name_ref].width[column][2][2]
                    #
                    #         valley_ref_second_CO2 = self.gcsets[name_ref].width[column][3][2]
                    #         valley_org_second_CO2 = self.gcsets[name_org].width[column][3][2]
                    # 
                    #         x_org,y_org,np_org=self.gcsets[name_org].graphs[column].GetX(),self.gcsets[name_org].graphs[column].GetY(),self.gcsets[name_org].graphs[column].GetN()
                    #         x_ref,y_ref,np_ref=self.gcsets[name_ref].graphs[column].GetX(),self.gcsets[name_ref].graphs[column].GetY(),self.gcsets[name_ref].graphs[column].GetN()
                    #
                    #         xn_org,yn_org,npn_org=self.gcsets[name_org].avgraphs[column].GetX(),self.gcsets[name_org].avgraphs[column].GetY(),self.gcsets[name_org].avgraphs[column].GetN()
                    #         xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column].GetX(),self.gcsets[name_ref].avgraphs[column].GetY(),self.gcsets[name_ref].avgraphs[column].GetN()
                    # 
                    #         print" x, y values for org curve"
                    #         for tmp1 in range(valley_org,valley_org_second):
                    #           print"({},{})".format(tmp1, x_org[tmp1], y_org[tmp1]),
                    #
                    #         print" x, y values for ref curve"
                    #         for tmp2 in range(valley_ref,valley_ref_second):
                    #           print"({},{})".format(tmp2, x_ref[tmp2], y_ref[tmp2]),
                    #
                    #         print"i values at peak org and ref Ar : ",peak_org,"  ",peak_ref
                    #         print"x values at peak org and ref Ar : ",x_org[peak_org],"  ",x_ref[peak_ref]
                    #         print"y values at peak org and ref Ar : ",y_org[peak_org],"  ",y_ref[peak_ref]
                    #      
                    #         print"i values at peak org and ref Co2 : ",peak_org_CO2,"  ",peak_ref_CO2
                    #         print"x values at peak org and ref Co2 : ",x_org[peak_org_CO2],"  ",x_ref[peak_ref_CO2]
                    #         print"y values at peak org and ref Co2 : ",y_org[peak_org_CO2],"  ",y_ref[peak_ref_CO2]
                    # 
                    #         print" values at valley org Ar : ({},{},{})  ".format(valley_org, x_org[valley_org], y_org[valley_org]) 
                    #         print" values at valley second org Ar : ({},{},{})  ".format(valley_org_second, x_org[valley_org_second], y_org[valley_org_second]) 
                    #
                    #         print" values at valley org Co2 : ({},{},{})  ".format(valley_org_CO2, x_org[valley_org_CO2], y_org[valley_org_CO2]) 
                    #         print" values at valley second org Co2 : ({},{},{})  ".format(valley_org_second_CO2, x_org[valley_org_second_CO2], y_org[valley_org_second_CO2]) 
                    #
                    #         print" values at valley ref Ar : ({},{},{})  ".format(valley_ref, x_ref[valley_ref], y_ref[valley_ref]) 
                    #         print" values at valley second ref Ar : ({},{},{})  ".format(valley_ref_second, x_ref[valley_ref_second], y_ref[valley_ref_second]) 
                    #
                    #         print" values at valley ref Co2 : ({},{},{})  ".format(valley_ref_CO2, x_ref[valley_ref_CO2], y_ref[valley_ref_CO2]) 
                    #         print" values at valley second ref Co2 : ({},{},{})  ".format(valley_ref_second_CO2, x_ref[valley_ref_second_CO2], y_ref[valley_ref_second_CO2]) 
                    #
                    #         # shift we define to just check chi-square
                    #         chi_square_list_Ar=[]
                    #         chi_plot_Ar = TGraph()
                    #         shift_i_value_list = []
                    #         #shifting for Ar
                    #         for shift_i_value in range(-10,10):
                    #            print"values by which whole ref curve is shifted along X ",shift_i_value
                    #            # shifting ref curve by shift_i_value and updating new shifted information in x_new_ref and checking chi-square
                    #            x_new_ref = []
                    #            x_new_ref_graph = []
                    #            y_new_ref = []
                    #            y_new_ref_graph = []
                    #    
                    #            for i in range (np_ref):                
                    #                 if i in range(valley_ref-15, valley_ref_second+15) : 
                    #                   x_ref_shift = x_ref[i+ shift_i_value]
                    #                   y_ref_shift = y_ref[i+shift_i_value]
                    #                 else :
                    #                  x_ref_shift = x_ref[i] 
                    #                  y_ref_shift = y_ref[i] 
                    #                 x_new_ref.append(x_ref_shift)
                    #                 y_new_ref.append(y_ref_shift)
                    #    
                    #            shift_i_value_list.append(float(shift_i_value)) 
                    #            print" graph all values after shifting Ar peak" 
                    #             
                    #            for i in range(valley_ref-shift_i_value, valley_ref_second-shift_i_value):
                    #              print"({},{},{})".format(i, x_new_ref[i],y_new_ref[i]), 
                    #             
                    #            
                    #            # checking chi-square now
                    #            chi_square_Ar = 0 
                    #            length_range_Ar = 0 
                    #            
                    #            # Chi-square for Ar peak
                    #            for it in range(valley_org, peak_org): 
                    #              length_range_Ar+=1
                    #              print"y_ref and y_org",y_new_ref[it]," -  ",y_org[it], " :  x_ref and x_org ",x_new_ref[it]," - ",x_org[it]  
                    #              chi_square_Ar = float(chi_square_Ar+ (pow((y_new_ref[it] - y_org[it]),2)/(pow( (0.05*y_org[it]) ,2))))
                    #              print"chi_square ",chi_square_Ar
                    #            print " total chi square ",chi_square_Ar 
                    #            chi_square_ndf_Ar = chi_square_Ar/(length_range_Ar -1)
                    #            chi_square_list_Ar.append(chi_square_ndf_Ar)
                    #            print"chi_square per ndf ",chi_square_ndf_Ar 
                    #
                    #
                    #         # shift we define to just check chi-square
                    #         chi_square_list_Co2=[]
                    #         chi_plot_Co2 = TGraph()
                    #         
                    #         shift_i_value_list_CO2 = []
                    #         #shifting for CO2
                    #         for shift_i_value_CO2 in range(-32,5):
                    #            print"values by which whole ref curve is shifted along X ",shift_i_value_CO2
                    #            # shifting ref curve by shift_i_value and updating new shifted information in x_new_ref and checking chi-square
                    #            x_new_ref = []
                    #            x_new_ref_graph = []
                    #            y_new_ref = []
                    #            y_new_ref_graph = []
                    #    
                    #            for i in range (np_ref):                
                    #                 if i in range(valley_ref_CO2 -35 , valley_ref_second_CO2+35): 
                    #                   x_ref_shift = x_ref[i+shift_i_value_CO2]
                    #                   y_ref_shift = y_ref[i+shift_i_value_CO2]
                    #                 else :
                    #                  x_ref_shift = x_ref[i] 
                    #                  y_ref_shift = y_ref[i] 
                    #                 x_new_ref.append(x_ref_shift)
                    #                 y_new_ref.append(y_ref_shift)
                    #    
                    #            shift_i_value_list_CO2.append(float(shift_i_value_CO2)) 
                    # 
                    #            print" graph all values after shifting CO2 peak" 
                    #             
                    #            for i in range(valley_ref_CO2-shift_i_value_CO2, valley_ref_second_CO2-shift_i_value_CO2):
                    #              print"({},{},{})".format(i, x_new_ref[i],y_new_ref[i]), 
                    # 
                    #            chi_square_Co2 = 0
                    #            length_range_Co2 = 0
                    #            # Chi-square for Co2 peak
                    #            for it in range(valley_org_CO2, peak_org_CO2): 
                    #              length_range_Co2+=1
                    #              print"y_ref and y_org",y_new_ref[it]," -  ",y_org[it]," :  x_ref and x_org ",x_new_ref[it]," - ",x_org[it]  
                    #              chi_square_Co2 = float(chi_square_Co2+ (pow((y_new_ref[it] - y_org[it]),2)/(pow((0.05 * y_org[it]),2))))
                    #              print"chi_square Co2 ",chi_square_Co2
                    #            print " total chi square Co2 ",chi_square_Co2 
                    #            chi_square_ndf_Co2 = chi_square_Co2/(length_range_Co2 -1)
                    #            chi_square_list_Co2.append(chi_square_ndf_Co2)
                    #            print "chi_square per ndf _Co2",chi_square_ndf_Co2 
                    #            
                    #            #exiting the shift i value loop
                    #
                    #         # make chi square value plot
                    #         print"type chi square ", type(chi_square_ndf_Ar)
                    #       
                    #         for i in range(0,20):
                    #           print " i value and chi square list " , i, shift_i_value_list[i], chi_square_list_Ar[i]
                    #           chi_plot_Ar.SetPoint(i,shift_i_value_list[i], chi_square_list_Ar[i])
                    #         canvas_chi_square_Ar = TCanvas("chi_square_shift_x : Ar","canvas_chi_square_Ar",1200,800)
                    #         chi_plot_Ar.GetXaxis().SetRangeUser(-17,17)
                    #         chi_plot_Ar.SetMarkerColor(2)
                    #         chi_plot_Ar.SetMarkerSize(2)
                    #         chi_plot_Ar.SetMarkerStyle(8)
                    #         chi_plot_Ar.GetYaxis().SetRangeUser(0,100000)
                    #         canvas_chi_square_Ar.SetLogy()
                    #         chi_plot_Ar.Draw("AP*")
                    #         canvas_chi_square_Ar.SaveAs("chi_square_Ar.pdf") 
                    #         print"i values at peak  ref, valley, second valley_Ar : ",peak_ref,"  ",valley_ref, "  ",valley_ref_second
                    #
                    #         min_chi_square_Ar = min(chi_square_list_Ar)
                    #         index_min_chi_square_Ar = chi_square_list_Ar.index(min_chi_square_Ar)
                    #
                    #         print"minimum chi-square is with shift value Ar  ",index_min_chi_square_Ar," with chi-square ",min_chi_square_Ar
                    # 
                    #
                    #            # make chi square value plot
                    #
                    #         for i in range(0,35):
                    #          print " i value and chi square list " , i, shift_i_value_list_CO2[i], chi_square_list_Co2[i]
                    #          chi_plot_Co2.SetPoint(i,shift_i_value_list_CO2[i], chi_square_list_Co2[i])
                    #         canvas_chi_square_Co2 = TCanvas("chi_square_shift_x : Co2","canvas_chi_square_Co2",1200,800)
                    #         chi_plot_Co2.SetMarkerColor(2)
                    #         chi_plot_Co2.GetXaxis().SetRangeUser(-35,10)
                    #         chi_plot_Co2.SetMarkerSize(2)
                    #         chi_plot_Co2.SetMarkerStyle(8)
                    #         chi_plot_Co2.GetYaxis().SetRangeUser(0,100000)
                    #         canvas_chi_square_Co2.SetLogy()
                    #         chi_plot_Co2.Draw("AP*")
                    #         canvas_chi_square_Co2.SaveAs("chi_square_Co2.pdf") 
                    #         print"i values at peak  ref, valley, second valley : ",peak_ref_CO2,"  ",valley_ref_CO2, "  ",valley_ref_second_CO2
                    #
                    #         # peak minimum chi-square shift value
                    #
                    #         min_chi_square_Co2 = min(chi_square_list_Co2)
                    #         index_min_chi_square_Co2 = chi_square_list_Co2.index(min_chi_square_Co2)
                    #
                    #         print"minimum chi-square is with shift value  Co2 ",index_min_chi_square_Co2," with chi-square ",min_chi_square_Co2
                    #
                    #         
                    #         #changing the peak and valley for Ar peak according to the shift: we can run setPeak function again, but it will be too much maybe so I am just changing the peak and valley position by knowing the shift to make
                    #        # peak minimum chi-square shift value
                    #
                    # 
                    #         opt_shift_value = shift_i_value_list[index_min_chi_square_Ar]
                    #         opt_shift_value_CO2 = shift_i_value_list_CO2[index_min_chi_square_Co2]
                    #         print"values by which Ar ref peak shifted along X ",opt_shift_value
                    #         print"values by which CO2 ref peak shifted along X ",opt_shift_value_CO2
                    #
                    #         print " shifting for optimum shift : valleys now before shifting",valley_ref, " second " ,valley_ref_second 
                    #         print " shifting for optimum shift : peak now before shifting",peak_ref
                    #         print " shifting for Ar peak " 
                    #         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
                    #              print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
                    #              return
                    #         self.gcsets[name_ref].shiftGC_peak(column, int(opt_shift_value), valley_ref, valley_ref_second) 
                    #
                    #         print " shifting for CO2 peak " 
                    #         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
                    #              print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
                    #              return
                    #         self.gcsets[name_ref].shiftGC_peak(column, int(opt_shift_value_CO2), valley_ref_CO2, valley_ref_second_CO2) 
                    #         #self.gcsets[name_ref].shiftGC_peak(column, int(4), valley_ref_CO2, valley_ref_second_CO2) 
                    #
                    #
                    #         x_ref,y_ref,np_ref=self.gcsets[name_ref].graphs[column].GetX(),self.gcsets[name_ref].graphs[column].GetY(),self.gcsets[name_ref].graphs[column].GetN()
                    #         xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column].GetX(),self.gcsets[name_ref].avgraphs[column].GetY(),self.gcsets[name_ref].avgraphs[column].GetN()
                    #
                    #         valley_ref = valley_ref -  int(opt_shift_value)
                    #         valley_ref_second = valley_ref_second - int(opt_shift_value)
                    #         peak_ref = peak_ref - int(opt_shift_value) 
                    #
                    #         valley_ref_CO2 = valley_ref_CO2 -  int(opt_shift_value_CO2)
                    #         valley_ref_second_CO2 = valley_ref_second_CO2 - int(opt_shift_value_CO2)
                    #         peak_ref_CO2 = peak_ref_CO2 - int(opt_shift_value) 
                    #
                    #
                    #         print"ref curve peak value after shifting x- y"
                    #         print"({},{})".format(x_ref[peak_ref],y_ref[peak_ref])
                    #
                    #         print"peak reference curves"
                    #         print" (i,x,y) : ({},{},{}) ".format(peak_ref, x_ref[peak_ref], y_ref[peak_ref])
                    #         print"valley reference curves"
                    #         print" (i,x,y) : ({},{},{}) ".format(valley_ref, x_ref[valley_ref], y_ref[valley_ref])
                    #         print"second valley reference curves"
                    #         print" (i,x,y) : ({},{},{}) ".format(valley_ref_second, x_ref[valley_ref_second], y_ref[valley_ref_second])
                    #
                    # 
                    #    def setPeak_positions_ref(self,name_ref, column,x_range,peakName):
                    #        self.gcsets[name_ref].setPeak(column,x_range)
                    #        self.gcsets[name_ref].peakNames[column][0] = "Argon"
                    #        self.gcsets[name_ref].peakNames[column][1] = "CO2"
                    #
                    #
                    #