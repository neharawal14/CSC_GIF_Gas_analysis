#include<iostream>
using namespace std;

void analyze_Plot(){
TFile *f = TFile::Open("../Plot.root");
TDirectoryFile *base_dir = (TDirectoryFile*) f->Get("GC");
TDirectoryFile *B_dir = (TDirectoryFile *) base_dir->Get("B");
TCanvas *hist_B_voltage;
hist_B_voltage = (TCanvas *)B_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_B");
hist_B_voltage->SaveAs("B_first.pdf");

TCanvas *hist_B_voltage_second;
hist_B_voltage_second = (TCanvas *)B_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_B");
hist_B_voltage_second->SaveAs("B_second.pdf");

TCanvas *hist_B_voltage_third;
hist_B_voltage_third = (TCanvas *)B_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_B_logY");
hist_B_voltage_third->SaveAs("B_third.pdf");

/*TDirectoryFile *C_dir = (TDirectoryFile*)base_dir->Get("C");
TCanvas *C_voltage;
C_voltage = (TCanvas *)C_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_C");
C_voltage->SaveAs("C_first.pdf");

TCanvas *C_voltage_second;
C_voltage_second = (TCanvas *)C_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_C");
C_voltage_second->SaveAs("C_second.pdf");

TCanvas *C_voltage_third;
C_voltage_third = (TCanvas *)C_dir->Get("CSC_ME11ME21out8lh_0CF4_2bm_20211124_0070.AXY_C_logY");
C_voltage_third->SaveAs("C_third.pdf");

TDirectoryFile *drift_dir = (TDirectoryFile *) f->Get("drift");
TDirectoryFile *drift_B_dir = (TDirectoryFile *) drift_dir->Get("B");
TDirectoryFile *drift_C_dir = (TDirectoryFile *) drift_dir->Get("C");

TCanvas *drift_B_first;
drift_B_first = (TCanvas *)drift_B_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__B_BaseLineDrift");
drift_B_first->SaveAs("drift_B_BaseLine.pdf");

TCanvas *drift_C_first;
drift_C_first = (TCanvas *)drift_C_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__C_BaseLineDrift");
drift_C_first->SaveAs("dirft_C_BaseLine.pdf");

TCanvas *drift_B_second;
drift_B_second = (TCanvas *)drift_B_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__B_IntegralDrift");
drift_B_second->SaveAs("drift_B_IntegralDrift.pdf");

TCanvas *drift_C_second;
drift_C_second = (TCanvas *)drift_C_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__C_IntegralDrift");
drift_C_second->SaveAs("dirft_C_IntegralDrift.pdf");

TCanvas *drift_B_third;
drift_B_third = (TCanvas *)drift_B_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__B_PeakDrift");
drift_B_third->SaveAs("drift_B_PeakDrift.pdf");

TCanvas *drift_C_third;
drift_C_third = (TCanvas *)drift_C_dir->Get("CSC_calibr_1lh_10CF4_100mb_StandardConn_May17_2018__C_PeakDrift");
drift_C_third->SaveAs("dirft_C_PeakDrift.pdf");
*/
}
