'''
Created on 21 Nov 2016

@author: kkuzn
'''
import sys
import os

from ROOT import gStyle
from ROOT import TCanvas
from ROOT import TLegend
from ROOT import TGraph
from ROOT import TFile
from ROOT import gROOT
from ROOT import TMultiGraph
from ROOT import TF1
from ROOT import TH1D
from ROOT import TH1F
from ROOT import TLine
import ROOT

import GCdata

gROOT.SetBatch(1)

class GSset(object):
    '''
    classdocs
    '''

    def __init__(self, input_file, output_file):
        '''
        Constructor
        '''

        # function just to initialize the member variables of class, so that later when we run the plot function two times, we can just clear the list
        # this initialize functions we will have member variables used for the plotMulti function

        self.output = output_file 
        self.initialize_plot_Multi()
        self.logMulti=TMultiGraph()
        self.multi=TMultiGraph()
       
        self.graphs=TGraph()
        self.avgraphs=TGraph()
        self.graphs_new=TGraph()
        self.avgraphs_new=TGraph()


        self.yHisto = TH1D()

        self.integrals = []
        self.interror  = [] #calculating error for integrals
       

        self.graphcount= {}
        self.legends   = {}
        #graphsets = {};
        self.colours = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
        self.ncolours = 6
        self.peaks=[]
        self.peakNames=[]
        self.valleys=[]
        self.flat=[]
        self.flaterror=[]
        self.width=[]
        self.baselines=[]
        self.canvases  = TCanvas("canvases","canvases",600,700)
        self.c2=TCanvas("log_plot","c2",1200,800)

        gStyle.SetOptTitle(1)
