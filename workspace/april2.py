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

##http://codeforces.com/blog/entry/21693

def recurs(order, nodes, edges):

	node_index = 0
	nodes[0] = {}
	
	queue = []
	for k in order[0]:
		node_index += 1
		nodes[node_index] = {}
		nodes[0][node_index]  = k - 1  #  0 -> node_index is edge k-1 
		edges[k-1] = (0, node_index)   # k -1 maps to 0 -> node_index, par, child
		queue.append(k)
	
	
	visited = set([0])
	
	while len(queue) > 0 :
		cur = queue.pop() #dequeue ??
	
		new_par = edges[cur-1][1]
		
		for k in order[cur]:
			if (k in visited):
				continue
			
			node_index += 1
			nodes[node_index] = {}
			nodes[new_par][node_index]  = k - 1  #  new_par -> node_index is edge k-1 
			edges[k-1] = (new_par, node_index)   # k -1 maps to 0 -> node_index, par, child
			queue.append(k)
		
		visited.add(cur)
	
	
def main():
	
	import sys
 
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		N, M = map(int , sys.stdin.readline().strip().split())
		
		edges = [0]*N
		weigth = [0]*N
		
		nodes = {}
		
		order = [0]* (N+1)
		for n in range(N+1):
			order[n] = []
		
		for n in range(N):
			P, W = map(int , sys.stdin.readline().strip().split())
			weigth[n] = W  ## weigth of edge n
			
			order[n+1].append(P)
			order[P].append(n+1)
		
		recurs(order, nodes, edges)
		
		#print nodes
		#print edges
		
		
		
		
		
		for m in range(M):
			data =  map(int , sys.stdin.readline().strip().split())
			state = data[0]
			q = data[1]
			
			if q == 1:
				u = data[2] - 1
				x = data[3]
				
				
			else:
				u = data[2] - 1

		
		
 
		
 
		
def test(A,L,R,X,Y):
	1
	
def generate():
	1
	
	
if __name__ == "__main__":
	
	s= time.time()
	
	main()
	#generate()
	#test()
	
 
	print time.time()-s   