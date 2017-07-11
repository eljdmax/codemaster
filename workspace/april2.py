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
 
 
def build_tree_max( tree1, tree2, magicA, cur , l , r , NN):
	if( l==r ):
		tree1[ NN*cur + l] = magicA[ l ] 
		tree2[ NN*cur + l] = magicA[ l ] 
		return
	
	mid = l+(r-l)/2
	build_tree_max(tree1, tree2, magicA, cur+1 , l , mid , NN) #Build left tree 
	build_tree_max(tree1, tree2, magicA, cur+1 , mid+1 , r , NN) #Build right tree
	
	
	start = NN*cur + l 
	
	ptL = NN*(cur+1) + l
	endPtL = NN*(cur+1) + mid + 1
	
	ptR = NN*(cur+1) + mid + 1
	endPtR = NN*(cur+1) + r + 1
	
	while ptL < endPtL and ptR < endPtR:
		if tree1[ptL] <= tree1[ptR]:
			tree1[start] = tree1[ptL]
			ptL += 1
		else:
			tree1[start] = tree1[ptR]
			ptR += 1
		
		start += 1
	
	for k in xrange(ptL, endPtL):
		tree1[start] = tree1[k]
		start += 1
		
	for k in xrange(ptR, endPtR):
		tree1[start] = tree1[k]
		start += 1
	
	start = NN*cur + l 
	end = NN*cur + r + 1 
	tree2[start]  = tree1[start]
	for k in xrange(start+1,end):
		tree2[k] = tree2[k-1] ^ tree1[k]
	
 
 
def query_max(tree1, tree2, cur, l, r, x, y, NN, K ) :
 
	if ( r<x  or l>y ) : 
		return 0
	
	if (l ==r):
		if ( tree1[NN*cur + l ] <= K):
			return tree2[NN*cur + l ]
		else:
			return 0
		return
		
	if( x<=l and r<=y ) : 
		top = bisect.bisect_right(tree1, K, NN*cur+l , NN*cur +r + 1)
		if top == NN*cur+l:
			return 0
		return tree2[top-1]
 
		
	mid=l+(r-l)/2
		
	return query_max(tree1, tree2, cur+1, l, mid, x, y, NN, K ) ^ query_max(tree1, tree2, cur+1, mid+1, r, x, y, NN, K )
 
 
	
 
def next_recurs(vertices, ray, parent, branches, magic):
	
	queue = []
	
	queue.append((1,-1, 0,1)) # cur, position in the branch , level, node at the root of the branch
	parent[1] = (1,-1, 0,1)  # parent, position in the branch , level,  node at the root of the branch
	branches[1] = []
	
	#visited = set([])
	
	while len(queue) > 0 :
		cur, pos, level, cur_branch = queue.pop() #dequeue ??
		
		#if (cur in visited): 
		#	continue
		
 
		size = len(vertices[cur].keys())
		if size > 0:
			_sorted = sorted( vertices[cur].keys(),  key=lambda x: ray[x])
			
			if (size > 1):
				for k in xrange(size-1):
					queue.append((_sorted[k], 0 , level+1,_sorted[k]))
					parent[_sorted[k]] = (cur, 0, level+1,_sorted[k])
					branches[_sorted[k]] = [ magic[(cur, _sorted[k])] ]
				
			queue.append((_sorted[size-1], pos +1 , level+1, cur_branch))
			parent[_sorted[size-1]] = (cur, pos+1, level+1,cur_branch)
			branches[cur_branch].append(magic[(cur, _sorted[size-1])])
		
		#visited.add(cur)
 
def recurs(vertices, ray):
 
	queue = deque([])
	for k in vertices[1].keys():
		queue.append(1)
		queue.append(k)
	
	
	visited = set([1])
	
	ray.append(1)
	
	while len(queue) > 0 :
		
		cur = queue.pop() #dequeue ??
		ray.append(cur)
		if cur in visited:
			#ray.append(parents[cur])
			continue
		
		for k in vertices[cur].keys():
			if (k in visited):
				#del vertices[cur][k]
				continue
			queue.append(cur)
			queue.append(k)
		
		
		visited.add(cur)
		
	
 
	
	
def main():
	
	import sys
	#from collections import deque
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		N = int(sys.stdin.readline().strip())
		
		vertices = [0]*(N+1)
		magic = {}
		
		for n in xrange(1,N+1):
			vertices[n] = {}
		
		for n in xrange(N-1):
			U, V, C =  map( int, sys.stdin.readline().strip().split() )
 
			magic[(U,V)] = C
			magic[(V,U)] = C
			vertices[U][V] = 1
			vertices[V][U] = 1
		
		#print vertices
		
		ray = deque([])
		recurs(vertices, ray)
		ray = list(ray)
		
		
		vertices = None
		pos = 0
		magicA = deque([])
		first = {}
		
		for k in xrange(1,len(ray)):
			if (not ray[k-1] in first):
				first[ray[k-1]] = k-1
				
			if ray[k-1] == ray[k]:
				continue
			
			magicA.append(int( magic[(ray[k-1], ray[k])] ) )
			magic[(ray[k-1], ray[k])] = pos
			
			pos += 1
		
		magicA = list(magicA)
		
		
		
		#print magicA
		#print magic
		#print first
		
		#magicA = [3 , 1, 4,2,5, 1,123,123,34,554,433,1435,14,4345,24121,4541,11,11,545,55,1,4,5]
		
		NN = len(magicA)
		exp = int( math.log(NN,2)) ; 
		size = exp + 2
		tree1 = [0]* (NN * size)
		tree2 = [0]* (NN * size)
			
		build_tree_max( tree1, tree2, magicA, 0 , 0 , NN-1 , NN)
		
		#print magicA
		# print tree1
		# print tree2
		
		#for k in range(1,size):
		#	print tree1[(k-1)*NN : k*NN]
		
		#print "---"
		
		#for k in range(1,size):
		#	print tree2[(k-1)*NN : k*NN]
		
		M = int(sys.stdin.readline().strip())
		for m in xrange(M):
			U, V, K = map( int, sys.stdin.readline().strip().split() )
			
			sol = 0
			
			if U == V:
				print 0
				continue
			
			fU = first[U]
			fV = first[V]
			
			if fU < fV:
				x = magic[ (ray[fU], ray[fU+1]) ]
				y = magic[ (ray[fV-1], ray[fV]) ]
				#print x, y
				sol = query_max(tree1, tree2 , 0, 0, NN - 1, x, y, NN,  K )
			else:
				x = magic[ (ray[fV], ray[fV+1]) ]
				y = magic[ (ray[fU-1], ray[fU]) ]
				#print x, y
				sol = query_max(tree1, tree2 , 0, 0, NN - 1, x, y, NN, K )
			
			print sol
		
		
	
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