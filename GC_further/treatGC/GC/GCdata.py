'''
Created on 21 Nov 2016

@author: kkuzn
'''
import pickle
from ROOT import TGraph
from ROOT import TMultiGraph
from ROOT import TH1F
from ROOT import TF1
import math
class GCdata(object):
    '''
    classdocs
    '''

    def __init__(self, fname):
        '''
        Constructor
        '''
        self.names = ["A", "B", "C"]
        self.graphs    = {}
        self.graphs_new    = {}
        self.multi     = {}
        self.avgraphs  = {}
        self.avgraphs_new  = {}
        self.ranges    = {}
        self.peaks     = {}
        self.peakNames = {}
        self.valleys   = {}
        self.width     = {}
        self.baselines = {}
        self.flat      = {}
        self.flaterror = {}
        self.slope     = {}
        self.integrals = {}
        self.interror  = {}
        self.sums      = {}
        self.yHisto    = {}
        self.text_file = open('scaling_values.txt',"a")
        try:
            with open(fname, 'r') as f:
                read_data = f.readlines()
                f.closed
        except:
            print "can't open file ", fname, "exiting..."
            exit()
            
        N = len(read_data[0].split(", "))
        if(N<=1):
            print "less than two column in file ", fname, ", exiting..."
            exit()
        if(N>4):
            print "more than tree data columns in file ", fname, ", will do only three of them..."
            N=4
        
        for i in range (0,N-1):
            #self.names will be A B C
            self.multi[self.names[i]]=TMultiGraph()
            self.multi[self.names[i]].SetTitle(self.names[i])
            self.graphs[self.names[i]]=TGraph()
            self.graphs_new[self.names[i]]=TGraph()
            self.ranges[self.names[i]]=[100000000000000, -100000000000000]
            self.graphs[self.names[i]].SetName(self.names[i])
            self.graphs[self.names[i]].SetTitle(self.names[i])
            self.graphs_new[self.names[i]].SetName(self.names[i])
            self.graphs_new[self.names[i]].SetTitle(self.names[i])
            self.graphs[self.names[i]].SetMarkerStyle(20)
            self.graphs[self.names[i]].SetMarkerSize(0.5)
        for datastring in read_data:
            dset = datastring.split(", ")
            for i in range (0,N-1):                
                np  = self.graphs[self.names[i]].GetN()
                val = float(dset[i+1])
                #print"************************************************************************ np ***********************************", np
                self.graphs[self.names[i]].SetPoint(np, float(dset[0]), val)
                #print i, np, dset[0], dset[i+1]
                #min max
                if(val>self.ranges[self.names[i]][1]):
                    self.ranges[self.names[i]][1] = val
                if(val<self.ranges[self.names[i]][0]):
                    self.ranges[self.names[i]][0] = val

        print "calling for afile functions ", fname
        self.normalize("B",[0.2,0.8])

    def normalize(self,column,x_range):
        if not(column in self.graphs.keys()):
            print "can't find graph ",column, "doing nothing"
            return
        '''
        Set the most probable y value to 1000 so that there is an easier comparison between all the GC data
        '''
        np = self.graphs[column].GetN()
        print "normalize function np values", np 
        x  = self.graphs[column].GetX()
        y  = self.graphs[column].GetY()
        self.avgraphs[column]=TGraph()
        self.avgraphs_new[column]=TGraph()
        self.yHisto[column] = []

#        print" graph all values before anything" 
#        for i in range(np):
#         print(x[i]),
       #min_y=self.graphs[column].GetYaxis().GetXmin()
       #print("minimum voltage value",min_y)

       # for the moments lets not shift anything in avgraph
        y_list = [ y[i] for i in range(np) if x_range[0] <=  x[i] <= x_range[1]] #make a list of y values in the desired range
        self.yHisto[column]=TH1F("y_value_"+column,"",50000,min(y_list),max(y_list)) 
        for i in range(len(y_list)):self.yHisto[column].Fill(y_list[i])
        min_y2=self.yHisto[column].GetXaxis().GetBinCenter(self.yHisto[column].GetMaximumBin()) #Get most common y value
        #print ("minimum y value from which we are normalizing",min_y2)
        yshift = [y[i]-min_y2+1000 for i in range(np)] #Shift all y values to the required values

#        print " y shifted value over whole spectrum for avg graphs in normalize function "
        for i in range(np):
#          print" normalize : avgraph ({},{},{})".format(i, x[i],yshift[i])
           self.avgraphs[column].SetPoint(i,x[i],yshift[i])
        #print("first few y values after normalizing")
        #print(yshift[0], "  ", yshift[1], "  ", yshift[200]) 
        
