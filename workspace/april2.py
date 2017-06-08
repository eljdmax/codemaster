#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
#from itertools import chain, combinations
import random
import bisect
 
#filters = 5
#_modulo = [100663319, 201326611, 402653189, 1610612741, 805306457] 

filters = 1
_modulo = [100663319] 

#filters = 2
#_modulo = [100663319, 201326611] 
 
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
		
def build_tree( tree, magicA, tree2,  A, cur , l , r ):
	if( l==r ):
		index = magicA[ l ]
		tree[cur] = [ index ]
		
		#cumul sum of elements in tree 
		tree2[cur] = [0]*2
		tree2[cur][0] = [0]*filters
		tree2[cur][1] = [0]*filters
		for y in range(filters):
			tree2[cur][1][y] =  A[index]  % _modulo[y] #??
		return
	mid = l+(r-l)/2
	build_tree(tree, magicA, tree2, A, 2*cur+1 , l , mid ) #Build left tree 
	build_tree(tree, magicA, tree2, A, 2*cur+2 , mid+1 , r ) #Build right tree
	LL = 2*cur+1
	LR = 2*cur+2
	
	TL = len(tree[LL]) + len(tree[LR])
	tree[cur] = [0] * TL #merge( tree[2*cur+1] , tree[2*cur+2] ); //Merging the two sorted arrays
	tree2[cur] = [0] * (TL+1)
	
	merge(tree[cur], tree[LL], tree[LR])
	
	tree2[cur][0] = [0]*filters
	for k in range(TL):
		tree2[cur][k+1] = [0]*filters
		for y in range(filters):
			tree2[cur][k+1][y] = (tree2[cur][k][y] + A[tree[cur][k]] ) % _modulo[y]
	
	
	#cumul sum of elements in treecur
		# ??
 
 
 
def query( magicTree, magicTree2, rev, N, x, y, k) :
	
	_sum = [0]*filters
	
	if k == 0:
		return _sum
	
	
	cur = 0
	l = 0
	r = N-1
	while (l != r ):
		mid=l+(r-l)/2
		
		part = 2*cur + 1
		index_x = bisect.bisect_left( magicTree[part], x)
		index_y = bisect.bisect_right( magicTree[part], y)
		low = index_y - index_x
		
		if (low >= k):
			cur = 2*cur + 1
			r = mid
		else:
			for y in range(filters):
				_sum[y]  += magicTree2[part][index_y][y] - magicTree2[part][index_x][y]
				
			cur = 2*cur + 2
			l = mid+1
			k -= low
	
	for y in range(filters):
		_sum[y]  = ( rev[l] + _sum[y] ) % _modulo[y]
	
	return _sum
	#return ( rev[l], _sum + rev[l])
	
	
def check( A,B):
	for y in range(filters):
		if A[y] != B[y]:
			return False
	return True
	
def subs( C,A,B):
	for y in range(filters):
		C[y] = (A[y] - B[y]) % _modulo[y]
 
def recurs(L,R,l,r):
	
	if( l==r ):
		return 1 if L[r] != R[r] else 0
	
	mid = l+(r-l)/2
	c = 1 if L[mid] != R[mid] else 0
	
	return c + recurs(L,R,l,mid-1) + recurs(L,R,mid+1,r)
 
		
	