#        cname1="CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018_0001_B"
#        cname2="CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070_B"
#        self.canvases[cname1] = TCanvas(cname1, cname1, 1200, 800)
#        self.canvases[cname2] = TCanvas(cname2, cname2, 1200, 800)
        #temp=TFile(self.output,"RECREATE")
        #temp.Close()

        # read the file and normalize
        self.input_file_name = input_file
        self.readGCs(self.input_file_name)
        self.normalize("B",[0.2,0.8])

    def delete_lists(self):
        del(self.logMulti)
        del(self.multi)
        del(self.output)
       
        del(self.graphs)
        del(self.avgraphs)

        del(self.yHisto)

        del(self.integrals) 
        del(self.interror)  
       

        del(self.graphcount)
        del(self.legends)   
        del(self.colours) 
        del(self.ncolours) 
        del(self.peaks)
        del(self.peakNames)
        del(self.valleys)
        del(self.flat)
        del(self.flaterror)
        del(self.width)
        del(self.baselines)
        del(self.gPeak)
        del(self.gnPeak)
        del(self.gWidth)
        del(self.gnWidth) 
       
        del(self.canvases)  
        del(self.c2)
        del(self.rfile)


    def initialize_plot_Multi(self):

        self.gPeak = []
        self.gnPeak = []
        self.gWidth = TGraph()
        self.gnWidth = TGraph()
       
        self.rfile = TFile(self.output,"RECREATE")


    def readGCs(self,file_name):
        # checking if the input file exists or not 
        print "input file name in readGC ", file_name
        if ".AXY" in file_name:
          try:
            with open(file_name, 'r') as f:
                read_data = f.readlines()
                f.closed
          except:
            print "can't open file ", file_name, "exiting..."
            exit()
              
          N = len(read_data[0].split(", "))
          if(N<=1):
              print "less than two column in file ", file_name, ", exiting..."
              exit()
          if(N>4):
              print "more than tree data columns in file ", file_name, ", will do only three of them..."
              N=4
        
        # just setting the axis range and title for column B plots 
        self.ranges=[100000000000000, -100000000000000]
        self.graphs.SetName("B")
        self.graphs.SetTitle("B")
        # what the new graph is for ?
        self.graphs.SetMarkerStyle(20)
        self.graphs.SetMarkerSize(0.5)
       
        for datastring in read_data:
            dset = datastring.split(", ")
        # we are only reading for column B , so avoiding to do anything for column C
            np  = self.graphs.GetN()
            val = float(dset[2])
            self.graphs.SetPoint(np, float(dset[0]), val)
            if(val>self.ranges[1]):
                self.ranges[1] = val
            if(val<self.ranges[0]):
                self.ranges[0] = val

        # reading all the data points for the file is done

        #normalize the function now creating an avg graph between the range 0.2, 0.8 
        column_names ="B"
        print "read ", file_name, " for columns ", " ".join(cn for cn in column_names) 


    def normalize(self,column,x_range):
       if not(column in "B"):
           print "can't find graph ",column, "doing nothing"
           return
       '''
       Set the most probable y value to 1000 so that there is an easier comparison between all the GC data
       '''
       np = self.graphs.GetN()
       x  = self.graphs.GetX()
       y  = self.graphs.GetY()

       print "normalize function np values", np 
       # for the moments lets not shift anything in avgraph
       y_list = [ y[i] for i in range(np) if x_range[0] <=  x[i] <= x_range[1]] #make a list of y values in the desired range
       self.yHisto = TH1F("y_value_B","",50000,min(y_list),max(y_list)) 

       for i in range(len(y_list)):self.yHisto.Fill(y_list[i])
       min_y2 = self.yHisto.GetXaxis().GetBinCenter(self.yHisto.GetMaximumBin()) #Get most common y value
       #print ("minimum y value from which we are normalizing",min_y2)
       yshift = [y[i]-min_y2+1000 for i in range(np)] #Shift all y values to the required values

       # print " y shifted value over whole spectrum for avg graphs in normalize function "
       for i in range(np):
          self.avgraphs.SetPoint(i,x[i],yshift[i])
       self.avgraphs.SetName(self.graphs.GetName())
    
    def setPeak(self, name, column, peakName,x_range):
        if not(name in self.input_file_name) or not(column in "B") :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        print "Setting peaks for",name,"column",column
        self.normalize(column,x_range) #Set minimum point within range specified to 1000
        self.setPeak_exact(column,x_range) #Set peaks
        self.getIntegral_modified(column) #Get the integrals of the peaks
        self.setPeakName(name,column,-1,peakName) #Set peak names that are specified

    def setPeak_exact(self, column,x_range):
        if not(column in "B"):
            print "can't find graph ",column, "doing nothing"
            return
        np = self.avgraphs.GetN()
        x  = self.avgraphs.GetX()
        y  = self.avgraphs.GetY()
        if type(x_range) != list or len(x_range) != 2:x_range=[0,5]
        y_list = [y[i] for i in range(np) if x_range[0] <= x[i] <= x_range[1]] #make list of y values in desired x range
        i_list = [i for i in range(np) if x_range[0] <= x[i] <= x_range[1]]
        self.yHisto=TH1F("y_value_B","",50,min(y_list),max(y_list))
        for i in range(len(y_list)):self.yHisto.Fill(y_list[i])
        #doubtful - not clear why last bin would be larger than anyone
        self.yHisto.SetBinContent(1,0) #remove the last bin because it is usually much larger than any other
        
       
        sp,ep=min(i_list),max(i_list) #Set start points based off x range
        base_y,base_x,base_i=y[sp],x[sp],sp #values to compare the size of peaks
        prev_y,prev_x = y[sp],x[sp]
        stdev=self.yHisto.GetRMS()
        print "Standard Deviation used",stdev
        threshold=0.1*stdev #anything above this threshold has the chance to be marked as a peak, value was choosen to fit data
        hill=False
        for i in range(sp,ep):
            nPeaks=len(self.peaks)
            nValleys=len(self.valleys)
            if not hill:
                #print "was not a hill in start"
                #the next y value after a peak should be lower than the peak
                if prev_y > y[i]: 
                    valPeak = prev_y
                    #ignore any small bumps that are just noise
                    if abs(valPeak - base_y) >= threshold:
                        avgRise=0
                        atTop=True
                        #check the average y value over the next 150 points, if it is a peak this should be lower than the peak height
                        for j in range(150):
                            avgRise+=y[i+j]
                            if (valPeak < avgRise/float(j+1)):
                                if (valPeak-y[i+j] < threshold):
                                    atTop=False
                                    break
                        if (atTop):
                            print "Found peak at",i-1,prev_x,prev_y,(prev_y-base_y)/stdev
                            self.peaks.append([prev_x,prev_y,i-1])
                            self.peakNames.append(str(nPeaks))
                            #If no valleys have been found before a peak is found we use what ever the peaks height was compared to as the valley
                            if (nValleys == 0):self.valleys.append([base_x,base_y,base_i]);print "Setting start valley at",base_i,base_x,base_y
                            hill = True
                            base_y=prev_y
            elif hill:
                #we want to set the valley at the lowest point possible
                if base_y > y[i]:
                    base_y = y[i]
                    base_x = x[i]
                    base_i = i
                #the next y value after a valley should be higher than the valley
                elif prev_y < y[i]:
                    valPeak = prev_y
                    if abs(valPeak - base_y) >= threshold:
                        avgFall=0
                        atBottom=True
                        #check the average y value over the next 5 points, if it is a valley this should be higher than the valley height
                        for j in range(5):
                            avgFall+=y[i+j]
                            if (valPeak > avgFall/float(j+1)):
                                if (valPeak - y[i+j] < threshold):
                                    atBottom=False
                                    break
                        if (atBottom):
                            #The base values are better for marking valleys, not the prev values (not sure why)
                            print "Found valley at",base_i,base_x,base_y,(prev_y-base_y)/stdev
                            self.valleys.append([base_x,base_y,base_i])
                            hill=False

                    
            prev_x=x[i]
            prev_y=y[i]
        #if we ended on a hill without finding a valley we take the last base values as the last valley
        if hill: self.valleys.append([base_x,base_y,base_i]);print "Setting end valley at",base_i,base_x,base_y

        #print("number of peaks and number of valleys for column :  ",column," before flatcheck")
        print(len(self.peaks))
        print(len(self.valleys))
        for i in range(len(self.peaks)):
          print"peak values : x and y", self.peaks[i][0]," ", self.peaks[i][1]
        for i in range(len(self.valleys)):
          print"peak values : x and y", self.valleys[i][0]," ", self.valleys[i][1]
        #move valleys as close to the peaks without getting on them
        flatcheck = 50 #amount of points that are considered in the linear fit
        for iV in range(len(self.peaks)):
            i_i,i_f = self.valleys[iV][2],self.valleys[iV+1][2]
            y_1,y_2 = self.valleys[iV][1],self.valleys[iV+1][1]
            i_peak = self.peaks[iV][2]
           # print "i peak and i final peak values here" , i_i, "  ", i_f, "peak values here ", i_peak
            prevflat=-1
            fitslopeUp,fitslopeDo=-1,-1 #attempt at calculating uncertianty using physics analysis methods
            minChi2,minSlope=10**10,10**10 #debug variables
            for i in range(i_i,i_peak):
               # print "check values from first valley to the peak"
                if (y[i]-y_1 < threshold):
                    #fit 50 points with a line and use chi2 and slope to determine how flat section is
                    self.graphs.Fit('pol1','Q0','',x[i-flatcheck],x[i+flatcheck/5])
                    linearfit = self.graphs.GetFunction('pol1')
                    if (minChi2 > linearfit.GetChisquare()/stdev):minChi2=linearfit.GetChisquare()/stdev
                    if (minSlope > abs(linearfit.GetParameter(1))/stdev):minSlope=abs(linearfit.GetParameter(1))/stdev
                    fiterror=linearfit.GetParError(1)
                    #Uncertainty calculated by shifting slope up and down my the fit error
                    if (abs(linearfit.GetParameter(1)+fiterror)/stdev < 0.5):fitslopeUp=[x[i],y[i],i]
                    if (abs(linearfit.GetParameter(1)-fiterror)/stdev < 0.5):fitslopeDo=[x[i],y[i],i]
                    
                    if (abs(linearfit.GetParameter(1))/stdev < 0.5): #Slopes normalized to the stdev are choosen to be less than 0.5 to fit data
                        fitslope=abs(linearfit.GetParameter(1))/stdev
                        slopeErr=fiterror/stdev
                        chi2=linearfit.GetChisquare()/stdev
                        prevflat=[x[i],y[i],i]
