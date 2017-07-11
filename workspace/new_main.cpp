/* 
 * File:   main.cpp
 * Author: tchabole
 *
 * Created on May 27, 2014, 4:27 PM
 */

#include <cstdlib>
#include <cmath>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

unsigned long long int _modulo = (unsigned long long int) pow(10,9) + 7;
unsigned long long int _delta = (1L << 60) % _modulo;

unsigned long long int two_power(unsigned long long int L) {
    
    int _remain = L%60;    
    unsigned long long int _max = (L-_remain)/60;
    unsigned long long int _power = (1L << _remain) % _modulo;
    
    for (unsigned long long int j = 0; j<_max;j++){
        
        _power = (_power * _delta) % _modulo;
    }
    
    return _power;
}

/*
 * 
 */
int main(int argc, char** argv) {

    cin.sync_with_stdio(false);
    unsigned long long int  N;
    
    cin >> N;
    
    unsigned long long int* _data = (unsigned long long int*)malloc((N+1) * sizeof(unsigned long long int));
    
    //unsigned long long int* _cache = (unsigned long long int*)malloc(N * sizeof(unsigned long long int));
    
    _data[0] = 1;
    
    unsigned long long int K = 1;
    
    long data;
    unsigned long long int num;
    
    
    while (K<N+1) {
        cin >> num;
        unsigned long long int _power = two_power(num);
        _data[K] = 0;
        
        for (unsigned long long int i = K ; i > 0; i--) {
            _data[i] = ( _data[i] +  (_data[i-1]*_power) % _modulo )  % _modulo ;
        }
                
                
        K = K+1;
    }
    
    unsigned long long int _sum = 0;
    
    for (unsigned long long int i = 1 ; i< N+1; i++){
        _sum = (_sum + _data[i])%_modulo ; 
    }
    
    cout << _sum << "\n";
    
    return 0;
}