#        for i in range(50):print " all x-y  values in start for column ({},{})".format(x[i],y[i]), column
#        self.avgraphs[column].SetName(self.graphs[column].GetName())
  
          
    def setPeak(self, column,x_range):
        if not(column in self.graphs.keys()):
            print "can't find graph ",column, "doing nothing"
            return
        np = self.avgraphs[column].GetN()
        x  = self.avgraphs[column].GetX()
        y  = self.avgraphs[column].GetY()
        if type(x_range) != list or len(x_range) != 2:x_range=[0,5]
        y_list = [y[i] for i in range(np) if x_range[0] <= x[i] <= x_range[1]] #make list of y values in desired x range
        i_list = [i for i in range(np) if x_range[0] <= x[i] <= x_range[1]]
        yHisto=TH1F("y_value_"+column,"",50,min(y_list),max(y_list))
        for i in range(len(y_list)):yHisto.Fill(y_list[i])
        #doubtful - not clear why last bin would be larger than anyone
        yHisto.SetBinContent(1,0) #remove the last bin because it is usually much larger than any other
        
        self.peaks[column]=[]
        self.peakNames[column]=[]
        self.valleys[column]=[]
        self.flat[column]=[]
        self.flaterror[column]=[]
        
        sp,ep=min(i_list),max(i_list) #Set start points based off x range
        base_y,base_x,base_i=y[sp],x[sp],sp #values to compare the size of peaks
        prev_y,prev_x = y[sp],x[sp]
        stdev=yHisto.GetRMS()
        print "Standard Deviation used",stdev
        threshold=0.1*stdev #anything above this threshold has the chance to be marked as a peak, value was choosen to fit data
        hill=False
        for i in range(sp,ep):
            nPeaks=len(self.peaks[column])
            nValleys=len(self.valleys[column])
            if not hill:
                #print "was not a hill in start"
                #print "start y value ", y[i], prev_y
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
                            self.peaks[column].append([prev_x,prev_y,i-1])
                            self.peakNames[column].append(str(nPeaks))
                            #If no valleys have been found before a peak is found we use what ever the peaks height was compared to as the valley
                            if (nValleys == 0):self.valleys[column].append([base_x,base_y,base_i]);print "Setting start valley at",base_i,base_x,base_y
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
                            self.valleys[column].append([base_x,base_y,base_i])
                            hill=False

                    
            prev_x=x[i]
            prev_y=y[i]
       #if we ended on a hill without finding a valley we take the last base values as the last valley
        if hill: self.valleys[column].append([base_x,base_y,base_i]);print "Setting end valley at",base_i,base_x,base_y

        # print number of valleys and hills before flat check

        #print("number of peaks and number of valleys for column :  ",column," before flatcheck")
        print(len(self.peaks[column]))
        print(len(self.valleys[column]))
        for i in range(len(self.peaks[column])):
          print"peak values : x and y", self.peaks[column][i][0]," ", self.peaks[column][i][1]
        for i in range(len(self.valleys[column])):
          print"peak values : x and y", self.valleys[column][i][0]," ", self.valleys[column][i][1]
       #move valleys as close to the peaks without getting on them
        flatcheck = 50 #amount of points that are considered in the linear fit
        for iV in range(len(self.peaks[column])):
            i_i,i_f = self.valleys[column][iV][2],self.valleys[column][iV+1][2]
            y_1,y_2 = self.valleys[column][iV][1],self.valleys[column][iV+1][1]
            i_peak = self.peaks[column][iV][2]
           # print "i peak and i final peak values here" , i_i, "  ", i_f, "peak values here ", i_peak
            prevflat=-1
            fitslopeUp,fitslopeDo=-1,-1 #attempt at calculating uncertianty using physics analysis methods
            minChi2,minSlope=10**10,10**10 #debug variables
            for i in range(i_i,i_peak):
               # print "check values from first valley to the peak"
                if (y[i]-y_1 < threshold):
                    #fit 50 points with a line and use chi2 and slope to determine how flat section is
                    self.graphs[column].Fit('pol1','Q0','',x[i-flatcheck],x[i+flatcheck/5])
                    linearfit = self.graphs[column].GetFunction('pol1')
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
                self.flat[column].append(prevflat)
                self.flaterror[column].append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)]) #temporary Up and Down Uncertainty
                #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)])

            minChi2,minSlope=10**10,10**10
            prevflat,fitslopeUp,fitslopeDo=-1,-1,-1
            for i in range(i_f,i_peak,-1):
               # print "check values from second valley to the peak"
                if (y[i]-y_2 < threshold):# and (i_f-i > flatcheck):
                    avgY = [0.0,0.0]
                    self.graphs[column].Fit('pol1','Q0','',x[i-flatcheck/5],x[i+flatcheck])
                    linearfit = self.graphs[column].GetFunction('pol1')
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
                self.flat[column].append(prevflat)
                self.flaterror[column].append([(x[1]-x[0],x[1]-x[0]),(y[1],y[1]),(1,1)])
                #self.flaterror[column].append([(abs(prevflat[k]-fitslopeUp[k]),abs(prevflat[k]-fitslopeDo[k])) for k in range(3)])
            
     # a program to get 1st peak and valley values for the input file
    # it should be only called after getIntegral is called
    def getPeakValley(self, column):
        self.peak_y_value = self.peaks[column][0][1]
        self.peak_x_value = self.peaks[column][0][0]
        self.valley_x_value =  self.first_point_x
        self.valley_y_value =  self.first_point_y

    def getIntegral_modified(self,column):
        # in order to not take  CF4 into account  and integrating from Ar +CF4, 
        # means we have to ignore integrating between 1st and 2nd point, integrate between 1st and 3rd point
        np  = self.graphs[column].GetN()
        x   = self.graphs[column].GetX()
        y   = self.graphs[column].GetY()
        self.integrals[column] = []
        self.interror[column]  = [] #calculating error for integrals
        nValleys = len(self.valleys[column])
        self.width[column]=[]
        self.baselines[column]=[]
