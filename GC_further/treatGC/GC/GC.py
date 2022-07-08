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
from ROOT import TLine
import ROOT

import GCdata

gROOT.SetBatch(1)

class GSset(object):
    '''
    classdocs
    '''

    def __init__(self, files_or_dir, dir_flag, verb, pdfname):
        '''
        Constructor
        '''
        self.gcsets    = {};
        self.canvases  = {};
        self.graphcount= {};
        self.legends   = {};
        #graphsets = {};
        self.colours = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
        self.ncolours = 6

        #self.output='Plot.root'
        #temp=TFile(self.output,"RECREATE")
        #temp.Close()
        gStyle.SetOptTitle(1);
        if dir_flag:
            print "opening directory ", files_or_dir
            list_of_files = [(files_or_dir+"/"+f) for f in os.listdir(files_or_dir) ]
            print "here  ",list_of_files
        else:
            print "files or dir ", files_or_dir
            list_of_files = files_or_dir.split(",")
        self.readGCs(list_of_files, verb)
        
    def addGCs(self, files):
        list_of_files = files.split(",")
        self.readGCs(list_of_files)
        
        
    def readGCs(self,list_of_files, verb=False):
        print " list of files from readGCs ", list_of_files
        for afile in list_of_files:
            print "afile name : ", afile
            fname  = afile.split("/")[-1]
            print "fname in readGC ", fname
            if ".AXY" in fname:
                self.gcsets[fname] = GCdata.GCdata(afile)            
                column_names =self.gcsets[fname].graphs.keys()
                print "read ", afile, " for columns ", " ".join(cn for cn in column_names) 

    def plotAvg(self,name,column):
        cname=name+"_"+column
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        self.gcsets[name].averageGraph(column)
        #print "creating canvas ", cname            
        #self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
        #self.gcsets[name].avgraphs[column].Draw("APL")

    def normalize(self,name,column):
        self.gcsets[name].normalize(column)
     
    def setPeak(self, name, column, peakName,x_range):
        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        print "Setting peaks for",name,"column",column
        self.gcsets[name].normalize(column,x_range) #Set minimum point within range specified to 1000
        self.gcsets[name].setPeak(column,x_range) #Set peaks
        self.gcsets[name].getIntegral_modified(column) #Get the integrals of the peaks
        self.setPeakName(name,column,-1,peakName) #Set peak names that are specified

    def setPeakName(self,name,column,nPeak,peakName):
        if nPeak == -1:
            nPeak = len(self.gcsets[name].peaks[column])
            for i in range(nPeak):
                self.gcsets[name].peakNames[column][i] = peakName[i]

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
        
    def getIntegral(self,name,column,peakName):
        if not (name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()):
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        self.gcsets[name].getIntegral_modified(column)
    