#                        print "prevflat value",prevflat 
            
            #take the closest point to the peak

            #debug variables
            if not (minChi2==10**10 and minSlope==10**10):
                #print "Minimum Chi2:",minChi2
                #print "Minimum Slope:",minSlope
                pass
            
            if (type(prevflat) != int):
                #print "Min ChiSquare:",minChi
                #print fitslope*stdev,fitslope,"+-",slopeErr,prevflat[0] #,"+-",abs(fitslopeUp[0]-fitslopeDo[0])
               # print "previous flat appended in flat", prevflat
                self.flat.append(prevflat)
                self.flaterror.append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)]) #temporary Up and Down Uncertainty
                #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)])

            minChi2,minSlope=10**10,10**10
            prevflat,fitslopeUp,fitslopeDo=-1,-1,-1
            for i in range(i_f,i_peak,-1):
               # print "check values from second valley to the peak"
                if (y[i]-y_2 < threshold):# and (i_f-i > flatcheck):
                    avgY = [0.0,0.0]
                    self.graphs.Fit('pol1','Q0','',x[i-flatcheck/5],x[i+flatcheck])
                    linearfit = self.graphs.GetFunction('pol1')
                    if (minChi2 > linearfit.GetChisquare()/stdev):minChi2=linearfit.GetChisquare()/stdev
                    if (minSlope > abs(linearfit.GetParameter(1))/stdev):minSlope=abs(linearfit.GetParameter(1))/stdev
                    fiterror=linearfit.GetParError(1)
                    if (abs(linearfit.GetParameter(1)+fiterror)/stdev < 0.005):fitslopeUp=[x[i],y[i],i]
                    if (abs(linearfit.GetParameter(1)-fiterror)/stdev < 0.005):fitslopeDo=[x[i],y[i],i]
                    if (abs(linearfit.GetParameter(1))/stdev < 0.005):
                        fitslope=abs(linearfit.GetParameter(1))/stdev
                        slopeErr=fiterror/stdev
                        chi2=linearfit.GetChisquare()/stdev
                        prevflat=[x[i],y[i],i]
                      #  print "prev value from second valley to peak", prevflat        
            if not (minChi2==10**10 and minSlope==10**10):
                #print "Minimum Chi2:",minChi2
                #print "Minimum Slope:",minSlope
                pass
            if (type(prevflat) != int):
                #print "Min ChiSquare:",minChi
                #print fitslope*stdev,fitslope,"+-",slopeErr,prevflat[0] #,"+-",abs(fitslopeUp[0]-fitslopeDo[0])
               # print "previous flat value in last" ,prevflat
                self.flat.append(prevflat)
                self.flaterror.append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)])
                #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)])
 
    def setPeakName(self,name,column,nPeak,peakName):
        if nPeak == -1:
            nPeak = len(self.peaks)
            for i in range(nPeak):
                self.peakNames[i] = peakName[i]

        #else:
        ##     self.gcsets[name].peakNames[column][i] = peakName   
        
    def shiftGC(self, name, column):
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        self.gcsets[name].shiftGraph(column, value)

    def scaleGCx(self, name, column, value):
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        self.gcsets[name].scaleGraphx(column, value)

    def scaleGCy(self, name, column, value):
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        self.gcsets[name].scaleGraphy(column, value)


    def saveGC(self,name,column):
        cname=name+"_"+column
        if not(cname in self.canvases.keys()) :
            print "can't find ", cname," in known canvases; can't save"
            return
        self.canvases[cname].SaveAs(cname+".png")
        
    def savePlot(self,name,column):
        if not (name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()):
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        
    def getIntegral_modified(self,column):
        if not(column in "B"):
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        # in order to not take  CF4 into account  and integrating from Ar +CF4, 
        # means we have to ignore integrating between 1st and 2nd point, integrate between 1st and 3rd point
        np  = self.graphs.GetN()
        x   = self.graphs.GetX()
        y   = self.graphs.GetY()
        nValleys = len(self.valleys)
         # for finding first closer point to peak and storing its value
        first_point=0
        print" graph all values when evaluating integral" 
        
        # popping out valleys and a peak and a flat for original curve
        if(len(self.peaks)==3):
          self.peaks.pop(1)
          self.valleys.pop(1)
          nValleys=3

        for i in range(nValleys-1):
            integral,integralUp,integralDo=0.0,0.0,0.0
            point_i,point_i_err = self.valleys[i],[(0.000333, 0.000333), (1, 1), (1, 1)]
            point_f,point_f_err = self.valleys[i+1],[(0.000333, 0.000333), (1, 1), (1, 1)]

            #just some printing 
            print" it is the reference curve with two peaks"
            print"length peak ",len(self.peaks)
            for m in range(len(self.peaks)):
              print" peaks",self.peaks[m][0]
            print"length valley ",len(self.valleys)
            for m in range(len(self.valleys)):
              print" peaks",self.valleys[m][0]
            print"length flat column and values",len(self.flat)
            for m in range(len(self.flat)):
              print" flat",self.flat[m][0]

            #program logic here
            for p in range(len(self.flat)):
                #determine if there is a closer point to the peak than the marked valley
                #if self.peaks[column] == 3 and p ==3: i=2
                point=self.flat[p]
                pointerror=self.flaterror[p]
                if point_i[2] < point[2] < point_f[2]:
                    if point[2] < self.peaks[i][2]:point_i,point_i_err=point,pointerror
                    elif self.peaks[i][2] < point[2]:point_f,point_f_err=point,pointerror

            self.width.append(point_i)
            self.width.append(point_f)
            i_i,i_f = point_i[2],point_f[2]
            # storing the first closer point to the peak for future calculations
            # only store the first closer point and not after it
            if(first_point == 0): 
              self.first_point_x = x[i_i]  
              self.first_point_y = y[i_i]
              first_point = 1
            print("valley x here : ",x[i_i], " , ", x[i_f])
            print("valley y here : ",y[i_i], " , ", y[i_f])
            #Uncertainty in  x                    y       i
            point_i_err = [(0.000333, 0.000333), (1, 1), (1, 1)] #temporary uncertainty
            point_f_err = [(0.000333, 0.000333), (1, 1), (1, 1)]
            i_i_e,i_f_e=point_i_err[2],point_f_err[2]
            i_min = -1

            #uses the lowest point between the two bounds for the baseline
            if   y[i_i] < y[i_f]:base,i_min=y[i_i],i_i 
            elif y[i_f] < y[i_i]:base,i_min=y[i_f],i_f
            
            self.baselines.append((x[i_i],x[i_f]))

            slope =  (y[i_f]-y[i_i])/(x[i_f]-x[i_i])
            y_baseline= []
            print"slope of the line to find integral when nPeaks are",len(self.peaks), " is :", slope

            # defining a baseline with a line joining the two valleys
            for j in range(i_i,i_f):
               #to insert some value in the y_baseline  after i_f we use if j=i_f
               y_baseline_value = slope*(x[j]-x[i_i]) + y[i_i]
               dx = x[j+1]-x[j]
               integral+=( ( (y[j]+y[j+1])/2) - y_baseline_value)*dx

            print "y baselines values in the slope lines  "
            for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
                dx=(x[j+1]-x[j])
                slope =  (y[i_f+i_f_e[0]]-y[i_i-i_i_e[0]])/(x[i_f+i_f_e[0]]-x[i_i-i_i_e[0]])
                y_baseline_value = slope*(x[j]-x[i_i]) + y[i_i]
                integralUp+=(y[j]-y_baseline_value)*dx

            for j in range(i_i+i_i_e[1],i_f-i_f_e[1]):
                slope =  (y[i_f-i_f_e[0]]-y[i_i+i_i_e[0]])/(x[i_f-i_f_e[0]]-x[i_i+i_i_e[0]])
                y_baseline_value = slope*(x[j]-x[i_i]) + y[i_i]
                dx=(x[j+1]-x[j])
                integralDo+=(y[j]-y_baseline_value)*dx

            # evaluating error in integration