#        y_baseline = np*[None]
        # file to write the peaks and valleys for final integration
#        files = open('peak_valley.txt', 'w')
#        files.write('afile') 
         # for finding first closer point to peak and storing its value
        first_point=0

        print" graph all values when evaluating integral" 
#        for i in range(np):
#          print(x[i]),
 

#        for iV in range(len(self.peaks[column])):
#          print("peak x here: ",self.peaks[column][iV][0])
#          print("peak y here: ",self.peaks[column][iV][1] )
#        for iV in range(len(self.valleys[column])):
#          print("valley x here: ",self. valleys[column][iV][0])
#          print("valley y here: ",self.valleys[column][iV][1] )
        
        # popping out valleys and a peak and a flat for original curve
        if(len(self.peaks[column])==3):
          self.peaks[column].pop(1)
          self.valleys[column].pop(1)
          nValleys=3

        for i in range(nValleys-1):
            integral,integralUp,integralDo=0.0,0.0,0.0
            point_i,point_i_err = self.valleys[column][i],[(0.000333, 0.000333), (1, 1), (1, 1)]
            point_f,point_f_err = self.valleys[column][i+1],[(0.000333, 0.000333), (1, 1), (1, 1)]
            print" it is the reference curve with two peaks"
            print"length peak ",len(self.peaks[column])
            for m in range(len(self.peaks[column])):
              print" peaks",self.peaks[column][m][0]
            print"length valley ",len(self.valleys[column])
            for m in range(len(self.valleys[column])):
              print" peaks",self.valleys[column][m][0]
            print"length flat column and values",len(self.flat[column])
            for m in range(len(self.flat[column])):
              print" flat",self.flat[column][m][0]
            for p in range(len(self.flat[column])):
                #determine if there is a closer point to the peak than the marked valley
                #if self.peaks[column] == 3 and p ==3: i=2
                point=self.flat[column][p]
                pointerror=self.flaterror[column][p]
                if point_i[2] < point[2] < point_f[2]:
                    if point[2] < self.peaks[column][i][2]:point_i,point_i_err=point,pointerror
                    elif self.peaks[column][i][2] < point[2]:point_f,point_f_err=point,pointerror

            self.width[column].append(point_i)
            self.width[column].append(point_f)
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
            
            self.baselines[column].append((x[i_i],x[i_f]))

            slope =  (y[i_f]-y[i_i])/(x[i_f]-x[i_i])
            y_baseline= []
            print"slope of the line to find integral when nPeaks are",len(self.peaks[column]), " is :", slope

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

            self.interror[column].append((abs(integral-integralUp),abs(integral-integralDo))) #error given for both up and down
            self.integrals[column].append(integral)
            print "integral value for column ", column, "integral ", integral
            
        self.sums[column]=0.0
        
        print"integral errors Ar ",self.interror[column][0]
        print"integral errors Co2 ",self.interror[column][1]
        for i in self.integrals[column]:
            self.sums[column]+=i

        #calculating the error for the ratio
        for i in range(len(self.integrals[column])):
            error=(100*(self.integrals[column][i]/self.sums[column])*((self.interror[column][i][0]/self.integrals[column][i])**2+(sum(j*j for j in self.interror[column][0])/self.sums[column]))
                  ,100*(self.integrals[column][i]/self.sums[column])*((self.interror[column][i][1]/self.integrals[column][i])**2+(sum(j*j for j in self.interror[column][1])/self.sums[column])))
            print self.peakNames[column][i],100*self.integrals[column][i]/self.sums[column],"+",error[0],"-",error[1],"%"
 
