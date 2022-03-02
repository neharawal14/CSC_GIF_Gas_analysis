#include<iostream>
using namespace std;

void tmp_file(){
TFile *f = TFile::Open("../Plot.root");
//f.GetListOfKeys();
// f.GetListOfKeys() contains `TObject*`, but we know they are really `TKey*`
 for (TKey *key:<TKey*>(f->GetListOfKeys())) {
  std::cout << "key: " << key->GetName()
      << " points to an object of class: " << key->GetClassName() << '\n';
     }
}
