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
 

class plots(object):
    '''
    classdocs
    '''
    gcsets    = {};
    canvases  = {};
    graphcount= {};
    legends   = {};
    #graphsets = {};
    colours = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
    colours_ref = [ROOT.kRed,ROOT.kBlue,ROOT.kMagenta+1,ROOT.kViolet+7,ROOT.kTeal+3,ROOT.kOrange+3]
    ncolours = 6


    # read files and make plots send two files and directories flag to initialize

    def __init__(self, files_or_dir_org, dir_flag_org, verb_org, pdfname_org, files_or_dir_ref, dir_flag_ref, verb_ref, pdfname_ref) :
        '''
        Constructor
        '''
#        self.output='Plot_comparison.root'
#        temp=TFile(self.output,"RECREATE")
#        temp.Close()
        gStyle.SetOptTitle(1);
        if dir_flag_org:
            print "opening directory org ", files_or_dir_org
            list_of_files_org = [(files_or_dir_org+"/"+f) for f in os.listdir(files_or_dir_org) if os.path.isfile(files_or_dir_org+"/"+f)]
            #print list_of_files
        else:
            print "files or dir original ", files_or_dir_org
            list_of_files_org = files_or_dir_org.split(",")

        if dir_flag_ref:
            print "opening directory ref ", files_or_dir_ref
            list_of_files_ref = [(files_or_dir_ref+"/"+f) for f in os.listdir(files_or_dir_ref) if os.path.isfile(files_or_dir_ref+"/"+f)]
            #print list_of_files
        else:
            print "files or dir reference ", files_or_dir_ref
            list_of_files_ref = files_or_dir_ref.split(",")

        self.readGCs(list_of_files_org, list_of_files_ref,verb_org)
 
    def readGCs(self,list_of_files_org, list_of_files_ref,verb=False):
        print " list of files from readGCs original ", list_of_files_org
        print " list of files from readGCs reference ", list_of_files_ref
        for afile in list_of_files_org:
            print "afile name : ", afile
            fname_org  = afile.split("/")[-1]
            print "fname in readGC ", fname_org
            if ".AXY" in fname_org:
                self.gcsets[fname_org] = GCdata.GCdata(afile)            
                column_names_org =self.gcsets[fname_org].graphs.keys()
                print "read ", afile, " for columns ", " ".join(cn for cn in column_names_org) 
        
        for afile in list_of_files_ref:
            print "afile name : ", afile
            fname_ref  = afile.split("/")[-1]
            print "fname in readGC ", fname_ref
            if ".AXY" in fname_ref:
                self.gcsets[fname_ref] = GCdata.GCdata(afile)            
                column_names_ref =self.gcsets[fname_ref].graphs.keys()
                print "read ", afile, " for columns ", " ".join(cn for cn in column_names_ref) 

    def setPeak(self, name_org, name_ref, column, peakName_org,peakName_ref, x_range):
         print " in setPeak keys ",self.gcsets.keys()
         print self.gcsets[name_org].graphs.keys()
         print self.gcsets[name_ref].graphs.keys()

         if not(name_org in self.gcsets.keys()) or not(column in self.gcsets[name_org].graphs.keys()) :
             print "can't find ", name_org, ", column ", column, " in data; doing nothing original one"
             return
         print "Setting peaks for",name_org,"column",column
         self.gcsets[name_org].normalize(column,x_range) #Set minimum point within range specified to 1000
         self.gcsets[name_org].setPeak(column,x_range) #Set peaks
         self.gcsets[name_org].getIntegral_modified(column) #Get the integrals of the peaks
         if not(name_ref in self.gcsets.keys()) or not(column in self.gcsets[name_ref].graphs.keys()) :
             print "can't find ", name_ref, ", column ", column, " in data; doing nothing reference one"
             return
         print "Setting peaks for",name_ref,"column",column
         self.gcsets[name_ref].normalize(column,x_range) #Set minimum point within range specified to 1000
         self.gcsets[name_ref].setPeak(column,x_range) #Set peaks
         self.gcsets[name_ref].getIntegral_modified(column) #Get the integrals of the peaks
 
         self.setPeakName(name_org,name_ref,column,-1,-1, peakName_org, peakName_ref) #Set peak names that are specified
 
    def setPeakName(self,name_org,name_ref,column,nPeak_org,nPeak_ref,peakName_org, peakName_ref):
         if nPeak_org == -1:
             nPeak_org = len(self.gcsets[name_org].peaks[column])
             for i in range(nPeak_org):
                 self.gcsets[name_org].peakNames[column][i] = peakName_org[i]
 
         else:
              self.gcsets[name_org].peakNames[column][i] = peakName_org

         if nPeak_ref == -1:
             nPeak_ref = len(self.gcsets[name_ref].peaks[column])
             for i in range(nPeak_ref):
                 self.gcsets[name_ref].peakNames[column][i] = peakName_ref[i]
 
         else:
              self.gcsets[name_ref].peakNames[column][i] = peakName_ref


    def plot_org_ref(self, name_org, column_org, name_ref, column_ref, filename):