# integrals in previous way , I just swapped individual x bases with x[i+1]-x[i] instead of x[1]-x[0]
    def getIntegral(self,column):
        np  = self.graphs[column].GetN()
        x   = self.graphs[column].GetX()
        y   = self.graphs[column].GetY()
        self.integrals[column] = []
        self.interror[column]  = [] #calculating error for integrals
        nValleys = len(self.valleys[column])
        self.width[column]=[]
        self.baselines[column]=[]

        # file to write the peaks and valleys for final integration
#        files = open('peak_valley.txt', 'w')
#        files.write('afile') 
         # for finding first closer point to peak and storing its value
        first_point=0

#        print" graph all values when evaluating integral not moidified" 
#        for i in range(np):
#          print(x[i]),
 
        for iV in range(len(self.peaks[column])):
          print("peak x here: ",self.peaks[column][iV][0])
          print("peak y here: ",self.peaks[column][iV][1] )

        for i in range(nValleys-1):
            integral,integralUp,integralDo=0.0,0.0,0.0
            point_i,point_i_err = self.valleys[column][i],[(0.000333, 0.000333), (1, 1), (1, 1)]
            point_f,point_f_err = self.valleys[column][i+1],[(0.000333, 0.000333), (1, 1), (1, 1)]
            for p in range(len(self.flat[column])):
                #determine if there is a closer point to the peak than the marked valley
                point=self.flat[column][p]
                pointerror=self.flaterror[column][p]
                if point_i[2] < point[2] < point_f[2]:
                    if point[2] < self.peaks[column][i][2]:point_i,point_i_err=point,pointerror
                    elif self.peaks[column][i][2] < point[2]:point_f,point_f_err=point,pointerror

            self.width[column].append(point_i)
            self.width[column].append(point_f)
            i_i,i_f = point_i[2],point_f[2]
            # storing the first closer point to the peak for future calculations
            # only store the first closer point and not after it
            if(first_point == 0): 
              self.first_point_x = x[i_i]  
              self.first_point_y = y[i_i]
              first_point = 1;
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
            
            self.baselines[column].append((x[i_i],x[i_f]))

            for j in range(i_i,i_f):
                dx=(x[j+1]-x[j])
                integral+=(y[j]-base)*dx

            #calculating Up and Down from shifting bounds in and out from the peak
            for j in range(i_i-i_i_e[0],i_f+i_f_e[0]):
                dx=(x[j+1]-x[j])
                integralUp+=(y[j]-base)*dx

            for j in range(i_i+i_i_e[1],i_f-i_f_e[1]):
                dx=(x[j+1]-x[j])
                integralDo+=(y[j]-base)*dx

            self.interror[column].append((abs(integral-integralUp),abs(integral-integralDo))) #error given for both up and down
            self.integrals[column].append(integral)
            print "integral value for column ", column, "integral ", integral
            
        self.sums[column]=0.0
        for i in self.integrals[column]:
            self.sums[column]+=i

        #calculating the error for the ratio
        for i in range(len(self.integrals[column])):
            error=(100*(self.integrals[column][i]/self.sums[column])*((self.interror[column][i][0]/self.integrals[column][i])**2+(sum(j*j for j in self.interror[column][0])/self.sums[column]))
                  ,100*(self.integrals[column][i]/self.sums[column])*((self.interror[column][i][1]/self.integrals[column][i])**2+(sum(j*j for j in self.interror[column][1])/self.sums[column])))
            print self.peakNames[column][i],100*self.integrals[column][i]/self.sums[column],"+",error[0],"-",error[1],"%"