#            for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
#                dx=(x[j+1]-x[j])
#                slope =  (y[i_f+i_f_e[0]]-y[i_i-i_i_e[0]])/(x[i_f+i_f_e[0]]-x[i_i-i_i_e[0]])
#                y_baseline_value = slope*(x[j+1]-x[i_i]) + y[i_i]
#                integralUp+=(y[j]-y_baseline_value)*dx
#
#            for j in range(i_i+i_i_e[1],i_f-i_f_e[1]):
#                slope =  (y[i_f-i_f_e[0]]-y[i_i+i_i_e[0]])/(x[i_f-i_f_e[0]]-x[i_i+i_i_e[0]])
#                y_baseline_value = slope*(x[j]-x[i_i]) + y[i_i]
#                dx=(x[j+1]-x[j])
#                integralDo+=(y[j]-y_baseline_value)*dx
#

#            for j in range(np):
#              if j==i_i-i_i_e[0]:
#              # to insert some value in the y_baseline before i_i  we use if j=i_i 
#                y_baseline_value = y[i_i]
#                y_baseline.append(y_baseline_value)
#              elif j in range(i_i, i_f):
#                 #to insert some value in the y_baseline  after i_f we use if j=i_f
#                 y_baseline_value = slope*(x[j]-x[i_i]) + y[i_i]
#                 y_baseline.append(y_baseline_value)
#                 if j==i_f : y_baseline.append(y_baseline_value)
#                 dx = x[j+1]-x[j]
#                 integral+=(y[j]-y_baseline_value)*dx
#              else: 
#                 y_baseline.append(0)
            #print"j range : ",i_i," ",i_f
