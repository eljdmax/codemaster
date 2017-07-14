#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
#from itertools import chain, combinations
import random
import bisect
import copy
 

TOP = 10**9
#pi = pi / Decimal(10**100)

class Node:

	def __init__(self, id):
		self.id = id
		self.level = 0 
		self.parent = None
		self.children = []
		
		self.allMinHash = None
		self.onesMinHash = { "00" : [None, None] , "01": [None, None], "10": [None, None], "11": [None, None] } #up 2 to values , tuple -> (index, val)
		
		#only for 01
		self.secondHash = {}
		self.secondOnesMin = None
		
		self.data = [  TOP,  #000
					   TOP,  #001
					   TOP,  #010
					   TOP,  #011
					   TOP,  #100 #cant do
					   1,  #101
					   1,  #110
					   1  #111
					     ] # 8 values, 000 -> 111
		
	def setParent(self,parent):
		self.level = parent.level + 1
		self.parent = parent
	
	def addChild(self, child):
		self.children.append(child)
	
	def initMinHash(self):
		ll = len(self.children)
		
		self.allMinHash ={ "00" : [(0,0,0)]*ll , "01": [(0,0,0)]*ll, "10": [(0,0,0)]*ll, "11": [(0,0,0)]*ll }
		
	def updateMin(self, key, index, val0, val1):
		self.allMinHash[key][index] = (val0,val1, min(val0,val1))
		
		if (val1 != TOP ) :
			if ( self.onesMinHash[key][0] == None ) or ( val1 < self.onesMinHash[key][0][1] ) or ( ( val1 == self.onesMinHash[key][0][1] ) and (val0 >  self.allMinHash[key][ self.onesMinHash[key][0][0] ][0] ) ):
				#decal
				self.onesMinHash[key][1] = self.onesMinHash[key][0]
				self.onesMinHash[key][0] = (index, val1)
			elif  ( self.onesMinHash[key][1] == None ) or ( val1 < self.onesMinHash[key][1][1] ) or ( ( val1 == self.onesMinHash[key][1][1] ) and (val0 >  self.allMinHash[key][ self.onesMinHash[key][1][0] ][0] ) ):
				self.onesMinHash[key][1] = (index, val1)

	def updateParMin(self, id, val0, val1):
		if self.parent ==None:
			return
		
		self.parent.secondHash[id] = (val0,val1, min(val0,val1))
		
		if (val1 != TOP ):
			if (self.parent.secondOnesMin == None) or (val1 < self.parent.secondOnesMin[1]) or ( (val1 == self.parent.secondOnesMin[1])  and (val0 > self.parent.secondHash[ self.parent.secondOnesMin[0] ][0] ) ):
				self.parent.secondOnesMin = (id, val1)
			
		
	
	def process(self, index):
		
			
		if ( len(self.children) > 0 ):
			#update the data
			
			# key "00", need at least two ones
			key = "00"
			val = TOP
			if ( self.onesMinHash[key][0] != None ) and (self.onesMinHash[key][1] != None):
				excl0 = self.onesMinHash[key][0][0]
				excl1 = self.onesMinHash[key][1][0]
				
				val = self.onesMinHash[key][0][1] + self.onesMinHash[key][1][1]
				
				
				for i in xrange( len(self.children) ):
					if (i == excl0) or (i == excl1) :
						continue
					
					if ( self.allMinHash[key][i][2] == TOP ):
						val = TOP
						break
					val += self.allMinHash[key][i][2]
					
			self.data[0] = val  #000
			self.data[1] = val  #001
			
			# key "01", need at least one ones
			key = "01"
			val = TOP
			
			if ( self.onesMinHash[key][0] != None ) :
				excl0 = self.onesMinHash[key][0][0]
				val = self.onesMinHash[key][0][1]
				
				for i in xrange( len(self.children) ):
					if (i == excl0):
						continue
					if ( self.allMinHash[key][i][2] == TOP ):
						val = TOP
						break
					val += self.allMinHash[key][i][2]
			
			self.data[2] = val #010
			self.data[3] = val #011
			
			# key "10", need at least one ones  or zero ??
			key = "10"
			val = TOP
			if ( self.onesMinHash[key][0] != None ) :
				excl0 = self.onesMinHash[key][0][0]
				val = self.onesMinHash[key][0][1]
				
				for i in xrange( len(self.children) ):
					if (i == excl0):
						continue
					if ( self.allMinHash[key][i][2] == TOP ):
						val = TOP
						break
					val += self.allMinHash[key][i][2]
			
			self.data[4] = 1+val #100
			
			
			## at least one zeros in the second generation ???
			val = TOP
			if ( self.secondOnesMin != None ) :
				excl0 = self.secondOnesMin[0]
				val = self.secondOnesMin[1]
				
				for k in self.secondHash.keys():
					if k == excl0:
						continue
					if ( self.secondHash[k][2] == TOP ):
						val = TOP
						break
					val += self.secondHash[k][2]

			self.data[4] = min (self.data[4], 1 +val )
			
			
			#no constraints
			val = 0
			for i in xrange( len(self.children) ):
				if ( self.allMinHash[key][i][2] == TOP ):
					val = TOP
					break
				val += self.allMinHash[key][i][2]
			
			
			self.data[5] = 1+val #101
			

			# key "11", need at least zero ones
			key = "11"
			val = 0
			for i in xrange( len(self.children) ):
				if ( self.allMinHash[key][i][2] == TOP ):
					val = TOP
					break
				val += self.allMinHash[key][i][2]
			
			self.data[6] = 1+val #110
			self.data[7] = 1+val #111
			
		else:
			#push parent
			self.updateParMin(self.id, self.data[1], self.data[5] )
	
		if (self.parent != None):
			#push data to parent
			self.parent.updateMin("00", index, self.data[0], self.data[4] ) # 000 / 100
			self.parent.updateMin("01", index, self.data[1], self.data[5] ) # 001 / 101
			self.parent.updateMin("10", index, self.data[2], self.data[6] ) # 010 / 110
			self.parent.updateMin("11", index, self.data[3], self.data[7] ) # 011 / 111
			
			#self.parent.updateParMin(self.id, min(self.data[1], self.data[3] ), min(self.data[5],self.data[7]) ) #"01"
			self.parent.updateParMin(self.id, self.data[1], self.data[5] ) #"01"
	
	def isValid(self,tuple):
		
		numActiveChildren = 0
		numActiveGrandChildren = 0
		for k in self.children:
			if tuple[k.id] == 1:
				numActiveChildren += 1
				numActiveGrandChildren += 1
			for l in k.children:
				if tuple[l.id] == 1:
					numActiveGrandChildren += 1
				
		if tuple[self.id] == 0:
			if self.parent != None and tuple[self.parent.id] == 1:
				return numActiveChildren >=1 
			else:
				return numActiveChildren >= 2
		else:
			if self.parent!=None:
				if tuple[self.parent.id] == 1:
					return True
				else:
					if self.parent.parent != None and tuple[self.parent.parent.id] == 1:
						return True
					else:
						return numActiveGrandChildren >= 1
			else:
				#like if it was 00
				return numActiveGrandChildren >= 1
	
	def remove(self, tuple):
		new_tuple = list(tuple)
		new_tuple[self.id] = 0
		
		if not self.isValid(new_tuple):
			return None
		
		if self.parent != None:
			if not self.parent.isValid(new_tuple):
				return None
			if self.parent.parent != None and not self.parent.parent.isValid(new_tuple):
				return None
	
		
		for k in self.children:
			if not k.isValid(new_tuple):
				return None
			for l in k.children:
				if not l.isValid(new_tuple):
					return None
					
		return new_tuple
	
	def show(self):
		
		print "Node ", self.id
		
		print self.data
		

 