# shifting both original and reference curve to same level basically setting the common y axis for first valley point for both original and ref curve
    def shiftGraph(self, column, shift_graph, shift_avgraph):
        if not(column in self.graphs.keys()):
            print "can't find graph ", column, "doing nothing"
            return
        # shifting also the graph points
        np_graph  = self.graphs[column].GetN()
        x_graph   = self.graphs[column].GetX()
        y_graph   = self.graphs[column].GetY()
        print "shift value ", shift_graph
        print "number of values",np_graph
        print "column",column

        for i in range(2000,2010):
             print "i -  x - y values ({},{},{}) ".format(i, x_graph[i], y_graph[i])
        print("*********y shifted values *******")
        for i in range(0,np_graph):                
             y_shifted_graph = y_graph[i]-shift_graph
             print(y_shifted_graph, " type x ",x_graph[i], " type y ",y_shifted_graph)
             self.graphs_new[column].SetPoint(i,x_graph[i],y_shifted_graph)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting graphs ({},{},{}) ".format(i, x_graph[i], y_shifted_graph)
        print " after shifting number of values graphs", np_graph
 
        np  = self.avgraphs[column].GetN()
        x   = self.avgraphs[column].GetX()
        y   = self.avgraphs[column].GetY()
        print "shift value ", shift_avgraph
        print "number of values",np
        print "column",column
        print " average graph values before shifting " 
        #for i in range(2000,2010):
        #     print "i -  x - y avgraphs values before shifting to common baseline ({},{},{}) ".format(i, x[i], y[i])
        for i in range (0,np): 
             y_shifted = y[i]-shift_avgraph
             self.avgraphs_new[column].SetPoint(i,x[i],y_shifted)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting avgraphs ({},{},{}) ".format(i, x[i], y_shifted)
        
        print" after shifting number of values avgraphs", np

      

# this function is to scale the Ar peak along y axis to match with the original curve
#peak_org_graphs , peak_org_avgraphs: peak point value for the original curve
#base_org_graphs , base_org_avgraphs : valley point value for the original curve
#peak_ref : peak point for the reference curve
#base_ref : valley point for the ref curve
#second_valley_ref_point : second valley point for the ref curve
    def shiftGraph_CO2(self, column, shift_graph, shift_avgraph, second_valley, third_valley):
        if not(column in self.graphs.keys()):
            print "can't find graph ", column, "doing nothing"
            return
        np  = self.avgraphs[column].GetN()
        x   = self.avgraphs[column].GetX()
        y   = self.avgraphs[column].GetY()
        print "shift value ", shift_avgraph
        print "number of values",np
        print "column",column
        print " average graph values before shifting " 
#        for i in range(np):
#           print "check here {},{} ".format(x[i] , y[i])

        for i in range(2000,2010):
             print "i -  x - y avgraphs values before shifting to common baseline ({},{},{}) ".format(i, x[i], y[i])
        for i in range (0,np): 
           if i in range(second_valley, np):
             y_shifted = y[i]-shift_avgraph
             self.avgraphs_new[column].SetPoint(i,x[i],y_shifted)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting avgraphs ({},{},{}) ".format(i, x[i], y_shifted)

           else :
              y_shifted = y[i]
              self.avgraphs_new[column].SetPoint(i,x[i],y_shifted)
        
        print" after shifting number of values avgraphs", np

        # shifting also the graph points
        np_graph  = self.graphs[column].GetN()
        x_graph   = self.graphs[column].GetX()
        y_graph   = self.graphs[column].GetY()
        print "shift value ", shift_graph
        print "number of values",np_graph
        print "column",column

        for i in range(2000,2010):
             print "i -  x - y values ({},{},{}) ".format(i, x_graph[i], y_graph[i])
        for i in range (np_graph):                
           if i in range(second_valley, np_graph):
             y_shifted_graph = y_graph[i]-shift_graph
             self.graphs[column].SetPoint(i,x_graph[i],y_shifted_graph)
             if(i>2000 and i<2011):
              print "i -  x - y values after shifting graphs ({},{},{}) ".format(i, x_graph[i], y_shifted_graph)

           else : 
             y_shifted = y_graph[i]
             self.graphs[column].SetPoint(i,x[i],y_shifted)

        print " after shifting number of values graphs", np_graph
 
    def scaleGC_peak(self, column, peak_org_graphs,base_org_graphs, peak_org_avgraphs, base_org_avgraphs, peak_ref, base_ref, second_valley_ref_point):
        if not(column in self.avgraphs.keys()):
            print "can't find graph ", column, "doing nothing"
            return
        np  = self.avgraphs[column].GetN()
        x   = self.avgraphs[column].GetX()
        y   = self.avgraphs[column].GetY()
        np_graph  = self.graphs[column].GetN()
        x_graph   = self.graphs[column].GetX()
        y_graph   = self.graphs[column].GetY()

 #       print" graph all values when before scaling" 
 #       for i in range(np):
 #         print(x_graph[i]), 

        print " before scaling " 
        print " base org graph and peak org graph : peak :  ",peak_org_graphs, " base : ",base_org_graphs 
        print " base org avgraph and peak org avgraph : peak :  ",peak_org_avgraphs, " base : ",base_org_avgraphs 
        print" graph all values between first peak and valley  when before scaling" 
        for i in range(base_ref, second_valley_ref_point):
          print"({},{})".format(x_graph[i],y_graph[i]), 
        print" av graph all values between first peak and valley  when before scaling" 
        for i in range(base_ref, second_valley_ref_point):
         print"({},{})".format(x[i],y[i]), 
 