#           for j in range(i_i,i_f):
#                dx=(x[1]-x[0])
#                integral+=(y[j]-base)*dx

            #calculating Up and Down from shifting bounds in and out from the peak
    #            print "y baselines values in the slope lines  "
    #            for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
    #              print"({},{})".format(x[j],y_baseline[j]),
    #            for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
    #                #print" values j ",j
    #                dx=(x[j+1]-x[j])
    #                integralUp+=(y[j]-y_baseline[j])*dx
    #
    #            for j in range(i_i+i_i_e[1],i_f-i_f_e[1]):
    #                dx=(x[j+1]-x[j])
    #                integralDo+=(y[j]-y_baseline[j])*dx

#           for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
#                dx=(x[1]-x[0])
#                integralUp+=(y[j]-base)*dx
#
#            for j in range(i_i+i_i_e[1],i_f-i_f_e[1]):
#                dx=(x[1]-x[0])
#                integralDo+=(y[j]-base)*dx

            self.interror.append((abs(integral-integralUp),abs(integral-integralDo))) #error given for both up and down
            self.integrals.append(integral)
            print "integral value for column ", column, "integral ", integral
            
        self.sums=0.0
        
        print"integral errors Ar ",self.interror[0]
        print"integral errors Co2 ",self.interror[1]
        for i in self.integrals:
            self.sums+=i

        #calculating the error for the ratio
        for i in range(len(self.integrals)):
            error=(100*(self.integrals[i]/self.sums)*((self.interror[i][0]/self.integrals[i])**2+(sum(j*j for j in self.interror[0])/self.sums))
                  ,100*(self.integrals[i]/self.sums)*((self.interror[i][1]/self.integrals[i])**2+(sum(j*j for j in self.interror[1])/self.sums)))
            print self.peakNames[i],100*self.integrals[i]/self.sums,"+",error[0],"-",error[1],"%n"



    def plotDrift(self,column):
        fnames = sorted(self.gcsets.keys())
        if not(column in self.gcsets[fnames[0]].graphs.keys()):
            print "can't find column ", column, " in data; doing nothing"
            return
        print
        print "===================="
        print "Creating Drift Plots for column",column

        #Define Drift plots
        gBaselineDrift = TMultiGraph()
        gIntegralDrift = TMultiGraph()
        gPercentDrift  = TMultiGraph()
        gPeakDrift     = TMultiGraph()

        leg = TLegend(0.5,0.65,0.88,0.85)
        leg.SetTextSize(0.025)

        gBaselineDrift.SetName(fnames[0][:len(fnames[0])-8]+"_"+column+"_BaseLineDrift")
        gIntegralDrift.SetName(fnames[0][:len(fnames[0])-8]+"_"+column+"_IntegralDrift")
        gPercentDrift.SetName(fnames[0][:len(fnames[0])-8]+"_"+column+"_PercentDrift")
        gPeakDrift.SetName(fnames[0][:len(fnames[0])-8]+"_"+column+"_PeakDrift")

        gMaximum,gMinimum = [0.,0.,0.,0.], [10**10,10**10,10**10,10**10]
        avgIntegral=[]
        for peak in range(len(self.gcsets[fnames[0]].peaks[column])):

            #Get average integrals over the last 10 measurements
            total=0.0
            for fn in fnames[-10:]:total+=self.gcsets[fn].integrals[column][peak]
            total/=len(fnames[-10:])
            avgIntegral.append(total)
            
            gBaseline1 = TGraph()
            gBaseline2 = TGraph()
            gIntegral =  TGraph()
            gPercent  =  TGraph()
            gPeak     =  TGraph()

            #Define graphs to be put into TMulti graphs
            gMulti = [[gBaseline1,gBaseline2],gIntegral,gPercent,gPeak]
            for fn in range(len(fnames)):
                measurment=int(fnames[fn].replace(".AXY","")[len(fnames[fn])-8:])
                gValue = [self.gcsets[fnames[fn]].baselines[column][peak],self.gcsets[fnames[fn]].integrals[column][peak],100*self.gcsets[fnames[fn]].integrals[column][peak]/self.gcsets[fnames[fn]].sums[column],self.gcsets[fnames[fn]].peaks[column][peak][0]]

                #Special case for the baselines since every peak has two points to define its width
                for i in range(2):
                    if gMaximum[0] < gValue[0][i]: gMaximum[0] = gValue[0][i]
                    if gMinimum[0] > gValue[0][i]: gMinimum[0] = gValue[0][i]
                    gMulti[0][i].SetPoint(fn,measurment,gValue[0][i])
                    gMulti[0][i].SetLineColor(3)
                    gMulti[0][i].SetLineWidth(2)

                #Fill graphs with their values
                for i in range(1,len(gMulti)):
                    if gMaximum[i] < gValue[i]: gMaximum[i] = gValue[i]
                    if gMinimum[i] > gValue[i]: gMinimum[i] = gValue[i]
                    gMulti[i].SetPoint(fn,measurment,gValue[i])
                    gMulti[i].SetLineColor(self.colours[peak])
                    gMulti[i].SetLineWidth(2)

            leg.AddEntry(gIntegral,self.gcsets[fnames[0]].peakNames[column][peak],"l")
                
            #Baseline graph has both valleys and peak positions 
            gBaselineDrift.Add(gMulti[0][0],"lp")
            gBaselineDrift.Add(gMulti[0][1],"lp")
            gBaselineDrift.Add(gMulti[3].Clone(),"lp") #need to clone this one so it can be used again in gPeakDrift

            gIntegralDrift.Add(gMulti[1],"lp")
            gPercentDrift.Add(gMulti[2],"lp")
            gPeakDrift.Add(gMulti[3],"lp")

        #print average concentrations over last 10 meaurements
        for peak in range(len(self.gcsets[fnames[0]].peaks[column])):
            print self.gcsets[fnames[0]].peakNames[column][peak],100*avgIntegral[peak]/sum(avgIntegral)

        #Making the graphs pretty
        gMultiDrift = [gBaselineDrift,gIntegralDrift,gPercentDrift,gPeakDrift]
        gAxis  = ["Time of Baseline (s)","Peak Integral","Peak Integral/Total Integral","Time of Peak (s)"]
        
        rfile = TFile(self.output,"update")
        if not rfile.GetDirectory("drift"):rfile.mkdir("drift")
        rfile.cd("drift")
        if not rfile.GetDirectory("drift/"+column):rfile.mkdir("drift/"+column)
        rfile.cd("drift/"+column)
        for g in range(len(gMultiDrift)):
            canvas = TCanvas(gMultiDrift[g].GetName(),gMultiDrift[g].GetName(), 1200, 800)
            print gMultiDrift[g].GetName()
            gMultiDrift[g].Draw("a")
            gMultiDrift[g].SetMaximum(gMaximum[g]*1.5)
            gMultiDrift[g].SetMinimum(gMinimum[g]*0.5)
            gMultiDrift[g].GetXaxis().SetTitle("Measurment Number")
            gMultiDrift[g].GetYaxis().SetTitle(gAxis[g])
            gMultiDrift[g].GetYaxis().SetTitleOffset(1.4)
            leg.Draw()
            canvas.Write()
        rfile.Close()
                   
    def plotMulti(self,name,column):
        if name.endswith('.AXY'):
         name_new = name[:-4]
        cname=name_new+"_"+column
        if not (name in self.input_file_name) or not(column in "B"):
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        #Fill Peak points to be overlayed on the GC graphs
        self.npPeaks = len(self.peaks)
        print" number of peaks ****************************************",self.npPeaks
        x,y,np=self.graphs.GetX(),self.graphs.GetY(),self.graphs.GetN()
        xn,yn,npn=self.avgraphs.GetX(),self.avgraphs.GetY(),self.avgraphs.GetN()
        for i in range(self.npPeaks):
            self.gPeak.append(TGraph());self.gnPeak.append(TGraph())
            iP=self.peaks[i][2]
            self.gPeak[i].SetPoint(0,x[iP],y[iP]);self.gnPeak[i].SetPoint(0,xn[iP],yn[iP])
            self.gPeak[i].SetMarkerColor(self.colours[i]);self.gnPeak[i].SetMarkerColor(self.colours[i])
            self.gPeak[i].SetMarkerSize(2);self.gnPeak[i].SetMarkerSize(2)
            self.gPeak[i].SetMarkerStyle(8);self.gnPeak[i].SetMarkerStyle(8)    

        #Fill Peak Width points to be overlayed on the GC graphs
        self.npWidth = len(self.width)
        print" number of valleys ****************************************",self.npWidth 
        for i in range(self.npWidth):
            iV=self.width[i][2]
            self.gWidth.SetPoint(i,x[iV],y[iV]);self.gnWidth.SetPoint(i,xn[iV],yn[iV])
        self.gWidth.SetMarkerColor(3);self.gnWidth.SetMarkerColor(3)
        self.gWidth.SetMarkerSize(2);self.gnWidth.SetMarkerSize(2)
        self.gWidth.SetMarkerStyle(8);self.gnWidth.SetMarkerStyle(8)
        
        leg= TLegend(0.5,0.65,0.88,0.85)

        self.multi.Add(self.graphs,"pl")
        self.logMulti.Add(self.avgraphs,"pl")
        
        maxI = len(str(round(max(self.integrals),2)))
        #if npPeaks == 3: loop_times = npPeaks-1
        #else: loop_times = npPeaks
        for i in range(self.npPeaks):
            self.multi.Add(self.gPeak[i],"p")
            self.logMulti.Add(self.gnPeak[i],"p")

            #Calculate integrals and percentages as well as their respective errors
            #note: errors are still a work in progress so these need to be changed to reflect actual errors
            self.integral=str(round(self.integrals[i],2))
            self.integral_error=(str(round(self.interror[i][0],2)),str(round(self.interror[i][1],2)))
            self.percentage=str(round(100*self.integrals[i]/self.sums,2))
            self.perc_error=(str(round(100*(self.integrals[i]/self.sums)*((self.interror[i][0]/self.integrals[i])**2+(sum(j*j for j in self.interror[0])/self.sums)),3))
                  ,str(round(100*(self.integrals[i]/self.sums)*((self.interror[i][1]/self.integrals[i])**2+(sum(j*j for j in self.interror[1])/self.sums)),3)))

            #Used for spacing in the legend entry
            s=maxI-len(self.integral)+2
            self.integral=" "*s+self.integral
            
            #leg.AddEntry(self.gPeak[i],self.peakNames[i]+": "+self.integral+" #pm ^{"+self.integral_error[0]+"}_{"+self.integral_error[1]+"} | "+self.percentage+" #pm ^{"+self.perc_error[0]+"}_{"+self.perc_error[1]+"}%","p")
            leg.AddEntry(self.gPeak[i],self.peakNames[i]+": "+self.integral+" | "+self.percentage+"%","p")

        self.multi.Add(self.gWidth,"p")
        self.logMulti.Add(self.gnWidth,"p")