#    def plotMulti(self,name,column):
        #cname=name_org+"_cmp_"+name_ref+"_"+column_org
        cname="cmp"+filename
        if not(name_org in self.gcsets.keys()) or not (column_org in self.gcsets[name_org].graphs.keys()):
            print "can't find ", name_org, ", column ", column_org, " in data; doing nothing"
            return
        #Used to look at histogram of y values over the x range specified
        #c=TCanvas(self.gcsets[name].yHisto[column].GetName()+"_"+name,"c",800,800)
        #self.gcsets[name].yHisto[column].Draw("HIST")
        #c.SaveAs(c.GetName()+".png")
        #os.system("mv "+c.GetName()+".png /afs/hep.wisc.edu/home/ekoenig4/public_html/CSC/GC/tempPlots/")

        #Fill Peak points to be overlayed on the GC graphs
        gPeak_org = [] #Used to overlay on raw GC data
        gnPeak_org= [] #Used to overlay on normalized GC data
        gPeak_ref = [] #Used to overlay on raw GC data
        gnPeak_ref= [] #Used to overlay on normalized GC data

        print(" name ", name_org, " and other " , name_ref)
        print("column name ", column_org, " and other " , column_ref)

        npPeaks_ref = len(self.gcsets[name_ref].peaks[column_ref]) 
        npPeaks_org = len(self.gcsets[name_org].peaks[column_org]) 
        x_org,y_org,np_org=self.gcsets[name_org].graphs[column_org].GetX(),self.gcsets[name_org].graphs[column_org].GetY(),self.gcsets[name_org].graphs[column_org].GetN()
        x_ref,y_ref,np_ref=self.gcsets[name_ref].graphs[column_ref].GetX(),self.gcsets[name_ref].graphs[column_ref].GetY(),self.gcsets[name_ref].graphs[column_ref].GetN()

        xn_org,yn_org,npn_org=self.gcsets[name_org].avgraphs[column_org].GetX(),self.gcsets[name_org].avgraphs[column_org].GetY(),self.gcsets[name_org].avgraphs[column_org].GetN()
        xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column_ref].GetX(),self.gcsets[name_ref].avgraphs[column_ref].GetY(),self.gcsets[name_ref].avgraphs[column_ref].GetN()

        # good thing is that from peak and valley list we just access the point value, and so if you are shifting graph along y axis , nothing  gonna change and you do not need to change peak and valley position
        # you have to do only the time when you are changing x positions ? 
        print " in org_ref function np org", npn_org
        print " in org_ref function np ref", npn_ref
        for i in range(npPeaks_org):
            gPeak_org.append(TGraph());gnPeak_org.append(TGraph())
            iP_org=self.gcsets[name_org].peaks[column_org][i][2]
            gPeak_org[i].SetPoint(0,x_org[iP_org],y_org[iP_org]);gnPeak_org[i].SetPoint(0,xn_org[iP_org],yn_org[iP_org])
            gPeak_org[i].SetMarkerColor(self.colours[i]);gnPeak_org[i].SetMarkerColor(self.colours[i])
            gPeak_org[i].SetMarkerSize(2);gnPeak_org[i].SetMarkerSize(2)
            gPeak_org[i].SetMarkerStyle(8);gnPeak_org[i].SetMarkerStyle(8)    

        for i in range(npPeaks_ref):
            gPeak_ref.append(TGraph());gnPeak_ref.append(TGraph())
            iP_ref=self.gcsets[name_ref].peaks[column_ref][i][2]
            gPeak_ref[i].SetPoint(0,x_ref[iP_ref],y_ref[iP_ref]);gnPeak_ref[i].SetPoint(0,xn_ref[iP_ref],yn_ref[iP_ref])
            gPeak_ref[i].SetMarkerColor(self.colours_ref[i]);gnPeak_ref[i].SetMarkerColor(self.colours_ref[i])
            gPeak_ref[i].SetMarkerSize(2);gnPeak_ref[i].SetMarkerSize(2)
            gPeak_ref[i].SetMarkerStyle(8);gnPeak_ref[i].SetMarkerStyle(8)    



        #Fill Peak Width points to be overlayed on the GC graphs
        gWidth_org = TGraph() #Used to overlay on raw GC data
        gnWidth_org = TGraph() # Used to overlay on normalized GC data
        npWidth_org = len(self.gcsets[name_org].width[column_org])
        gWidth_ref = TGraph() #Used to overlay on raw GC data
        gnWidth_ref = TGraph() # Used to overlay on normalized GC data
        npWidth_ref = len(self.gcsets[name_ref].width[column_ref])
        for i in range(npWidth_org):
            iV_org=self.gcsets[name_org].width[column_org][i][2]
            gWidth_org.SetPoint(i,x_org[iV_org],y_org[iV_org]);gnWidth_org.SetPoint(i,xn_org[iV_org],yn_org[iV_org])
        gWidth_org.SetMarkerColor(3);gnWidth_org.SetMarkerColor(3)
        gWidth_org.SetMarkerSize(2);gnWidth_org.SetMarkerSize(2)
        gWidth_org.SetMarkerStyle(8);gnWidth_org.SetMarkerStyle(8)
        
        leg_org= TLegend(0.5,0.85,0.88,0.98)

        logMulti_org=TMultiGraph()
        logMulti_org.Add(self.gcsets[name_org].avgraphs[column_org],"pl")
        self.gcsets[name_org].multi[column_org].Add(self.gcsets[name_org].graphs[column_org])
        
        maxI_org = len(str(round(max(self.gcsets[name_org].integrals[column_org]),2)))
        for i in range(npPeaks_org):
            self.gcsets[name_org].multi[column_org].Add(gPeak_org[i],"p")
            logMulti_org.Add(gnPeak_org[i],"p")

            #Calculate integrals and percentages as well as their respective errors
            #note: errors are still a work in progress so these need to be changed to reflect actual errors
            integral_org=str(round(self.gcsets[name_org].integrals[column_org][i],2))
            integral_error_org=(str(round(self.gcsets[name_org].interror[column_org][i][0],2)),str(round(self.gcsets[name_org].interror[column_org][i][1],2)))
            percentage_org=str(round(100*self.gcsets[name_org].integrals[column_org][i]/self.gcsets[name_org].sums[column_org],2))
            perc_error_org=(str(round(100*(self.gcsets[name_org].integrals[column_org][i]/self.gcsets[name_org].sums[column_org])*((self.gcsets[name_org].interror[column_org][i][0]/self.gcsets[name_org].integrals[column_org][i])**2+(sum(j*j for j in self.gcsets[name_org].interror[column_org][0])/self.gcsets[name_org].sums[column_org])),3))
                  ,str(round(100*(self.gcsets[name_org].integrals[column_org][i]/self.gcsets[name_org].sums[column_org])*((self.gcsets[name_org].interror[column_org][i][1]/self.gcsets[name_org].integrals[column_org][i])**2+(sum(j*j for j in self.gcsets[name_org].interror[column_org][1])/self.gcsets[name_org].sums[column_org])),3)))

            #Used for spacing in the legend entry
            s_org=maxI_org-len(integral_org)+2
            integral_org=" "*s_org+integral_org
            
            leg_org.AddEntry(gPeak_org[i],self.gcsets[name_org].peakNames[column_org][i]+": "+integral_org+" #pm ^{"+integral_error_org[0]+"}_{"+integral_error_org[1]+"} | "+percentage_org+" #pm ^{"+perc_error_org[0]+"}_{"+perc_error_org[1]+"}%","p")

        self.gcsets[name_org].multi[column_org].Add(gWidth_org,"p")
        logMulti_org.Add(gnWidth_org,"p")
