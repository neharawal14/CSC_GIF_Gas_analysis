# CSC_GIF_Gas_analysis
CSC GIF Gas chromatography study 

##### setup the environment first
```
cmsrel 
CMSSW_8_0_26_patch1
cd CMSSW_8_0_26_patch1/src/
cmsenv
```

#### Clone the repository from master branch
```
git clone --branch master git@github.com:neharawal14/CSC_GIF_Gas_analysis.git
```

##### To analyze the  GC file 
```
python readGC.py -f your_GC_file.AXY
```
Output will be saved in Plot.root file, to read plots from root file and save them in pdfs, you can use the below python script
this is an optional step , you can always open the root file and see plots
analyze_plot.py : path : GC/treatGC/GC/analyze_output/analyze_plot.py
```
python analyze_plot.py
```

important files
readGC.py : main program for the analysis : path : GC/treatGC/readGC.py
GC.py : file on which readGC depends : path : GC/treatGC/GC/GC.py
GCdata.py : another file for which readGC depends : path : GC/treatGC/GC/GCdata.py

