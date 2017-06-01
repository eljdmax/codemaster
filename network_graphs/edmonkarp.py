import time
import math
 
#from decimal import *
#getcontext().prec = 50
#import bisect

import random
import bisect
import collections

from Queue import PriorityQueue
 
#pi = pi / Decimal(10**100)

#counter = 0

class Node:
	def __init__(self):
		self.outbound = set([])
	
	def addEdge(self, endNode): # min 0, data <- max cap, #data (min capacity, max capacity, cost) ??
		self.outbound.add(endNode)
		

class Graph:

	def __init__(self,N):
		self.N = N
		self.nodes = [Node() for _ in range(N)]
		self.edges = {}
		self.edgesCounter = 0
		
		
	def addEdge(self,a,b,data):
		self.edges[self.edgesCounter] = [a,b,self.edgesCounter+1,data,0] # start, end, reverse_edge, capacity, flow
		self.edges[self.edgesCounter+1] = [b,a,self.edgesCounter,0,0]
		
		self.nodes[a].addEdge(self.edgesCounter)
		self.nodes[b].addEdge(self.edgesCounter+1)
		
		self.edgesCounter += 2
		
			
	def BFS(self,s,t, path):
		visited = [False] * (self.N)
		queue = collections.deque()
		
		queue.append(s)
		visited[s] = True
		
		while queue:
			u = queue.pop() #popleft()
			for e in self.nodes[u].outbound:
				ind = self.edges[e][1] 
				if visited[ind] == False and self.edges[e][3] > self.edges[e][4]:
					queue.append(ind)
					visited[ind] = True
					path[ind] = (u,e)
					if ind == t:
						return True
		
		return False
		
	def EdmonKarp(self, s, t):
		max_flow = 0
		path = {}
		
		while self.BFS(s, t, path) :
			path_flow = float("Inf")
			cur = t
			while cur !=  s:
				par, e = path[cur]
				path_flow = min(path_flow, self.edges[e][3] - self.edges[e][4])
				cur = par
				
			max_flow += path_flow
			
			cur = t
			while cur !=  s:
				par,e = path[cur]
				self.edges[e][4] += path_flow
				self.edges[self.edges[e][2]][4] -= path_flow
				cur = par
			#path = {}
		
		return max_flow
	
	
	
def main():
	
	import sys
	#from operator import itemgetter
	#from sets import Set
	
	# N = 4
	# graph = Graph(N)
	
	# graph.addEdge(0,1,1000)
	# graph.addEdge(0,2,1000)
	# graph.addEdge(2,1,1)
	# graph.addEdge(1,3,1000)
	# graph.addEdge(2,3,1000)
	
	# print graph.FordFulk(0,3)
	
	N = 7
	graph = Graph(N)
	
	graph.addEdge(0,1,3)
	graph.addEdge(0,3,3)
	graph.addEdge(1,2,4)
	graph.addEdge(2,0,3)
	graph.addEdge(2,3,1)
	graph.addEdge(2,4,2)
	graph.addEdge(3,4,2)
	graph.addEdge(3,5,6)
	graph.addEdge(4,1,1)
	graph.addEdge(4,6,1)
	graph.addEdge(5,6,9)
	
	print graph.EdmonKarp(0,6)
	
	for i in range(N):
		for k in graph.nodes[i].outbound:
			print graph.edges[k]
	
	#T = int(sys.stdin.readline().strip())
	
	#for _ in range(T):
		#pq = PriorityQueue()
		#(N, M) = map(int , sys.stdin.readline().strip().split())
		
		
		#print len(result)
		#for i in range(len(result)):
		#	print result[i][0], result[i][1], result[i][2], result[i][3]
	
		#print counter

def test():
	1

	
def generate():
	1
	
if __name__ == "__main__":
	
	#s= time.time()
	main()
	#generate()
	#test()

	#print time.time()-s