#        self.gcsets[name_org].multi[column_org].SetName(name_org)

# for other reference file calculating everything

        #Fill Peak Width points to be overlayed on the GC graphs
        gWidth_ref = TGraph() #Used to overlay on raw GC data
        gnWidth_ref = TGraph() # Used to overlay on normalized GC data
        npWidth_ref = len(self.gcsets[name_ref].width[column_ref])
        gWidth_ref = TGraph() #Used to overlay on raw GC data
        gnWidth_ref = TGraph() # Used to overlay on normalized GC data
        npWidth_ref = len(self.gcsets[name_ref].width[column_ref])
        for i in range(npWidth_ref):
            iV_ref=self.gcsets[name_ref].width[column_ref][i][2]
            gWidth_ref.SetPoint(i,x_ref[iV_ref],y_ref[iV_ref]);gnWidth_ref.SetPoint(i,xn_ref[iV_ref],yn_ref[iV_ref])
        gWidth_ref.SetMarkerColor(28);gnWidth_ref.SetMarkerColor(28)
        gWidth_ref.SetMarkerSize(2);gnWidth_ref.SetMarkerSize(2)
        gWidth_ref.SetMarkerStyle(8);gnWidth_ref.SetMarkerStyle(8)
        
        leg_ref= TLegend(0.5,0.68,0.88,0.83)

        logMulti_ref=TMultiGraph()
        self.gcsets[name_ref].avgraphs[column_ref].SetMarkerColor(2)
        logMulti_ref.Add(self.gcsets[name_ref].avgraphs[column_ref],"pl")
        self.gcsets[name_ref].multi[column_ref].Add(self.gcsets[name_ref].graphs[column_ref])
