#!/usr/bin/python
 
import math
from fractions import gcd
from time import time,clock
from operator import mul
import random
import itertools
#import Queue as queue
#from decimal import *
#import functools
 
#getcontext().prec = 20
 
#from fractions import Fraction
 
#_modulo = 10**9 + 7
 
MAX = 10**15
 
import heapq
 
class PriorityQueue(object):
	"""Priority queue based on heap, capable of inserting a new node with
	desired priority, updating the priority of an existing node and deleting
	an abitrary node while keeping invariant"""
 
	def __init__(self, heap=[]):
		"""if 'heap' is not empty, make sure it's heapified"""
 
		heapq.heapify(heap)
		self.heap = heap
		self.entry_finder = dict({i[-1]: i for i in heap})
		self.REMOVED = '<remove_marker>'
		
	def check(self, node):
		return (self.entry_finder[node])[0]
 
	def insert(self, node, priority=0):
		"""'entry_finder' bookkeeps all valid entries, which are bonded in
		'heap'. Changing an entry in either leads to changes in both."""
 
		if node in self.entry_finder:
			self.delete(node)
		entry = [priority, node]
		self.entry_finder[node] = entry
		heapq.heappush(self.heap, entry)
 
	def delete(self, node):
		"""Instead of breaking invariant by direct removal of an entry, mark
		the entry as "REMOVED" in 'heap' and remove it from 'entry_finder'.
		Logic in 'pop()' properly takes care of the deleted nodes."""
 
		entry = self.entry_finder.pop(node)
		entry[-1] = self.REMOVED
		return entry[0]
 
	def pop(self):
		"""Any popped node marked by "REMOVED" does not return, the deleted
		nodes might be popped or still in heap, either case is fine."""
 
		while self.heap:
			priority, node = heapq.heappop(self.heap)
			if node is not self.REMOVED:
				del self.entry_finder[node]
				return priority, node
		raise KeyError('pop from an empty priority queue')
 
def dijkstra2(edges, init):
 
	pq = PriorityQueue(init)
	
	"""Returns the shortest paths from the source to all other nodes.
	'edges' are in form of {head: [(tail, edge_dist), ...]}, contain all
	edges of the graph, both directions if undirected."""
 
	size = len(pq.heap)
	processed = []
	uncharted = set([i[1] for i in pq.heap])
	shortest_path = {}
	#shortest_path = 0
	while size > len(processed):
		min_dist, new_node = pq.pop()
		processed.append(new_node)
		#print processed
		uncharted.remove(new_node)
		shortest_path[new_node] = min_dist
		for head, edge_dist in edges[new_node]:
			if head in uncharted:
				#old_dist = pq.delete(head)
				#new_dist = min(old_dist, min_dist + edge_dist)
				#pq.insert(head, new_dist)
				old_dist = pq.check(head)
				new_dist = min_dist + edge_dist
				if new_dist<old_dist:
					pq.delete(head)
					pq.insert(head, new_dist)
		
		
		 
		
	return shortest_path
		
 
def test():
	edges = { 1:[ (2,4) , (3,5)]  , 2: [ (1,4)], 3:[(1,5)] }
	
	init  =  [  [-1,1] , [0,2], [-1,3] ]
	
		
	print dijkstra2(edges,init)
	
def getMinVertex(K,edges,init):
 
	dist = dijkstra2(edges,init)
	
	_min = MAX
	_min_i = -1 #????
	for j in dist.keys():
		if ( j <= K) and ( dist[j] < _min ):
			_min = dist[j]
			_min_i = j
			
	return _min_i
	
def main():
	import sys
	
	
	T = int(raw_input().strip())
	
	for _ in range(T):
		#S =  raw_input().strip()
		parts = raw_input().strip().split()
		N = int(parts[0])
		K = int(parts[1])
		X = long(parts[2])
		M = int(parts[3])
		S = int(parts[4])
		
		# if (K > 500) :
			# for m in xrange(M):
				# raw_input().strip().split()
			
			# print "-1 " * N
			# continue
		
		adj = {}
		cost = {}
		dist = {}
		
		#edges = { 1:[ (2,4) , (3,5)]  , 2: [ (1,4)], 3:[(1,5)] }
		edges = {}
		for n in range(1,N+1):
			edges[n] = []
		
		init  =  [  [-1,1] , [0,2], [-1,3] ]
		
		_set = set([])
		
		for m in range(M):
			#(a,b,c) = map(int,raw_input().strip().split())
			parts = raw_input().strip().split()
			a = int(parts[0])
			b = int(parts[1])
			c = long(parts[2])
				
			edges[a].append( (b,c) )
			edges[b].append( (a,c) )
			
			_set.add(a)
			_set.add(b)
		
		
		if (S <= K) :
			init = [ [0,S] ]
			for a in range(1, S):
				edges[a].append( (S,X) )
				edges[S].append( (a,X) )
				
				init.append([MAX,a])
			
			for a in range(S+1, K+1):
				edges[a].append( (S,X) )
				edges[S].append( (a,X) )
				
				init.append([MAX,a])
				
			for a in range(K+1,N+1):
				init.append([MAX,a])
			
			
			
		else:  # S > K
			init = [ [0,S] ]
			_set.remove(S)
			for a in _set:
				init.append([MAX,a])
			
			mid = getMinVertex(K,edges,init)
 
			init = [ [0,S], [MAX,mid] ]
			for a in range(1, mid):
				edges[a].append( (mid,X) )
				edges[mid].append( (a,X) )
				
				init.append( [MAX,a] )
				
			for a in range(mid+1, K+1):
				edges[a].append( (mid,X) )
				edges[mid].append( (a,X) )
				
				init.append( [MAX,a] )
				
			for a in range(K+1, S):
				init.append( [MAX,a] )
			
			for a in range(S+1, N+1):
				init.append( [MAX,a] )
		
		
		dist = dijkstra2(edges, init)
 
		dist[S] = 0
 
		
		res = [""]*N
		
		# print dist
		
		for i in xrange(1,N+1):
			res[i-1] = str(dist[i])
	
		print " ".join(res)
		
 
if __name__ == "__main__":
	
	#the_start_time = time()
	
	#test()
	
	main()
	
	#print time() - the_start_time   