#        self.multi.SetName(name_new)
#        self.multi.SetTitle("B")

        print "creating canvas ", cname            
        if self.rfile.GetDirectory("GC"):  print"yes dir GC"
        if not self.rfile.GetDirectory("GC"): self.rfile.mkdir("GC") ; print"makign dir GC"
        self.rfile.cd("GC")
        # if not self.rfile.GetDirectory(column):self.rfile.mkdir("GC/"+column); print"making another column directory"
       # self.rfile.cd("GC/"+column)
        self.canvases.cd()
        self.multi.Draw("a")
        #Set range to zoom in on peaks for columns B and C, could probably be changed to use the user defined x range
        leg.Draw()
        self.canvases.Write()
        self.multi.GetXaxis().SetRangeUser(0.2,0.8)
        self.multi.GetXaxis().SetTitle("Time (sec)")
        self.multi.GetYaxis().SetTitle("Signal (#muV)")
        self.multi.GetYaxis().SetTitleOffset(1.2)
        #   self.canvases[cname].SaveAs(name+".png")
        
        self.c2.cd()
        self.c2.SetLogy()
        self.logMulti.Draw("a")
        print " after plottign log MUlti and before axis length"
        #Set range to zoom in on peaks for columns B and C and y axis values, could probably be changed to use the user defined x range
        self.logMulti.GetXaxis().SetRangeUser(0.2,0.8);#y_list=[yn[i] for i in range (npn) if 0.2 <= xn[i] <= 0.8 and yn[i] > 1];logMulti.GetYaxis().SetRangeUser(min(y_list)*10**(-0.5),max(y_list)*10**(2.2))
        #elif (column == "C"): self.logMulti.GetXaxis().SetRangeUser(0.1,0.5);#y_list=[yn[i] for i in range (npn) if 0.1 <= xn[i] <= 0.5 and yn[i] > 1];logMulti.GetYaxis().SetRangeUser(min(y_list)*10**(-0.5),max(y_list)*10**(2))
        
        print " after axis length"
        self.logMulti.GetXaxis().SetTitle("Time (sec)")
        self.logMulti.GetYaxis().SetTitle("Signal (#muV)")
        self.logMulti.GetYaxis().SetTitleOffset(1.2)
        leg.Draw()
        print"error in writing the canvas"
        self.c2.Write()
        print"error in closing the file"
 
        del(self.canvases)
        del(self.c2)
        #deleting the list now 
        #del(self.peaks)
        #del(self.peakNames)
        #del(self.valleys)
        #del(self.flat)
        #del(self.flaterror)
 