#        self.gcsets[name_ref].multi[column_ref].SetMarkerColor(2)
        self.gcsets[name_ref].graphs[column_ref].SetMarkerColor(2) 
        maxI_ref = len(str(round(max(self.gcsets[name_ref].integrals[column_ref]),2)))
        for i in range(npPeaks_ref):
            self.gcsets[name_ref].multi[column_ref].Add(gPeak_ref[i],"p")
            logMulti_ref.Add(gnPeak_ref[i],"p")

            #Calculate integrals and percentages as well as their respective errors
            #note: errors are still a work in progress so these need to be changed to reflect actual errors
            integral_ref=str(round(self.gcsets[name_ref].integrals[column_ref][i],2))
            integral_error_ref=(str(round(self.gcsets[name_ref].interror[column_ref][i][0],2)),str(round(self.gcsets[name_ref].interror[column_ref][i][1],2)))
            percentage_ref=str(round(100*self.gcsets[name_ref].integrals[column_ref][i]/self.gcsets[name_ref].sums[column_ref],2))
            perc_error_ref=(str(round(100*(self.gcsets[name_ref].integrals[column_ref][i]/self.gcsets[name_ref].sums[column_ref])*((self.gcsets[name_ref].interror[column_ref][i][0]/self.gcsets[name_ref].integrals[column_ref][i])**2+(sum(j*j for j in self.gcsets[name_ref].interror[column_ref][0])/self.gcsets[name_ref].sums[column_ref])),3))
                  ,str(round(100*(self.gcsets[name_ref].integrals[column_ref][i]/self.gcsets[name_ref].sums[column_ref])*((self.gcsets[name_ref].interror[column_ref][i][1]/self.gcsets[name_ref].integrals[column_ref][i])**2+(sum(j*j for j in self.gcsets[name_ref].interror[column_ref][1])/self.gcsets[name_ref].sums[column_ref])),3)))

            #Used for spacing in the legend entry
            s_ref=maxI_ref-len(integral_ref)+2
            integral_ref=" "*s_ref+integral_ref
            
            leg_ref.AddEntry(gPeak_ref[i],self.gcsets[name_ref].peakNames[column_ref][i]+": "+integral_ref+" #pm ^{"+integral_error_ref[0]+"}_{"+integral_error_ref[1]+"} | "+percentage_ref+" #pm ^{"+perc_error_ref[0]+"}_{"+perc_error_ref[1]+"}%","p")

        self.gcsets[name_ref].multi[column_ref].Add(gWidth_ref,"p")
        logMulti_ref.Add(gnWidth_ref,"p")