#    def getPeakValley(self, name, column,peakName):
#        if not (name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()):
#             print "can't find ", name, ", column ", column, " in data; doing nothing"
#             return  
#        self.gcsets[name].getPeakValley(column)
#        self.first_valley_x_value = self.gcsets[name].valley_x_value 
#        self.first_valley_y_value = self.gcsets[name].valley_y_value 
#        self.first_peak_x_value = self.gcsets[name].peak_x_value 
#        self.first_peak_y_value = self.gcsets[name].peak_y_value 
#        print "first peak : x and y "
#        print  self.first_peak_x_value, " ", self.first_peak_y_value
#        print "first valley : x and y "
#        print  self.first_valley_x_value, " ", self.first_valley_y_value

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
        if not (name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()):
            print "can't find ", name, ", column ", column, " in data; doing nothing"
            return
        #Used to look at histogram of y values over the x range specified
        #c=TCanvas(self.gcsets[name].yHisto[column].GetName()+"_"+name,"c",800,800)
        #self.gcsets[name].yHisto[column].Draw("HIST")
        #c.SaveAs(c.GetName()+".png")
        #os.system("mv "+c.GetName()+".png /afs/hep.wisc.edu/home/ekoenig4/public_html/CSC/GC/tempPlots/")

        #Fill Peak points to be overlayed on the GC graphs
        gPeak = [] #Used to overlay on raw GC data
        gnPeak= [] #Used to overlay on normalized GC data
        npPeaks = len(self.gcsets[name].peaks[column])
        x,y,np=self.gcsets[name].graphs[column].GetX(),self.gcsets[name].graphs[column].GetY(),self.gcsets[name].graphs[column].GetN()
        xn,yn,npn=self.gcsets[name].avgraphs[column].GetX(),self.gcsets[name].avgraphs[column].GetY(),self.gcsets[name].avgraphs[column].GetN()
        for i in range(npPeaks):
            gPeak.append(TGraph());gnPeak.append(TGraph())
            iP=self.gcsets[name].peaks[column][i][2]
            gPeak[i].SetPoint(0,x[iP],y[iP]);gnPeak[i].SetPoint(0,xn[iP],yn[iP])
            gPeak[i].SetMarkerColor(self.colours[i]);gnPeak[i].SetMarkerColor(self.colours[i])
            gPeak[i].SetMarkerSize(2);gnPeak[i].SetMarkerSize(2)
            gPeak[i].SetMarkerStyle(8);gnPeak[i].SetMarkerStyle(8)    

        #Fill Peak Width points to be overlayed on the GC graphs
        gWidth = TGraph() #Used to overlay on raw GC data
        gnWidth = TGraph() # Used to overlay on normalized GC data
        npWidth = len(self.gcsets[name].width[column])
        for i in range(npWidth):
            iV=self.gcsets[name].width[column][i][2]
            gWidth.SetPoint(i,x[iV],y[iV]);gnWidth.SetPoint(i,xn[iV],yn[iV])
        gWidth.SetMarkerColor(3);gnWidth.SetMarkerColor(3)
        gWidth.SetMarkerSize(2);gnWidth.SetMarkerSize(2)
        gWidth.SetMarkerStyle(8);gnWidth.SetMarkerStyle(8)
        
        leg= TLegend(0.5,0.65,0.88,0.85)

        logMulti=TMultiGraph()
        logMulti.Add(self.gcsets[name].avgraphs[column],"pl")
        
        self.gcsets[name].multi[column].Add(self.gcsets[name].graphs[column],"pl")
        
        maxI = len(str(round(max(self.gcsets[name].integrals[column]),2)))
        #if npPeaks == 3: loop_times = npPeaks-1
        #else: loop_times = npPeaks
        for i in range(npPeaks):
            self.gcsets[name].multi[column].Add(gPeak[i],"p")
            logMulti.Add(gnPeak[i],"p")

            #Calculate integrals and percentages as well as their respective errors
            #note: errors are still a work in progress so these need to be changed to reflect actual errors
            integral=str(round(self.gcsets[name].integrals[column][i],2))
            integral_error=(str(round(self.gcsets[name].interror[column][i][0],2)),str(round(self.gcsets[name].interror[column][i][1],2)))
            percentage=str(round(100*self.gcsets[name].integrals[column][i]/self.gcsets[name].sums[column],2))
            perc_error=(str(round(100*(self.gcsets[name].integrals[column][i]/self.gcsets[name].sums[column])*((self.gcsets[name].interror[column][i][0]/self.gcsets[name].integrals[column][i])**2+(sum(j*j for j in self.gcsets[name].interror[column][0])/self.gcsets[name].sums[column])),3))
                  ,str(round(100*(self.gcsets[name].integrals[column][i]/self.gcsets[name].sums[column])*((self.gcsets[name].interror[column][i][1]/self.gcsets[name].integrals[column][i])**2+(sum(j*j for j in self.gcsets[name].interror[column][1])/self.gcsets[name].sums[column])),3)))

            #Used for spacing in the legend entry
            s=maxI-len(integral)+2
            integral=" "*s+integral
            
            #leg.AddEntry(gPeak[i],self.gcsets[name].peakNames[column][i]+": "+integral+" #pm ^{"+integral_error[0]+"}_{"+integral_error[1]+"} | "+percentage+" #pm ^{"+perc_error[0]+"}_{"+perc_error[1]+"}%","p")
            leg.AddEntry(gPeak[i],self.gcsets[name].peakNames[column][i]+": "+integral+" | "+percentage+"%","p")

        self.gcsets[name].multi[column].Add(gWidth,"p")
        logMulti.Add(gnWidth,"p")
        self.gcsets[name].multi[column].SetName(name)

        self.output = "Plot_" + name_new + ".root"
        rfile = TFile(self.output,"RECREATE")
        print "creating canvas ", cname            
        self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
        if not rfile.GetDirectory("GC"): rfile.mkdir("GC")
        rfile.cd("GC")
        if not rfile.GetDirectory(column):rfile.mkdir("GC/"+column)
        rfile.cd("GC/"+column)
        self.gcsets[name].multi[column].Draw("a")
        y_range=(self.gcsets[name].multi[column].GetYaxis().GetXmin(),self.gcsets[name].multi[column].GetYaxis().GetXmax())

        #Set range to zoom in on peaks for columns B and C, could probably be changed to use the user defined x range
        if   (column == "B"): self.gcsets[name].multi[column].GetXaxis().SetRangeUser(0.2,0.8)
        elif (column == "C"): self.gcsets[name].multi[column].GetXaxis().SetRangeUser(0.1,0.5)

        self.gcsets[name].multi[column].GetXaxis().SetTitle("Time (sec)")
        self.gcsets[name].multi[column].GetYaxis().SetTitle("Signal (#muV)")
        self.gcsets[name].multi[column].GetYaxis().SetTitleOffset(1.2)
        leg.Draw()
        self.canvases[cname].Write()
        c2=TCanvas(cname+"_logY","c2",1200,800)
        c2.SetLogy()
        logMulti.Draw("a")

        #Set range to zoom in on peaks for columns B and C and y axis values, could probably be changed to use the user defined x range
        if   (column == "B"): logMulti.GetXaxis().SetRangeUser(0.2,0.8);y_list=[yn[i] for i in range (npn) if 0.2 <= xn[i] <= 0.8 and yn[i] > 1];logMulti.GetYaxis().SetRangeUser(min(y_list)*10**(-0.5),max(y_list)*10**(2.2))
        elif (column == "C"): logMulti.GetXaxis().SetRangeUser(0.1,0.5);y_list=[yn[i] for i in range (npn) if 0.1 <= xn[i] <= 0.5 and yn[i] > 1];logMulti.GetYaxis().SetRangeUser(min(y_list)*10**(-0.5),max(y_list)*10**(2))
        
        logMulti.GetXaxis().SetTitle("Time (sec)")
        logMulti.GetYaxis().SetTitle("Signal (#muV)")
        logMulti.GetYaxis().SetTitleOffset(1.2)
        leg.Draw()
        c2.Write()

        #uncomment these to write y value histogram to file
        #c.Write()
        #self.canvases[cname].SaveAs(name+".png")
        rfile.Close()
    
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
            
           