#        del(self.gPeak) 
#       del(self.gnPeak)
#       del(self.gWidth)
#        del(self.gnWidth)

    def plotGC(self, name, column, newflag, oldname="", oldcolumn=""):
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        cname=name+"_"+column
        if newflag:
            print "creating canvas ", cname            
            self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
            self.gcsets[name].graphs[column].Draw("APL")
            self.graphcount[cname]=1
        else:
            oldcname=oldname+"_"+oldcolumn
            if not(oldcname in self.canvases.keys()):
                print "please first draw ", oldname, ", column ", oldcolumn, "; doing nothing"
                return 
            self.canvases[oldcname].cd()
            self.gcsets[name].graphs[column].SetLineColor(self.colours[self.graphcount[oldcname]])
            self.gcsets[name].graphs[column].SetMarkerColor(self.colours[self.graphcount[oldcname]])
            self.gcsets[name].graphs[column].Draw("PLsames")
            self.graphcount[oldcname]=self.graphcount[oldcname]+1
            if not(oldcname in self.legends.keys()):
                l=TLegend(0.4,0.75,0.9,0.9)
                l.SetFillStyle(0)
                l.SetBorderSize(0)
                l.AddEntry(self.gcsets[oldname].graphs[oldcolumn],oldcname,"PL")
                self.legends[oldcname]=l
            l.AddEntry(self.gcsets[name].graphs[column],cname,"PL")
            l.Draw()
            self.canvases[oldcname].Update()
            
           
