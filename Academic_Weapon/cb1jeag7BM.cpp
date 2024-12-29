#include <iostream>
#include <vector>

using namespace std;

bool dicho(int val, vector<int> t){
    int fin = t.size()-1;
    int debut =0;
    while (debut <= fin){
        int milieu = (debut + fin) /2;
        if(t[milieu] == val){
            return true;
        }else if (t[milieu] > val){
            fin = milieu -1;
        }else{
            debut = milieu + 1;
        }
    }
    return false;
}

int main(){
    vector<int> v = {1,2,3,4,5,6};
    cout <<  dicho(6, v);
}