# program to print the plots from Plot.root file, it gives the GC plots with peak and valley and percentage of gas information
from ROOT import TFile, TDirectoryFile

# provide your input file name
infile = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/Plot.root'
tfile = TFile.Open(infile, 'read')

def get_TDir_name(tfile):
    """Return the name (str) of the TDirectoryFile in `tfile`."""
    all_keys = list(tfile.GetListOfKeys())
    for key in all_keys:
        name = key.GetName()
        obj = tfile.Get(name)
        if isinstance(obj, TDirectoryFile):
            return name

# Returns 'Ana'.
dir_name = get_TDir_name(tfile)
print(dir_name)

# Opening base dir which is "GC" in our case
base_dir = tfile.Get(dir_name)

#inside GC we have other directory with name "B" and "C" 
# each of "B" and "C" holds the unscaled plots and log plots for column B and C , respectively  
second_dir = base_dir.Get("B")

all_keys_second_dir = list(second_dir.GetListOfKeys())
for keys in all_keys_second_dir:
    name_B = keys.GetName()
    print("canvas names ") 
    print(name_B)
    if("AXY_B_log" in name_B) :
      name_B2= name_B
    else:
      name_B1=name_B
    # use this name further to plot the canvas
#name2 will be the log plot canvas
#name1 will be the unscaled normal plot
canvas1 = second_dir.Get(name_B1)
canvas1.SaveAs("B_first.pdf")
canvas2 = second_dir.Get(name_B2)
canvas2.SaveAs("B_second.pdf")

third_dir = base_dir.Get("C")

all_keys_third_dir = list(third_dir.GetListOfKeys())
for keys in all_keys_third_dir:
    name_C = keys.GetName()
    print("canvas names ") 
    print(name_C)
    if("AXY_C_log" in name_C):
      name_C2= name_C
    else:
      name_C1=name_C
    # use this name further to plot the canvas
    
canvasC1 = third_dir.Get(name_C1)
canvasC1.SaveAs("C_first.pdf")
canvasC2 = third_dir.Get(name_C2)
canvasC2.SaveAs("C_second.pdf")