#        self.gcsets[name_ref].multi[column_ref].SetName(name_ref)
         
        Plot_name = "cmp_plot_" + filename
 
        Plot_name = TMultiGraph() 
 
        self.output='Plot_comparison'+filename+'.root'
        temp=TFile(self.output,"RECREATE")
        temp.Close()
         
        rfile = TFile(self.output,"update")
        print "creating canvas ", cname            
        self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
        if not rfile.GetDirectory("GC_cmp"): rfile.mkdir("GC_cmp")
        rfile.cd("GC_cmp")
        if not rfile.GetDirectory(column_org):rfile.mkdir("GC_cmp/"+column_org)
        rfile.cd("GC_cmp/"+column_org)
        Plot_name.Add(self.gcsets[name_org].multi[column_org])
        Plot_name.Add(self.gcsets[name_ref].multi[column_ref])
        Plot_name.Draw("ap")
        Plot_name.GetXaxis().SetRangeUser(0.2,0.8)
        Plot_name.GetYaxis().SetRangeUser(100,10000000)
#        cmp_plot.GetYaxis().SetRangeUser(self.gcsets[name_org].multi[column_org].GetYaxis().GetXmin(),self.gcsets[name_org].multi[column_org].GetYaxis().GetXmax())
#        cmp_plot.GetYaxis().SetRangeUser(0,self.gcsets[name_org].multi[column_org].GetYaxis().GetXmax())
        #Set range to zoom in on peaks for columns B and C, could probably be changed to use the user defined x range
#        if   (column_org == "B"): self.gcsets[name_org].multi[column_org].GetXaxis().SetRangeUser(0.2,0.8)
#        if   (column_ref == "B"): self.gcsets[name_ref].multi[column_ref].GetXaxis().SetRangeUser(0.2,0.8)
#        elif (column_org == "C"): self.gcsets[name_org].multi[column_org].GetXaxis().SetRangeUser(0.1,0.5)

#        self.gcsets[name_org].multi[column_org].GetXaxis().SetTitle("Time (sec)")
#        self.gcsets[name_org].multi[column_org].GetYaxis().SetTitle("Signal (#muV)")
#        self.gcsets[name_org].multi[column_org].GetYaxis().SetTitleOffset(1.2)
        Plot_name.GetXaxis().SetTitle("Time (sec)")
        Plot_name.GetYaxis().SetTitle("Signal (#muV)")
        Plot_name.GetYaxis().SetTitleOffset(1.2)
        leg_org.Draw()
        leg_ref.Draw()
        self.canvases[cname].Write()
       
        logMulti_all=TMultiGraph()

        c2=TCanvas(cname+"_logY","c2",1200,800)
        c2.SetLogy()
        logMulti_all.Add(logMulti_org)
        logMulti_all.Add(logMulti_ref)
        logMulti_all.Draw("ap")
         
        print" printing x[i] - y[i] values avg graphs org "
        for i in range(2000,2010):
          print "({},{})".format(xn_org[i], yn_org[i])
        print" printing x[i] - y[i] values avg graphs ref "
        for i in range(2000,2010):
          print "({},{})".format(xn_ref[i], yn_ref[i])
        #Set range to zoom in on peaks for columns B and C and y axis values, could probably be changed to use the user defined x range
        if   (column_org == "B"): y_list_org=[yn_org[i] for i in range (npn_org) if 0.2 <= xn_org[i] <= 0.8 and yn_org[i] > 1];
#        for i in range(npn_org):
#          if 0.2<= xn_org[i] <=0.8:
#              print " y_list _org( {},{})".format(xn_org[i], y_list_org[i])
#        logMulti_org.GetYaxis().SetRangeUser(min(y_list_org)*10**(-0.5),max(y_list_org)*10**(2.2))
#        logMulti_org.GetXaxis().SetRangeUser(0.2,0.8)
        if (column_ref == "B"): y_list_ref=[yn_ref[i] for i in range (npn_ref) if 0.2 <= xn_ref[i] <= 0.8 and yn_ref[i] > 1];
