#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
#from itertools import chain, combinations
import random
import bisect
 
from collections import deque
 
 
#pi = pi / Decimal(10**100)
 

def getTuple(a,b):
	if a < b :
		return (a,b)
	else:
		return (b,a)
 
	
	
def main():
	
	import sys
	#from collections import deque
	
	N, Q = map( int, sys.stdin.readline().strip().split() ) #int(sys.stdin.readline().strip())
	
	A = map( int, sys.stdin.readline().strip().split() )
	
	
	test(A,N)
	
	A.append(-1)
	
	data = {}
	index = -1
	seen = []  # num, consecutive count, number of elem < , number of elem >
	
	
	track = {A[0]:0}
	zeros = {}
	
	pre = A[0]
	l = 0
	
	for i in range(N+1):
		if (A[i] == pre):
			l += 1
			continue
	
		if not pre in track:
			track[pre] = 0
			
		
		val = i - l - track[pre]
		seen.append( (pre, l, val ) )
		
		if not pre in zeros :
			zeros[pre] = (val*(val+1))/2
		
		track[pre] = i
		l = 1
		pre = A[i]
	
	
	M = len(seen)
	track = { seen[M-1][0] : 0  }
	
	seen[M-1] = seen[M-1] + (0,)
	
	cumul = seen[M-1][1]
	track = {}
	track[ seen[M-1][0] ]  = cumul
	
	#print track
	
	for i in range(M-2, -1, -1):
		
		if not seen[i][0] in track:
			track[  seen[i][0] ] = 0
		
		val = cumul - track[seen[i][0]]
		seen[i] = seen[i] + (val,)
		
		zeros[ seen[i][0] ] += (val*(val+1))/2 

		cumul += seen[i][1]
		track[seen[i][0]] = cumul

		
		
	zeros[-1] = (N*(N+1))/2 
	
	
	#print seen
	#print zeros
	
	carry = { seen[0][0] : 0}
	
	carry[seen[0][0]] +=  ( seen[0][2]  * (seen[0][2] +1) ) /2
	
	for i in range(1, M):
		pre = seen[i]
		
		if not pre[0] in carry:
			carry[pre[0] ] = 0
			
		carry[pre[0]] +=  ( pre[2]  * (pre[2] +1) ) /2
		
		cumul = { pre[0] : 0 }
		total = pre[1]
		reset = 0
		first = {}
		for j in range(i-1,-1,-1):
			cur = seen[j]
			
			if cur[0] == pre[0] :
				cumul[pre[0]] += cur[1]
				total += cur[1]
				reset = 0
				continue
			
			
			
			_min = 0
			tuple = getTuple(pre[0], cur[0])
			
			if not tuple in data :
				#first time, zero left
				_min += carry[cur[0]]
				#if i ==3 and j ==2:
				#	print _min
				
				_min += ( reset * ( reset + 1) ) / 2
				#if i ==3 and j ==2:
				#	print _min
				
				data[tuple] = 0
			
			if not cur[0] in cumul :
				cumul[ cur[0] ] = 0
				first[ cur[0] ] = min ( pre[3] , cur[3] - total )
				
				_min += ( first[cur[0]] * (first[cur[0]] + 1 ) ) / 2
			
			#data[tuple] += _min 
			
			
			total += cur[1]
			reset += cur[1]
			
			# can we make cur[0] and pre ?
			delta = cumul[pre[0]] - cumul[ cur[0] ] 
			tmp_l = pre[1]
			tmp_left = cur[1]
			
			cumul[ cur[0] ]  += cur[1]
			
			if delta > 0:
				#we need more cur[0]
				if tmp_left > delta :
					tmp_left -= delta
				else:
					continue
			elif delta < 0:
				#we need more pre
				if tmp_l > -delta:
					tmp_l += delta
				else :
					continue
			
			
			_min = 0
			if tuple == (1,3):
				print first[cur[0]]
				print min(cur[2] , pre[2] - reset)
			
			if tmp_l < tmp_left:
				_min += tmp_l
				#complete right of pre which is not pre or cur
				_min += first[cur[0]]
				
			elif tmp_l > tmp_left:
				_min += tmp_left
				#complete left of cur[0] which is not pre or cur
				_min += min(cur[2] , pre[2] - reset)
			else:
				_min += tmp_l - 1
				# and
				_min += (first[cur[0]] + 1) * ( 1 + min(cur[2] , pre[2] - reset) )
				
			
			data[tuple] += _min 
	
	

	print data
	
	for _ in xrange(Q):
		x,y = map(int, sys.stdin.readline().strip().split() )
		
	
def test(A,N):
	
	sol = {}
	
	_keys = list(set(A))
	
	for i in range(N):
		for j in range(i+1):
			_count = {}
			for k in _keys:
				_count[k] = 0
			for c in A[j:i+1]:
				_count[c] += 1
			
			
			
			for n in range(1,len(_keys)):
				for m in range(n):
					tuple = getTuple(_keys[n], _keys[m])
					if not tuple in sol:
						sol[tuple] = 0
					if _count[_keys[n] ] == _count[_keys[m]]  and _count[_keys[n] ] != 0:
						sol[tuple] += 1
	
	print sol
			 
	
	
	
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