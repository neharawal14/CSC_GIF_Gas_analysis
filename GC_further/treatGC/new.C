    def scaleGC_peak(self, column, peak_org_graphs,base_org_graphs, peak_org_avgraphs, base_org_avgraphs, peak_ref, base_ref):
        if not(column in self.avgraphs.keys()):
            print "can't find graph ", column, "doing nothing"
            return
        np  = self.avgraphs[column].GetN()
        x   = self.avgraphs[column].GetX()
        y   = self.avgraphs[column].GetY()
        np_graph  = self.graphs[column].GetN()
        x_graph   = self.graphs[column].GetX()
        y_graph   = self.graphs[column].GetY()

#        print" graph all values when before scaling" 
#        for i in range(np):
#          print(x_graph[i]), 
 
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
        # for the purporse of graphs
        for i in range (np_graph):                
             scale_factor =  (( y_graph[i]-y_graph[base_ref]) * ((peak_org_graphs-base_org_graphs)/(y_graph[peak_ref]-y_graph[base_ref]) ))
             y_scaled_graph_value = y_graph[base_ref]+ (( y_graph[i]-y_graph[base_ref]) * ((peak_org_graphs-base_org_graphs)/(y_graph[peak_ref]-y_graph[base_ref])))
             y_scaled_graph.append(y_scaled_graph_value)
             if(i>2000 and i<2010) :  print(y_scaled_graph_value, scale_factor)
#             self.graphs[column].SetPoint(i,x_graph[i],y_scaled_graph)
             if(i>2000 and i<2011):
              print "i -  x - y values after scaling graphs ({},{},{}) ".format(i, x_graph[i], y_scaled_graph[i])
#            print "i -  x - y values ({},{},{}) ".format(i, x[i], y[i])
#            print "i -  x- y shifted ({}, {},{})".format(i, x[i], y_shifted[i])
 
        # for the purporse of avgraphs
        for i in range (np):                
             y_scaled_value = y[base_ref]+ (( y[i]-y[base_ref]) * ((peak_org_avgraphs-base_org_avgraphs)/(y[peak_ref]-y[base_ref])))
             y_scaled.append(y_scaled_value)
             if(i>2000 and i<2010) : print(y_scaled_value)
#             self.avgraphs[column].SetPoint(i,x[i],y_scaled)
             if(i>2000 and i<2011):
              print "i -  x - y values after scaling avgraphs ({},{},{}) ".format(i, x[i], y_scaled[i])
#            print "i -  x - y values ({},{},{}) ".format(i, x[i], y[i])
#            print "i -  x- y shifted ({}, {},{})".format(i, x[i], y_shifted[i])

        for i in range(np_graph):
             self.graphs[column].SetPoint(i,x_graph[i],y_scaled_graph[i])
        for i in range(np):
             self.avgraphs[column].SetPoint(i,x[i],y_scaled[i])

        print" graph all values after scaling" 
        for i in range(np):
          print(x_graph[i]),