#        for i in range(np): 
#            self.avgraphs[column].SetPoint(i,0.0,0.0)
#            self.graphs[column].SetPoint(i,0.0,0.0)
        print"base and peak y values for Ar peak in org"
        print" peak graphs ({})".format(peak_org_graphs)
        print" valley graphs ({})".format(base_org_graphs)
        print"base and peak y values for Ar peak in ref"
        print" peak graphs ({},{})".format(x_graph[peak_ref], y_graph[peak_ref])
        print" valley graphs ({},{})".format(x_graph[base_ref], y_graph[base_ref])

        
        for i in range(2000,2010):
             print "i -  x - y values avgraphs({},{},{}) ".format(i, x[i], y[i])
        for i in range(2000,2010):
             print "i -  x - y values graphs({},{},{}) ".format(i, x_graph[i], y_graph[i])

        y_scaled_graph=[]
        y_scaled = []
        print " base lll value ",base_ref 
        print " second ref  lll value ",second_valley_ref_point 

        self.text_file.write(' scale factor by which curve scaled Ar and CO2 :  ')
        scale_value = (peak_org_graphs-base_org_graphs)/(y_graph[peak_ref]-y_graph[base_ref]) 
        scale_value_file = repr(scale_value)
        self.text_file.write(scale_value_file)


        # scaling only the points that are between base ref and second valley ref point, other points remains the same
        # for the purporse of graphs
        for i in range (np_graph):                
             if i in range(base_ref, second_valley_ref_point):
                A_v = ( y_graph[i]-y_graph[base_ref])
                B_v = (peak_org_graphs-base_org_graphs)
                C_v = (y_graph[peak_ref]-y_graph[base_ref]) 
                print " in graph A : ",A_v
                print " in graph B : ",B_v
                print " in graph C : ",C_v
                scale_factor =  (( y_graph[i]-y_graph[base_ref]) * ((peak_org_graphs-base_org_graphs)/(y_graph[peak_ref]-y_graph[base_ref]) ))
                y_scaled_graph_value = y_graph[base_ref]+ (( y_graph[i]-y_graph[base_ref]) * ((peak_org_graphs-base_org_graphs)/(y_graph[peak_ref]-y_graph[base_ref])))
                y_scaled_graph.append(y_scaled_graph_value)
             else : 
                scale_factor = -500
                y_scaled_graph_value = y_graph[i]
                y_scaled_graph.append(y_scaled_graph_value)
             if(i>2000 and i<2010) :  print(y_scaled_graph_value, scale_factor)
             if(i>2000 and i<2011):   print "i -  x - y values after scaling graphs ({},{},{}) ".format(i, x_graph[i], y_scaled_graph[i])
#            print "i -  x - y values ({},{},{}) ".format(i, x[i], y[i])
#            print "i -  x- y shifted ({}, {},{})".format(i, x[i], y_shifted[i])
        print " avg graph base y value ",y[base_ref] 
        print " base lll value ",base_ref 
        print " second ref  lll value ",second_valley_ref_point 
        # for the purporse of avgraphs
        for i in range (np):     
             if i in range(base_ref, second_valley_ref_point):
                A_v_2 = ( y[i]-y[base_ref])
                B_v_2= (peak_org_avgraphs-base_org_avgraphs)
                C_v_2 = (y[peak_ref]-y[base_ref]) 
                print " in avgraph A : ",A_v_2
                print " in avgraph B : ",B_v_2
                print " in avgraph C : ",C_v_2
                scale_factor_new = (( y[i]-y[base_ref]) * ((peak_org_avgraphs-base_org_avgraphs)/(y[peak_ref]-y[base_ref]) ))
                y_scaled_value = y[base_ref] + scale_factor_new
                print "y avg graph in the peak ",y_scaled_value
                y_scaled.append(y_scaled_value)
             else : 
                scale_factor_new = 4
                y_scaled_value = y[i]
                print " y avg graph ",y_scaled_value
                y_scaled.append(y_scaled_value)
             if(i>2000 and i<2010) : print "  scale factor new avgraphs ", scale_factor_new
             if(i>2000 and i<2010) : print "i -  x - y values after scaling avgraphs ({},{},{}) ".format(i, x[i], y_scaled[i])