#        logMulti_ref.GetYaxis().SetRangeUser(min(y_list_ref)*10**(-0.5),max(y_list_ref)*10**(2.2))
#        logMulti_ref.GetXaxis().SetRangeUser(0.2,0.8)
#        for i in range(npn_ref):
#          if 0.2<= xn_ref[i] <=0.8: 
#              print " y_list _ref( {},{})".format(xn_ref[i], y_list_ref[i]) 
        if(column_org =="B") :
          if (min(y_list_org)*10**(-0.5) > min(y_list_ref)*10**(-0.5)): 
              logMulti_all.GetYaxis().SetRangeUser(min(y_list_ref)*10**(-0.5),max(y_list_org)*10**(2.2))
          else:   
              logMulti_all.GetYaxis().SetRangeUser(min(y_list_org)*10**(-0.5),max(y_list_org)*10**(2.2))
          logMulti_all.GetXaxis().SetRangeUser(0.2,0.8) 
        logMulti_all.GetXaxis().SetTitle("Time (sec)")
        logMulti_all.GetYaxis().SetTitle("Signal (#muV)")
        logMulti_all.GetYaxis().SetTitleOffset(1.2)
        leg_org.Draw()
        leg_ref.Draw()
        c2.Write()

        #uncomment these to write y value histogram to file
        #c.Write()
        #self.canvases[cname].SaveAs(name+".png")
        rfile.Close()
            
   
