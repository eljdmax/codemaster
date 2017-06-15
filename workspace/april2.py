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

def check_palin(dict):
	
	_sum = 0
	_pres = 0
	for i in range(1,10):
		_pres = max( _pres, dict[i])
		_sum += dict[i]%2
		
	_sum += dict[0]%2
	
	return ( _sum, _pres )
	
	# if _sum > 1:
		# return False
	
	# if _pres <=1:
		# return False
		
	# return True
	
	
def subs(dictA, dictB):
	res = list(dictA)
	
	for i in range(10):
		res[i] -= dictB[i]
	
	return res
	
def merge( C, A, B):
	ptA, lA = 0, len(A)
	ptB, lB = 0, len(B)
	
	pt = 0
	while ( ptA < lA)  and ( ptB < lB ):
		if A[ptA] <= B[ptB]:
			C[pt] = A[ptA]
			ptA += 1
		else:
			C[pt] = B[ptB]
			ptB += 1
		pt += 1
		
	for k in range(ptA,lA):
		C[pt] = A[k]
		pt += 1
		
	for k in range(ptB,lB):
		C[pt] = B[k]
		pt += 1
 
 
def build_tree( tree, magicA, cur , l , r ):
	if( l==r ):
		tree[cur] = magicA[ l ]
		return
	mid = l+(r-l)/2
	build_tree(tree, magicA, 2*cur+1 , l , mid ) #Build left tree 
	build_tree(tree, magicA, 2*cur+2 , mid+1 , r ) #Build right tree
	LL = 2*cur+1
	LR = 2*cur+2
	tree[cur] = [0] * (len(tree[LL]) + len(tree[LR]) ) #merge( tree[2*cur+1] , tree[2*cur+2] ); //Merging the two sorted arrays
	merge(tree[cur], tree[LL], tree[LR])

def query_top( magicTree, cur, l, r, x, y, k) :
	if( r < x or l > y ):
		return 0 #out of range
 
	if( x<=l and r<=y ) : #Binary search over the current sorted vector to find elements smaller than K
		#upper_bound(tree[cur].begin(),tree[cur].end(),K)-tree[cur].begin();
		return bisect.bisect_right(magicTree[cur],k)
	mid=l+(r-l)/2
	return query_top(magicTree, 2*cur+1,l,mid,x,y,k)+query_top(magicTree, 2*cur+2,mid+1,r,x,y,k)
	
	
def query_bot( magicTree, cur, l, r, x, y, k) :
	if( r < x or l > y ):
		return 0 #out of range
 
	if( x<=l and r<=y ) : #Binary search over the current sorted vector to find elements smaller than K
		#upper_bound(tree[cur].begin(),tree[cur].end(),K)-tree[cur].begin();
		return bisect.bisect_left(magicTree[cur],k)
	mid=l+(r-l)/2
	return query_bot(magicTree, 2*cur+1,l,mid,x,y,k)+query_bot(magicTree, 2*cur+2,mid+1,r,x,y,k)
	
def getDict(magicTree, N, l,r,x,y):
	
	print query_top( magicTree, 0, 0, N-1, l, r,y) - query_bot( magicTree, 0, 0, N-1, l, r,x)
	
def main():
	
	import sys
	from collections import deque
	
	
	N, M = map( int, sys.stdin.readline().strip().split()) 
	
	nums = [0]*10
	
	for i in range(10):
		nums[i] = [0]*N
	
	A = [0] * N
	
	
	for n in xrange(N):
		for i in range(10):
			nums[i][n] = []
		j = 0
		for k in  map( int, sys.stdin.readline().strip().split()) :
			nums[k][n].append(j)
			j += 1
	
	magicTree = [0]*10
	_mul = N * M* (int(math.log(N*M,2))+3) ##??
	for i in range(10):
		magicTree[i] = [0]*_mul
		build_tree(magicTree[i],nums[i],0,0,N-1)
	
	
	#print nums[0]
	#print magicTree[0]
	
	print getDict(magicTree[0], N, 0,1,0,2)  # top_i, bot_i, top_j, bot_j
	
	# _mul = N * (int(math.log(N,2))+3)
	# magicTree = [0]*_mul
	
	
	# build_tree(magicTree,A,0,0,N-1,M)
	
	# print getDict(magicTree, N, 0,N-1,0,M-1)

	
	
	
def test(A,L,R,X,Y):
	1
	
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
	
	s= time.time()
	main()
	print time.time()-s   
	
	#test()