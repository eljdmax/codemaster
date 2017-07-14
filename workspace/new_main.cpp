#include <cstdlib>
#include <iostream>
#include <math.h>  
#include <list>
#include <map>
#include <algorithm>

using namespace std;



void build_tree_max(unsigned int* tree1, unsigned int* tree2, unsigned int* A, unsigned int cur, unsigned int l, unsigned int r, unsigned int NN  ) {

    if( l==r ) {
		tree1[ NN*cur + l] = A[ l ] ;
		tree2[ NN*cur + l] = A[ l ] ;
		return;
    }
	
	unsigned int mid = l+(r-l)/2;
	build_tree_max(tree1, tree2, A, cur+1 , l , mid , NN); //Build left tree 
	build_tree_max(tree1, tree2, A, cur+1 , mid+1 , r , NN); //Build right tree
	
	
	unsigned int start = NN*cur + l ;
	
	unsigned int ptL = NN*(cur+1) + l;
	unsigned int endPtL = NN*(cur+1) + mid + 1;
	
	unsigned int ptR = NN*(cur+1) + mid + 1;
	unsigned int endPtR = NN*(cur+1) + r + 1;
	unsigned int pre = 0;
	while ( (ptL < endPtL) && (ptR < endPtR) ){
		if (tree1[ptL] <= tree1[ptR]) {
			tree1[start] = tree1[ptL];
			ptL += 1;
		} else {
e a			ptR += 1;
		}
		tree2[start] = pre^tree1[start];
		pre = tree2[start];
		start += 1;
	}
	for (unsigned int k=ptL; k < endPtL; k++) {
		tree1[start] = tree1[k];
		tree2[start] = pre^tree1[start];
		pre = tree2[start];
		start += 1;
	}
	
	for (unsigned int k = ptR; k< endPtR; k++) {
		tree1[start] = tree1[k];
		tree2[start] = pre^tree1[start];
		pre = tree2[start];
		start += 1;
	}
	

}


unsigned int query_max(unsigned int* tree1, unsigned int* tree2, unsigned int cur, unsigned int l, unsigned int r,  unsigned int x, unsigned int y,  unsigned int NN, unsigned int K  ) {

    if ( ( r<x ) || (l>y) ) {
		return 0;
    }
	
	if (l ==r) {
		if ( tree1[NN*cur + l ] <= K) {
			return tree2[NN*cur + l ];
		} else {
			return 0;
		}
	}
		
	if( (x<=l) && (r<=y) ) {
	    
	    unsigned int* top = std::upper_bound(tree1 + NN*cur+l, tree1 + NN*cur+r+1 ,K) ;
		//top = bisect.bisect_right(tree1, K, NN*cur+l , NN*cur +r + 1)
		unsigned int val = top - tree1;
		if (val == NN*cur+l) {
			return 0;
		}
		return tree2[val-1];
	}
		
	unsigned int mid=l+(r-l)/2;
		
	return query_max(tree1, tree2, cur+1, l, mid, x, y, NN, K ) ^ query_max(tree1, tree2, cur+1, mid+1, r, x, y, NN, K );
}


unsigned int recurs(list< pair<unsigned int, unsigned int> >* vertices,  unsigned int* ray_next, unsigned int* ray_pre, unsigned int* first, unsigned int top, unsigned int* magicA , unsigned int N) {
    
    unsigned int NN = 0, sizeRay = 0;
    
    list<pair<unsigned int, unsigned int>> queue = {};
    unsigned int queue_size = 0;
    
    for (pair<unsigned int, unsigned int> n : vertices[1]) {
        queue.push_back( make_pair(1, n.second) );
        queue.push_back( n );
        queue_size += 2;
    }
    
    bool* visited = new bool[N+1];
    for (unsigned int n =1; n < N+1; n++){
        visited[n] = false;
    }
    
    first[1] = sizeRay;
    
    unsigned int  pre = 1;
    pair<unsigned int, unsigned int> cur;
    
    while ( queue_size > 0) {
        cur = queue.back();
        queue.pop_back();
        queue_size -= 1;
        
        sizeRay += 1;
        
        if ( cur.first == pre) {
            continue;
        }
        
        
        magicA[NN] = cur.second;
        ray_next[sizeRay-1] = NN;
        ray_pre[sizeRay] = NN;
        
        NN += 1;
        
        
        pre = cur.first;
        
        if (first[cur.first] < top) {
            continue;
        }
        
        first[cur.first] = sizeRay; // ???
        
        for (pair<unsigned int, unsigned int> n : vertices[cur.first]) {
            if (first[n.first] < top) {
                continue;
            }
            queue.push_back( make_pair(cur.first, n.second) );
            queue.push_back(n);
            queue_size += 2;
        }
        
        
    }
    
    
    return NN;
    
}



int main(int argc, char** argv) {

    cin.sync_with_stdio(false);
    cout.sync_with_stdio(false);
    
    unsigned int T;
    cin >> T;
    
    
    for (unsigned int t=0; t < T; t++ ) {
        
        unsigned int N;
        cin >> N;
        
        list< pair<unsigned int, unsigned int> >* vertices = new  list< pair<unsigned int, unsigned int> >[N+1];
        for (unsigned int n=1; n < N+1; n++){
            vertices[n] = {};
        }
        

        unsigned int U,V,C;
        for (unsigned int n=0; n < N-1; n++){
            cin >> U >>V >> C;
            
            vertices[U].push_back( make_pair(V,C) );
            vertices[V].push_back( make_pair(U,C) );
        }
        
        
        
        unsigned int* ray_next = new  unsigned int[2*N] ;
        unsigned int* ray_pre = new  unsigned int[2*N] ;
        
        unsigned int sizeRay;
        
        unsigned int top = 3*N;
        unsigned int* first = new unsigned int[N+1];
        for (unsigned int n =1; n < N+1; n++){
            first[n] = top;
        }
        
        unsigned int* magicA = new  unsigned int[5*N] ;
        unsigned int NN = 1;
        NN = recurs(vertices, ray_next, ray_pre, first, top, magicA , N);
        
        delete[] vertices;
        
        /*
        for (unsigned int i =1; i < N+1; ++i){
            cout << first[i] << " ";
        }
        cout << endl;
        
        for (unsigned int i =0; i < NN; ++i){
            cout << magicA[i] << " ";
        }
        cout << endl;
        */
        
        unsigned int _exp = int(log2(NN) )  + 2;
        unsigned int* tree1 = new unsigned int[ NN * _exp ];
        unsigned int* tree2 = new unsigned int[ NN * _exp ];
        
        
        build_tree_max( tree1, tree2, magicA, 0 , 0 , NN-1 , NN);
        
        delete[] magicA;
        
        unsigned int M;
        cin >> M;
        
        unsigned int K, sol, fU, fV, x , y;
        for (unsigned int n=0; n < M; n++){
            cin >> U >> V >> K;
            sol = 0;
            if ( U ==V ) {
                cout << sol << endl;
                continue;
            }
            
            fU = first[U];
            fV = first[V];
            
            if ( fU < fV) {
                x = ray_next[fU]  ;
                y = ray_pre[fV] ;
                //sol = query_max(tree1, tree2 , 0, 0, NN - 1, x, y, NN,  K );
           
            } else {
                x = ray_next[fV]  ;
                y = ray_pre[fU] ;
                //sol = query_max(tree1, tree2 , 0, 0, NN - 1, x, y, NN,  K );
           
            }
            
           cout << sol << endl;
            
        }
        
        delete[] first, tree1, tree2, ray_next, ray_pre ;
        
    }
    
     
    
    return 0;
}