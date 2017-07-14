#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
#from itertools import chain, combinations
import random
import bisect
 
 
#pi = pi / Decimal(10**100)


def build_tree_max( tree, A, cur , l , r ):
	if( l==r ):
		tree[cur] = [ A[l] , 0 ]  #  distance , dirty_val
		return
		
	mid = l+(r-l)/2
	build_tree_max(tree, A, 2*cur+1 , l , mid )
	build_tree_max(tree, A, 2*cur+2 , mid+1 , r )
	
	tree[cur] = [ min(tree[2*cur+1][0], tree[2*cur+2][0]) , 0 ]
 

def update_range_max(tree, cur, l, r, x, y, inc, dirty ) :
 
	if ( r<x  or l>y ) : 
		#if ( x<= l and r<=y ):
		tree[cur][0] += dirty
		tree[cur][1] += dirty
		return 
	
	if (l ==r):
		#print "Updating ", l
		tree[cur][0] += inc + dirty
		return
		
	if( x<=l and r<=y ) : 
		tree[cur][0] += inc + dirty
		#set it dirty
		tree[cur][1] += inc + dirty
		return
		
	mid=l+(r-l)/2
	
		
	update_range_max(tree, 2*cur+1, l, mid, x, y, inc, dirty + tree[cur][1]  )
	update_range_max(tree, 2*cur+2, mid+1, r, x, y, inc, dirty + tree[cur][1] )
	
	tree[cur][0] = min( tree[2*cur+1][0] , tree[2*cur+2][0] )
	tree[cur][1] = 0 #no longer dirty
 
 

def query_range_max(tree, cur, l, r, y) :
	
	if l == r:
		return tree[cur][0]
	
	res = float('Inf')
	
	while l != r:
		mid=l+(r-l)/2
		
		#apply dirty
		tree[2*cur+2][0] += tree[cur][1]
		tree[2*cur+2][1] += tree[cur][1]
		
		tree[2*cur+1][0] += tree[cur][1]
		tree[2*cur+1][1] += tree[cur][1]
		
		tree[cur][1] = 0
		
		if y == mid:
			return min(res , tree[2*cur+1][0])
		
		if y > mid :
			res = min(res , tree[2*cur+1][0])
			l = mid+1
			cur = 2*cur+2
		else:
			r = mid
			cur = 2*cur+1
			
	
	return min( res , tree[cur][0] )
	
 
	
def main():
	
	import sys
	#from collections import deque
	
	M = int(sys.stdin.readline().strip())
	
	for _ in range(M):
		N, D = map( int, sys.stdin.readline().strip().split() )
		
		pq = PriorityQueue()
		dq = PriorityQueue()
		
		sad = [0]*N
		num = [0]*N
		
		for n in xrange(N):
			Di, Ti, Si = map( int, sys.stdin.readline().strip().split() )
			
			sad[n] = Si
			num[n] = Ti
			
			dq.put ( (-( D-Di+1),n))
			pq.put((-Si, n))
		
		mapping = [0]*N
		
		A = [0]*N
		i = 0
		while (not dq.empty() ):
			(delta, n) = dq.get()
			mapping[n] = i
			A[i] = -delta
			i += 1
		
		exp = int( math.log(N,2)) + 1; 
		size = ( 1<<(exp+1) )
		
		#print A
		#print mapping
		
		tree = [0] * size
		build_tree_max(tree,A,0,0,N-1)
	
		#print tree
		
		#update_range_max(tree, 0, 0, N-1, 0, 2, -1, 0 )
		
		#print query_range_max(tree, 0, 0, N-1, 3 )

		while (not pq.empty() ):
			s, n = pq.get()
			
			new_n = mapping[n]
			
			max_cap = query_range_max(tree, 0, 0, N-1, new_n )
			
			delta = min (max_cap , num[n])
			if delta > 0:
				num[n] -= delta
				update_range_max(tree, 0, 0, N-1, 0, new_n, -delta, 0 )
			
			
	
		sadness = 0
		for n in xrange(N):
			sadness += num[n]*sad[n]
		
		print sadness
	
def test():
	d = 1
			
	
def generate():
	M = 10**5
	N = 1
	print N, M
	
	
	for n in range(N):
		_str = ""
		for m in range(M):
			_str += "0 "
		print _str
	
	
if __name__ == "__main__":
	
	#generate()
	
	#s= time.time()
	main()
	#print time.time()-s   
	
	#test() 
 