def main():
	
	import sys
 
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		N, Q = map(int , sys.stdin.readline().strip().split())
		A = map(int , sys.stdin.readline().strip().split())
		
		# N = 343
		# _max = 10**5
		# k = 1
		# # = list(range(2, N+1, 2))#[ random.randint(1,1000) for k in range(N/2) ]
		# A = []
		# while k < N:
			# for i in range(k):
				# A.append(_max)
			# _max -= 2
			# k += 1
		
		# N = len(A)
		# B = list(A)
		
		# B[N-1] = 1
		# #B[6] = 2*7 - 1
		
		# A.extend(B)
		# print len(A)
		
		# N = 2*N
		
		
		dist = {}
		for n in range(N):
			dist[A[n]] = dist.setdefault(A[n],0) + 1
		
		#print dist
		
		order = dist.keys() #sorted(dist.keys() )
		
		Code = {}
		ini = 0
		for k in order:
			ini += 1
			Code[k] = ini
			ini = ini * dist[k]
		
		# NewCode = {}
		# for k in order:
			# NewCode[k] = [0] * filters
			# for y in range(filters):
				# NewCode[k][y] = Code[k] % _modulo[y]
		
		#print ini
		print Code
		
		order = None
		#Code = None
		
		cumul = [0]*(N+1)
		for k in range(N):
			cumul[k+1] = cumul[k] + Code[A[k]]
			
		# cumul[0]  = [0]*filters
		# for k in range(N):
			# cumul[k+1] = [0]*filters
			# for y in range(filters):
				# cumul[k+1][y] = (cumul[k][y] + NewCode[A[k]][y]) % _modulo[y]
		
 
		_sorted  = sorted(enumerate(A), key=lambda x:x[1])
		pos = [0]*N
		rev = [0]*N #??
		newA = [0]*N
		for n in range(N):
			pos[n] = _sorted[n][0]
			rev[n] = Code[_sorted[n][1]]
			newA[n]  = Code[A[n]]
 
		_sorted = None
			
		_mul = N* (int(math.log(N,2))+3)
		magicTree = [0]*_mul
		magicTree2 = [0]*_mul
		build_tree(magicTree,pos,magicTree2,newA,0,0,N-1)
 
		#print A
		#print newA
		#print magicTree
		print magicTree2
		
		#return
		
		#Q = 1000
		for _ in range(Q):
			a, b, c, d = map(int , sys.stdin.readline().strip().split())
			
			a -=1 
			b -=1 
			c -=1 
			d -=1 
			
			# a = 0 
			# b = N/2-1 
			# c = N/2
			# d = N-1
			
			# if (b - a + 1) <= 80:
				# print (test(A,a,b,c,d))
				# continue
			
			tmpL = cumul[b+1] - cumul[a]
			tmpR = cumul[d+1] - cumul[c]
			
			
			#print initL, initR
			res = "YES"
			
			
			if tmpL  == tmpR:
				print res
				#print(test(A,a,b,c,d))
				continue
			
			initL = [0]*filters
			initR = [0]*filters
			for y in range(filters):
				initL[y] = tmpL % _modulo[y]
				initR[y] = tmpR % _modulo[y]

			
			na = a
			nb = b
			nc = c
			nd = d
			
			altL = [0] * filters
			altR = [0] * filters
			sumL = [0] * filters
			sumR = [0] * filters
			
			while na!=nb:
				mL = na+(nb-na)/2
				mR = nc+(nd-nc)/2
				
				subs( sumL , query( magicTree, magicTree2, rev, N, a, b, mL-a+1) , query( magicTree, magicTree2, rev, N, a, b, na-a) )
				subs( sumR , query( magicTree, magicTree2, rev, N, c, d, mR-c+1) , query( magicTree, magicTree2, rev, N, c, d, nc-c) )
			
				for y in range(filters):
					altL[y] = (initL[y] - sumL[y]) % _modulo[y]
					altR[y] = (initR[y] - sumR[y]) % _modulo[y]
				
				print initL, initR, sumL, sumR, altL, altR
				
				boolSum = check(sumL , sumR)
				boolAlt = check(altL , altR)
				if  (not boolSum) and (not boolAlt):
					res = "NO"
					break
				
				if (not boolSum):
					initL = list(sumL)
					initR = list(sumR)
					nb = mL
					nd = mR
				else:
					initL = list(altL)
					initR = list(altR)
					na = mL+1
					nc = mR+1
			
			print res
			#print(test(A,a,b,c,d))
			
			# if res != test(A,a,b,c,d):
				# print A
				# print a,b,c,d
				# print res
				# return
 
		
 
		
def test(A,L,R,X,Y):
	B = A[L:R+1]
	B = sorted(B)
	C = A[X:Y+1]
	C = sorted(C)
	
	numdiff = 0
	for k in range(len(C)):
		if B[k] != C[k]:
			numdiff += 1
			
	if numdiff <= 1:
		return "YES"
	else:
		return "NO"
	
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
	
	s= time.time()
	
	# N = 80
	# T = (10**5)  *  ( int( N*math.log(N) + N ) )
	# ss= 2
	# for z in xrange(T):
		# ss = (2*ss*z) % _modulo
	
	main()
	#generate()
	#test()
	
 
	print time.time()-s   