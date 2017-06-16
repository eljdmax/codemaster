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

	
def main():
	
	import sys
	from collections import deque
	
	
	N, M, Q = map( int, sys.stdin.readline().strip().split()) 
	
	nodes = [0]*(N+1)
	for n in xrange(1,N+1):
		nodes[n] = []
	
	for m in xrange(M):
		u, v = map( int, sys.stdin.readline().strip().split()) 
		
		nodes[u].append(v)
		nodes[v].append(u)
			
	
	
	
	
	for q in xrange(Q):
		u, v, w = map( int, sys.stdin.readline().strip().split()) 
	
	
	
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