#    def plotGC(self, name, column, newflag, oldname="", oldcolumn=""):
#        if not(name in self.gcsets.keys()) or not(column in self.gcsets[name].graphs.keys()) :
#            print "can't find ", name, ", column ", column, " in data; doing nothing"
#            return
#        cname=name+"_"+column
#        if newflag:
#            print "creating canvas ", cname            
#            self.canvases[cname] = TCanvas(cname, cname, 1200, 800)
#            self.gcsets[name].graphs[column].Draw("APL")
#            self.graphcount[cname]=1
#        else:
#            oldcname=oldname+"_"+oldcolumn
#            if not(oldcname in self.canvases.keys()):
#                print "please first draw ", oldname, ", column ", oldcolumn, "; doing nothing"
#                return 
#            self.canvases[oldcname].cd()
#            self.gcsets[name].graphs[column].SetLineColor(self.colours[self.graphcount[oldcname]])
#            self.gcsets[name].graphs[column].SetMarkerColor(self.colours[self.graphcount[oldcname]])
#            self.gcsets[name].graphs[column].Draw("PLsames")
#            self.graphcount[oldcname]=self.graphcount[oldcname]+1
#            if not(oldcname in self.legends.keys()):
#                l=TLegend(0.4,0.75,0.9,0.9)
#                l.SetFillStyle(0)
#                l.SetBorderSize(0)
#                l.AddEntry(self.gcsets[oldname].graphs[oldcolumn],oldcname,"PL")
#                self.legends[oldcname]=l
#            l.AddEntry(self.gcsets[name].graphs[column],cname,"PL")
#            l.Draw()
#            self.canvases[oldcname].Update()


            
    def shiftGC_baseline(self, name_org,name_ref, column):
                   # to evaulate the value to shift 
          # first peak and first valley
         peak_org=self.gcsets[name_org].peaks[column][0][2]
         peak_ref=self.gcsets[name_ref].peaks[column][0][2]
         valley_org=self.gcsets[name_org].width[column][0][2]
         valley_ref=self.gcsets[name_ref].width[column][0][2]

         # values of graphs 
         x_org,y_org,np_org=self.gcsets[name_org].graphs[column].GetX(),self.gcsets[name_org].graphs[column].GetY(),self.gcsets[name_org].graphs[column].GetN()
         x_ref,y_ref,np_ref=self.gcsets[name_ref].graphs[column].GetX(),self.gcsets[name_ref].graphs[column].GetY(),self.gcsets[name_ref].graphs[column].GetN()

         # values of avgraphs
         xn_org,yn_org,npn_org=self.gcsets[name_org].avgraphs[column].GetX(),self.gcsets[name_org].avgraphs[column].GetY(),self.gcsets[name_org].avgraphs[column].GetN()
         xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column].GetX(),self.gcsets[name_ref].avgraphs[column].GetY(),self.gcsets[name_ref].avgraphs[column].GetN()
 
         shift_valley_org_graphs = y_org[valley_org] - 500.0
         shift_valley_ref_graphs = y_ref[valley_ref] - 500.0

         shift_valley_org_avgraphs = yn_org[valley_org] - 500.0
         shift_valley_ref_avgraphs = yn_ref[valley_ref] - 500.0
         
         print " np in plot org_ref function org graph ",np_org
         print " np in plot org_ref function ref graph ",np_ref

         print"shift valley org graph" ,shift_valley_org_graphs
         print"shift valley ref graph", shift_valley_ref_graphs



         print " np in plot org_ref function org ",npn_org
         print " np in plot org_ref function ref ",npn_ref

         print"shift valley org avgraph" ,shift_valley_org_avgraphs
         print"shift valley ref avgraph", shift_valley_ref_avgraphs

         print" printing x[i] - y[i] values  graphs org before shifting avgraphs"
         for i in range(2000,2010):
          print "({},{})".format(x_org[i], y_org[i])
         print" printing x[i] - y[i] values graphs ref before shifting avgraphs"
         for i in range(2000,2010):
          print "({},{})".format(x_ref[i], y_ref[i])
 
         print" printing x[i] - y[i] values avg graphs org before shifting graphs"
         for i in range(2000,2010):
          print "({},{})".format(xn_org[i], yn_org[i])
         print" printing x[i] - y[i] values avg graphs ref before shifting graphs"
         for i in range(2000,2010):
          print "({},{})".format(xn_ref[i], yn_ref[i])
 

         # since yn_org  already declared from before and so it is fine to use it here directly
         if not(name_org in self.gcsets.keys()) or not (column in self.gcsets[name_org].graphs.keys()):
             print "can't find ", name_org, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_org].shiftGraph(column, shift_valley_org_graphs, shift_valley_org_avgraphs)

         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
             print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_ref].shiftGraph(column, shift_valley_ref_graphs, shift_valley_ref_avgraphs)
 
    def scaleGC_first_peak(self, name_org,name_ref, column):
                   # to evaulate the value to shift 
          # first peak and first valley
         peak_org=self.gcsets[name_org].peaks[column][0][2]
         peak_ref=self.gcsets[name_ref].peaks[column][0][2]
         valley_org=self.gcsets[name_org].width[column][0][2]
         valley_ref=self.gcsets[name_ref].width[column][0][2]

         xn_org,yn_org,npn_org=self.gcsets[name_org].avgraphs[column].GetX(),self.gcsets[name_org].avgraphs[column].GetY(),self.gcsets[name_org].avgraphs[column].GetN()
         xn_ref,yn_ref,npn_ref=self.gcsets[name_ref].avgraphs[column].GetX(),self.gcsets[name_ref].avgraphs[column].GetY(),self.gcsets[name_ref].avgraphs[column].GetN()
        # shift_peak_org = yn_org[peak_org] - 500.0
         shift_peak_ref = (yn_org[peak_ref]/yn_ref[peak_ref])

         print " np in plot org_ref function org ",npn_org
         print " np in plot org_ref function ref ",npn_ref

         print"scale peak org" ,shift_valley_org
         print"shift valley ref", shift_valley_ref

         print" printing x[i] - y[i] values avg graphs org before scaling , shifted once to baseline"
         for i in range(2000,2010):
          print "({},{})".format(xn_org[i], yn_org[i])
         print" printing x[i] - y[i] values avg graphs ref before scaling, shifted once to baseline"
         for i in range(2000,2010):
          print "({},{})".format(xn_ref[i], yn_ref[i])
 

         # since yn_org  already declared from before and so it is fine to use it here directly
         if not(name_org in self.gcsets.keys()) or not (column in self.gcsets[name_org].graphs.keys()):
             print "can't find ", name_org, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_org].shiftGraph(column, shift_valley_org)

         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
             print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_ref].shiftGraph(column, shift_valley_ref)
 
    def scaleGCx(self, name_org, name_ref, column):
         if not(name_org in self.gcsets.keys()) or not (column in self.gcsets[name_org].graphs.keys()):
             print "can't find ", name_org, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_org].scaleGraphx(column, value) 
         if not(name_ref in self.gcsets.keys()) or not (column in self.gcsets[name_ref].graphs.keys()):
             print "can't find ", name_ref, ", column ", column, " in data; doing nothing"
             return
         self.gcsets[name_ref].scaleGraphx(column, value) 