#            print "i -  x - y values ({},{},{}) ".format(i, x[i], y[i])
#            print "i -  x- y shifted ({}, {},{})".format(i, x[i], y_shifted[i])

#        for i in range(base_ref, second_valley_ref_point):
#             self.graphs[column].SetPoint(i,x_graph[i],y_scaled_graph[i])
#        for i in range(base_ref, second_valley_ref_point):
#             self.avgraphs[column].SetPoint(i,x[i],y_scaled[i])
        for i in range(np_graph):
             self.graphs[column].SetPoint(i,x_graph[i],y_scaled_graph[i])
        for i in range(np):
             self.avgraphs[column].SetPoint(i,x[i],y_scaled[i])


        print" graph all values after scaling between first valley and second valley" 
        for i in range(base_ref, second_valley_ref_point):
          print" ({},{})".format(x_graph[i], y_graph[i]),


# this function is to shift Ar peak along x axis : so as to match with original curve
# shift_Ar_peak : amount by which to shift along x axis
# base_ref : is the first valley point for the reference curve
#second_valley_ref : is the second valley point for the reference curve
    #    def shiftGC_peak(self, column, shift_Ar_peak, base_ref, second_valley_ref):
    #        if not(column in self.avgraphs.keys()):
    #            print "can't find graph ", column, "doing nothing"
    #            return
    #        np  = self.avgraphs[column].GetN()
    #        x   = self.avgraphs[column].GetX()
    #        y   = self.avgraphs[column].GetY()
    #        np_graph  = self.graphs[column].GetN()
    #        x_graph   = self.graphs[column].GetX()
    #        y_graph   = self.graphs[column].GetY()
    #
    # 
    ##        print"base and peak y values for Ar peak in org"
    ##        print" peak graphs ({})".format(peak_org_graphs)
    ##        print" valley graphs ({})".format(base_org_graphs)
    ##        print"base and peak y values for Ar peak in ref"
    ##        print" peak graphs ({},{})".format(x_graph[peak_ref], y_graph[peak_ref])
    ##        print" valley graphs ({},{})".format(x_graph[base_ref], y_graph[base_ref])
    #
    #
    #        x_new_ref = []
    #        x_new_ref_graph = []
    #        y_new_ref = []
    #        y_new_ref_graph = []
    #
    #
    #        print" graph all values before shifting for Ar " 
    #        for i in range(base_ref, second_valley_ref):
    #         print" ({},{},{})".format(i, x_graph[i], y_graph[i]),
    #
    #        for i in range (np):                
    #          #if i in range(base_ref, second_valley_ref):
    #           #if i in range(base_ref-shift_value, second_valley_ref-shift_value):
    #           # x_ref = x[i+shift_Ar_peak]
    #           # y_ref = y[i+shift_Ar_peak]
    #           # x_new_ref.append(x_ref)
    #           # y_new_ref.append(y_ref)
   #           #else: 
    #           #  x_new_ref.append(x[i])
    #           #  y_new_ref.append(y[i])
    #          
    #           if(math.copysign(1,shift_Ar_peak) > 0) : 
    #             # this is for the end points when you shift whole curve
    #             if( (i+shift_Ar_peak) >= np) : 
    #               x_ref = x[i]
    #               y_ref = y[i]
    #               print " it is called " 
    #             else : 
    #               x_ref = x[i+shift_Ar_peak]
    #               y_ref = y[i+shift_Ar_peak]
    #             x_new_ref.append(x_ref)
    #             y_new_ref.append(y_ref)
    #
    #           elif(math.copysign(1,shift_Ar_peak) < 0) :
    #             if( (i+shift_Ar_peak) < 0) : 
    #               x_ref = x[i] 
    #               y_ref = y[i]
    #               print " it is called opposite sign " 
    #             else : 
    #               x_ref = x[i+shift_Ar_peak]
    #               y_ref = y[i+shift_Ar_peak]
    #             x_new_ref.append(x_ref)
    #             y_new_ref.append(y_ref)
    #        
    #        for i in range(np):
    #           self.avgraphs[column].SetPoint(i,x_new_ref[i],y_new_ref[i]) 
    #         
    #        # for avgraphs
    #        for i in range (np_graph):                
    #          if(math.copysign(1,shift_Ar_peak) > 0): 
    #             # this is for the end points when you shift whole curve
    #             if( (i+shift_Ar_peak) >= np): 
    #               x_ref_graph = x_graph[i]
    #               y_ref_graph = y_graph[i]
    #             else : 
    #               x_ref_graph = x_graph[i+shift_Ar_peak]
    #               y_ref_graph = y_graph[i+shift_Ar_peak]
    #             x_new_ref_graph.append(x_ref_graph)
    #             y_new_ref_graph.append(y_ref_graph)
    #
    #          elif(math.copysign(1,shift_Ar_peak) < 0):
    #             if( (i+shift_Ar_peak) < 0): 
    #               x_ref_graph = x_graph[i] 
    #               y_ref_graph = y_graph[i]
    #             else : 
    #               x_ref_graph = x_graph[i+shift_Ar_peak]
    #               y_ref_graph = y_graph[i+shift_Ar_peak]
    #             x_new_ref_graph.append(x_ref_graph)
    #             y_new_ref_graph.append(y_ref_graph)
    #        
    #        for i in range(np):
    #          self.graphs[column].SetPoint(i,x_new_ref_graph[i],y_new_ref_graph[i]) 
    #
    #        print" graph all values after shifting Ar peak" 
    #         
    #        for i in range(0, second_valley_ref-shift_Ar_peak):
    #          print"({},{},{})".format(i, x_new_ref_graph[i],y_new_ref_graph[i]), 

