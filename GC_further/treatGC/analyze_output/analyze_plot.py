# program to print the plots from Plot.root file, it gives the GC plots with peak and valley and percentage of gas information
from ROOT import TFile, TDirectoryFile

# provide your input file name

org_file = 'CSC_ME21outNomFlow_10CF4_6bm_20211112_0023'
ref_file = 'CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070'
infile_org = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_'+org_file+'.root'
infile_ref = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_'+ref_file+'.root'

infile_cmp_first = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_comparisonfirst.root'
infile_cmp_second = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_comparisonsecond.root'
infile_cmp_third = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_comparisonthird.root'
infile_cmp_fourth = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/Plot_comparisonfourth.root'

results = '/afs/cern.ch/user/n/nrawal/work/CSC_GIF_Gas_analysis/CMSSW_8_0_26_patch1/src/GC_further/treatGC/analyze_output/10perCF4_12_0023/results/'
org_saving_name = results+'org_'+org_file+'.pdf'
org_saving_name_log = results+'org_'+org_file+'_logY.pdf'

ref_saving_name = results+'ref_'+ref_file+'.pdf'
ref_saving_name_log = results+'ref_'+ref_file+'_logY.pdf'



list_files = [infile_org, infile_ref,  infile_cmp_first, infile_cmp_second, infile_cmp_third, infile_cmp_fourth]
#list_files = [infile_org, infile_ref,  infile_cmp_first];
saving_name_canvas1 = [org_saving_name, ref_saving_name, results+'cmp_first.pdf', results+'cmp_second.pdf',results+'cmp_third.pdf',results+'cmp_fourth.pdf']
saving_name_canvas2 = [org_saving_name_log , ref_saving_name_log , results+'cmp_first_logY.pdf', results+'cmp_second_logY.pdf', results+'cmp_third_logY.pdf', results+'cmp_fourth_logY.pdf']
def get_TDir_name(tfile):
    """Return the name (str) of the TDirectoryFile in `tfile`."""
    all_keys = list(tfile.GetListOfKeys())
    for key in all_keys:
        name = key.GetName()
        obj = tfile.Get(name)
        if isinstance(obj, TDirectoryFile):
            return name
   
for index, input_root_file in enumerate(list_files):
    print("index ", index)
    print(" input root file ",input_root_file)
    tfile = TFile.Open(input_root_file, 'read')
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
        print("canvas names") 
        print(name_B)
        if("_logY" in name_B) :
          name_B2= name_B
        else:
          name_B1=name_B
        # use this name further to plot the canvas
    #name2 will be the log plot canvas
    #name1 will be the unscaled normal plot
    canvas1 = second_dir.Get(name_B1)
    canvas1.SaveAs(saving_name_canvas1[index])
    canvas2 = second_dir.Get(name_B2)
    canvas2.SaveAs(saving_name_canvas2[index])

#third_dir = base_dir.Get("C")
#all_keys_third_dir = list(third_dir.GetListOfKeys())
#for keys in all_keys_third_dir:
#    name_C = keys.GetName()
#    print("canvas names ") 
#    print(name_C)
#    if("AXY_C_log" in name_C):
#      name_C2= name_C
#    else:
#      name_C1=name_C
#    # use this name further to plot the canvas
#    
#canvasC1 = third_dir.Get(name_C1)
#canvasC1.SaveAs("C_first.pdf")
#canvasC2 = third_dir.Get(name_C2)
#canvasC2.SaveAs("C_second.pdf")
