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
 
 
def update(tree,N,x,y,val):
	
	
	while ( x <= N):
		y1 = y
		while (y1 <= m_top):
			tree[x][y1] = tree[x].setdefault(y1,0) + val
			y1 += (y1 & -y1)
		x += (x & -x)
	
 
def read(tree,x,y):
	res = 0
	while x>0:
		y1 = y
		while y1>0:
			res += tree[x].setdefault(y1,0)
			y1 -= (y1 & -y1)
		x -= (x & -x)
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
		
def build_tree( tree, magicA, Code, cur , l , r ):
	if( l==r ):
		tree[cur] = Code[magicA[l]] #[ magicA[ l ] ]
		return
	mid = l+(r-l)/2
	build_tree(tree, magicA, Code, 2*cur+1 , l , mid ) #Build left tree 
	build_tree(tree, magicA, Code, 2*cur+2 , mid+1 , r ) #Build right tree
	LL = 2*cur+1
	LR = 2*cur+2
	tree[cur] = tree[LL] + tree[LR]
	#tree[cur] = [0] * (len(tree[LL]) + len(tree[LR]) ) #merge( tree[2*cur+1] , tree[2*cur+2] ); //Merging the two sorted arrays
	#merge(tree[cur], tree[LL], tree[LR])
	
	
	
	
 
 
def query( magicTree, cur, l, r, x, y, k) :
	if( r < x or l > y ):
		return 0 #[] #out of range
 
	if( x<=l and r<=y ) : #Binary search over the current sorted vector to find elements smaller than K
		#upper_bound(tree[cur].begin(),tree[cur].end(),K)-tree[cur].begin();
		return magicTree[cur] #bisect.bisect_right(magicTree[cur],k)
	mid=l+(r-l)/2
	LL = query(magicTree, 2*cur+1,l,mid,x,y,k)
	LR = query(magicTree, 2*cur+2,mid+1,r,x,y,k)
	#M = [0]* ( len(LL) + len(LR) ) 
	#merge(M,LL,LR)
	#return M
	
	return LL + LR
 
def recurs(L,R,l,r):
	
	if( l==r ):
		return 1 if L[r] != R[r] else 0
	
	mid = l+(r-l)/2
	c = 1 if L[mid] != R[mid] else 0
	
	return c + recurs(L,R,l,mid-1) + recurs(L,R,mid+1,r)
 
		
	
def main():
	
	import sys
	#from operator import itemgetter
	
	#pq = PriorityQueue()
	
	# L = map(int , sys.stdin.readline().strip().split())
	# R = map(int , sys.stdin.readline().strip().split())
	
	# s= time.time()
	# print recurs(L, R, 0, (10**6) -1 )
	# print time.time()-s 
	
	# N = 140
	
	# ini = 0
	# for k in range(1,N):
		# ini = (ini +1)*k
	
	# print ini
	
	#return 
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		N, Q = map(int , sys.stdin.readline().strip().split())
		A = map(int , sys.stdin.readline().strip().split())

		dist = {}
		for n in range(N):
			dist[A[n]] = dist.setdefault(A[n],0) + 1
		
		print dist
		
		order =  sorted(dist.keys(), key=lambda x : dist[x], reverse = True )
		
		Code = {}
		ini = 0
		for k in order:
			ini += 1
			Code[k] = ini
			ini = ini * dist[k]
			
		print Code
		
		 
		
		magicTree = [0]*(3*N) 
		build_tree(magicTree,A,Code,0,0,N-1)
		
		print magicTree
		
		#print query(magicTree,0,0,N-1,1,2,9)
		#print query(magicTree,0,0,N-1,4,5,9)
		
		
		
		for _ in range(Q):
			a, b, c, d = map(int , sys.stdin.readline().strip().split())
			print query(magicTree,0,0,N-1,a-1,b-1,9) , query(magicTree,0,0,N-1,c-1,d-1,9)
			# if  recurs( query(magicTree,0,0,N-1,a-1,b-1,9) , query(magicTree,0,0,N-1,c-1,d-1,9), 0, b-a ) <= 1:
				# print "YES"
			# else:
				# print "NO"
			
 
	

	

		#print query(magicTree,0,0,N-1,L-1,R-1,Y) - query(magicTree,0,0,N-1,L-1,R-1,X-1)
		

		
def test(A,reverse,L,R,X,Y):
	res = 0
	for i in range(X, Y+1):
		if not i in reverse:
			continue
		
		for j in range(L-1,R):
			cur = A[j]
			exp = 0
			while (cur % i == 0):
				cur = cur / i
				exp += 1
			res += exp
	
	return res
	
def generate():
	_str= ""
	for k in range(1,(10**6)+1):
		_str += str(k)+ " "
	
	print _str
	
	_str= ""
	for k in range(1,(10**6)+1):
		_str += str(k)+ " "
 
	print _str
	
	
if __name__ == "__main__":
	
	#s= time.time()
	main()
	#generate()
	#test()
	

	#print time.time()-s  