#  functions written again and tweaking now : to shift Ar and CO2 peak separately
    def shiftGC_peak(self, column, shift_peak, base_ref, second_valley_ref):
        if not(column in self.avgraphs.keys()):
            print "can't find graph ", column, "doing nothing"
            return
        np  = self.avgraphs[column].GetN()
        x   = self.avgraphs[column].GetX()
        y   = self.avgraphs[column].GetY()
        np_graph  = self.graphs[column].GetN()
        x_graph   = self.graphs[column].GetX()
        y_graph   = self.graphs[column].GetY()

 
#        print"base and peak y values for Ar peak in org"
#        print" peak graphs ({})".format(peak_org_graphs)
#        print" valley graphs ({})".format(base_org_graphs)
#        print"base and peak y values for Ar peak in ref"
#        print" peak graphs ({},{})".format(x_graph[peak_ref], y_graph[peak_ref])
#        print" valley graphs ({},{})".format(x_graph[base_ref], y_graph[base_ref])


        x_new_ref = []
        x_new_ref_graph = []
        y_new_ref = []
        y_new_ref_graph = []


        print" graph all values before shifting for Ar " 
        for i in range(base_ref, second_valley_ref):
         print" ({},{},{})".format(i, x_graph[i], y_graph[i]),

        for i in range (np):                
         if i in range(base_ref + shift_peak - 20, second_valley_ref+shift_peak+ 20) : 
             x_ref = x[i]
             y_ref = y[i+shift_peak]
         else : 
              x_ref = x[i]
              y_ref = y[i]
         x_new_ref.append(x_ref)
         y_new_ref.append(y_ref)
        
        for i in range(np):
           self.avgraphs[column].SetPoint(i,x_new_ref[i],y_new_ref[i]) 
         
        # for avgraphs
        for i in range (np_graph):                
         if i in range(base_ref +shift_peak - 20, second_valley_ref+ shift_peak+ 20) : 
             x_ref_graph = x_graph[i]
             y_ref_graph = y_graph[i+shift_peak]
         else : 
             x_ref_graph = x_graph[i]
             y_ref_graph = y_graph[i]
         x_new_ref_graph.append(x_ref_graph)
         y_new_ref_graph.append(y_ref_graph)
       
        for i in range(np_graph):
          self.graphs[column].SetPoint(i,x_new_ref_graph[i],y_new_ref_graph[i]) 

        print" graph all values after shifting Ar peak" 
         
        for i in range(0, second_valley_ref-shift_peak):
          print"({},{},{})".format(i, x_new_ref_graph[i],y_new_ref_graph[i]), 


    def setPeakName(self,name,column,nPeak,peakName):
        if nPeak == -1:
         nPeak = len(self.peaks[column])
        for i in range(nPeak):
          print"*****************************" 
          print" peakname here ", peakName[i]
          print"*****************************" 
          self.peakNames[column][i] = peakName[i]
 
        #else:
        # self.peakNames[column][i] = peakName 