def recurs(vertices, root, nodes):
 
	queue = []
	for k in vertices[1].keys():
		cur = Node(k)
		nodes[k] = cur
		cur.setParent(root)
		root.addChild(cur)
		
		queue.append(cur)
	
	root.initMinHash()
	visited = set([1])
	
	while len(queue) > 0 :
		
		cur = queue.pop() #dequeue ??
	
		if cur.id in visited:
			continue

			
		if len(vertices[cur.id]) == 1 :
			continue
			
		for k in vertices[cur.id].keys():
			if (k in visited):
				#del vertices[cur][k]
				continue
			new_cur = Node(k)
			nodes[k] = new_cur
			new_cur.setParent(cur)
			cur.addChild(new_cur)
			
			queue.append(new_cur)
		
		cur.initMinHash()
		visited.add(cur.id)
 
def dfs(root):
	
	queue = [(root,-1)]
	
	for i in xrange(len(root.children)):
		c = root.children[i]
		queue.append((c , i))
		queue.append((c , i))
	
	visited = set([1])
	
	while len(queue) > 0 :
		
		cur, index = queue.pop() #dequeue ??
	
		if cur.id in visited:
			#finished treating its children, process !!
			cur.process(index)
			continue
		

		for i in xrange(len(cur.children)):
			c = cur.children[i]
			queue.append((c , i))
			queue.append((c , i))
	
		visited.add(cur.id)


def dfs_show(root):
	
	queue = [(root,-1)]
	
	for i in xrange(len(root.children)):
		c = root.children[i]
		queue.append((c , i))
		queue.append((c , i))
	
	visited = set([1])
	
	while len(queue) > 0 :
		
		cur, index = queue.pop() #dequeue ??
	
		if cur.id in visited:
			#finished treating its children, process !!
			cur.show()
			continue
		

		for i in xrange(len(cur.children)):
			c = cur.children[i]
			queue.append((c , i))
			queue.append((c , i))
	
		visited.add(cur.id)
		

		
def main():
	
	import sys
	#from collections import deque
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		N = int(sys.stdin.readline().strip())
		
		vertices = [0]*(N+1)
		adj = [0]*(N)
		for n in xrange(1,N+1):
			vertices[n] = {}
			adj[n-1] = [0]*N
		
		for n in xrange(N-1):
			U, V = map( int, sys.stdin.readline().strip().split() )

			adj[U-1][V-1] = 1
			adj[V-1][U-1] = 1
			
			vertices[U][V] = 1
			vertices[V][U] = 1
		
		#for  n in range(N):
		#	print ",".join([ str(c) for c in adj[n]])
		
		
		nodes = [0]*(N+1)
		root = Node(1)
		nodes[1] = root
		extra = recurs(vertices, root, nodes)
		
		dfs(root)
		#print root.data
		
		
		
		sol = min ( root.data[0]  , root.data[4] )
		if sol == TOP:
			sol = -1
		print sol
		
		#dfs_show(root)
		
		print "----"
		
		brute(nodes,N)
		
		
		

def brute(nodes,N):
	
	tuple = [1]*(N+1)
	sols = []
	_min = TOP
	
	#tuple = [1, 1, 1, 0, 1, 1]
	queue = [ tuple ]
	
	while len(queue) > 0:
		cur = queue.pop()
	
		can_remove = False
		for i in range(1,N+1):
			if cur[i] == 0:
				continue
			val = nodes[i].remove(cur)
			if val != None:
				queue.append(val)
				can_remove = True
		
		if not can_remove:
			val = sum(cur) -1
			if val < _min:
				_min = val
				sols = [cur]
				print _min
				print sols
			#elif val == _min:
			#	sols.append(cur)
	

	#print _min
	#print sols
		
		
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
 