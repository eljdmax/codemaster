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
		self.values = [ {} for _ in range(N)]
		
		
	def addEdge(self,a,b,data):
		self.nodes[a].addEdge(b)
		self.nodes[b].addEdge(a)
		self.values[a][b] = data
		self.values[b][a] = 0
			
	def BFS(self,s,t, path):
		visited = [False] * (self.N)
		queue = collections.deque()
		
		queue.append(s)
		visited[s] = True
		
		while queue:
			u = queue.popleft()
			for ind in self.nodes[u].outbound:
				if visited[ind] == False and self.values[u][ind] > 0:
					queue.append(ind)
					visited[ind] = True
					path[ind] = u
					if ind == t:
						return True
		
		return False
		
	def FordFulk(self, s, t):
		max_flow = 0
		path = {}
		
		while self.BFS(s, t, path) :
			path_flow = float("Inf")
			cur = t
			while cur !=  s:
				path_flow = min(path_flow, self.values[path[cur]][cur])
				cur = path[cur]
				
			max_flow += path_flow
			
			cur = t
			while cur !=  s:
				par = path[cur]
				self.values[par][cur] -= path_flow
				self.values[cur][par] += path_flow
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
	
	print graph.FordFulk(0,6)
	
	for i in range(N):
		for k in graph.nodes[i].outbound:
			print i,k,graph.values[i][k], graph.values[k][i]
	
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