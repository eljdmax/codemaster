#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
from itertools import chain, combinations
 
#import bisect
 
#pi = pi / Decimal(10**100)
 
MASK = (1<<31) - 1
	
class Branch:
	def __init__(self):
		self.inline = None
		self.inline_root = 0
		self.rootNode = None
		self.counter = -1
		self._keys = []
		
	def setRootNode(self, node):
		self.rootNode = node
	
	def getLevel(self, key):
		#search key , insert edge bit
		self.counter += 1
		self._keys.append(key)
		return self.counter
		
	def init(self):
		
		self.inline = [0] *(5* 2 * (self.counter+2) )
		
		top = 5
		
		#set root
		self.inline[1] = self._keys[0]
		
		
		for i in xrange(1,self.counter+1):
			key = self._keys[i]
			
			cur = self.inline_root
			pre = -1
			enter = -1
			
			
			magic = 1<<(len(bin( self.inline[cur + 1] ^ key))-3)
			
			
			while (self.inline[cur+2] != 0) and ( magic <= self.inline[cur+2]):
				pre = cur
				mask = self.inline[cur+2] & key
				
				if (mask == 0):
					cur = self.inline[cur+3]
					enter = 0
				else:
					cur = self.inline[cur+4]
					enter = 1
					
				magic = 1<<(len(bin(self.inline[cur + 1] ^ key))-3)
			
			
			t = ( (MASK - (magic-1) ) & key ) | magic
			new_cur = top
			top += 5
			self.inline[new_cur] = self.inline[cur] # new_cur will reach cur which is the min
			self.inline[new_cur+1] = t
			self.inline[new_cur+2] = magic
			
			if (pre == -1):
				self.inline_root = new_cur
			else:
				self.inline[pre+3+enter] = new_cur
			
			key_node = top
			top += 5
			self.inline[key_node] = i
			self.inline[key_node+1] = key
			
			if (magic & self.inline[cur + 1] ) == 0:
				self.inline[new_cur+3] = cur
				self.inline[new_cur+4] = key_node
			else:
				self.inline[new_cur+3] = key_node
				self.inline[new_cur+4] = cur
 
		
	def getMax(self, key, index):
		
		cur = self.inline_root
 
		while ( self.inline[cur+2] != 0 ):
			mask = 0 if (self.inline[cur+2] & key == 0) else 1
			if ( self.inline[self.inline[cur+4-mask]] <= index):
				cur = self.inline[cur+4-mask]
			else:
				cur = self.inline[cur+3+mask]
 
		return self.inline[cur+1] ^ key
		
		
	def getMin(self, key, index):
	
		cur = self.inline_root
 
		while ( self.inline[cur+2] != 0 ):
			mask = 0 if (self.inline[cur+2] & key == 0) else 1
			if ( self.inline[self.inline[cur+3+mask]] <= index):
				cur = self.inline[cur+3+mask]
			else:
				cur = self.inline[cur+4-mask]
 
		return self.inline[cur+1] ^ key
 
		
class Node:
	def __init__(self, val, key):
		self.val = val
		self.key = key
		self.branch = None
		self.level = 0 
		self.parent = None
		self.numChildren = 0
		self.cumulChildren = 1
		self.children = []
	
	
	def addChild(self, child):
		self.numChildren += 1
		self.children.append(child)
		child.setParent(self)
		
	def increaseCumul(self, increase):
		self.cumulChildren += increase
		
	def setParent(self, parent):
		self.parent = parent
		
	def setBranch(self, branch):
		self.branch = branch
		
	def setLevel(self, level):
		self.level = level
		if (level == 0):
			self.branch.setRootNode(self)
		
	def updateChildren(self):
		if (self.numChildren != 0 ):
			self.children = sorted(self.children , key=lambda student: -1*student.cumulChildren)
			
	def getMax(self, key):
		_max  = self.branch.getMax(key, self.level)
		
		cur = self.branch.rootNode.parent
		while (cur != None):
			_max = max( _max, cur.getMax(key) )
			cur = cur.branch.rootNode.parent
		
		return _max
	
	def getMin(self, key):
		_min = self.branch.getMin(key, self.level)
		
		cur = self.branch.rootNode.parent
		while (cur != None):
			_min = min( _min, cur.getMin(key) )
			cur = cur.branch.rootNode.parent
		
		return _min
	
def firstTraverse(nodes, tour, _top):
	
	for i in xrange(_top-1, -1, -1):
		(par, cur) = tour[i]
		nodes[par].addChild(nodes[cur])
		nodes[par].increaseCumul(nodes[cur].cumulChildren)
	
 
def traverse(cur, cur_branch , branches):
	
 
	level = cur_branch.getLevel(cur.key)
	cur.setBranch(cur_branch)
	cur.setLevel(level)
	
	while cur.numChildren > 0:
		cur.updateChildren()
		if (cur.numChildren > 1):
			for i in xrange(1,cur.numChildren):
				new_branch = Branch()
				branches.append(new_branch)
				traverse(cur.children[i], new_branch, branches )
				
		cur = cur.children[0]
		level = cur_branch.getLevel(cur.key)
		cur.setBranch(cur_branch)
		cur.setLevel(level)
	
def main():
	
	import sys
	#from operator import itemgetter
	#from sets import Set
	
	
	
	(N, Q) = map(int , sys.stdin.readline().strip().split())
	
	(R, K) = map(int , sys.stdin.readline().strip().split())
	
	
	
	nodes = {}
	
	nodes[R] = Node(R,K)
	
	
	_top = 0
	tour = [0]*(N+Q)
	
	_top_q = 0
	queries = [0]*Q
 
	# for i in xrange(N-1):
		# ( u, v, k) = map(int , sys.stdin.readline().strip().split())
		# nodes[u] = Node(u,k)
		# tour[_top] = (v,u) 
		# _top += 1
	
	# for q in xrange(Q):
		# data = map(int , sys.stdin.readline().strip().split())
		
		# if (len(data) == 4):
			# v = data[1] ^ data[0]
			# u = data[2] ^ data[0]
			# k = data[3] ^ data[0]
			
			# nodes[u] = Node(u,k)
			
			# tour[_top] = (v,u) 
			# _top += 1
 
		# else:
			# #query
			# queries[_top_q] = (data[1],data[2])
			# _top_q += 1
	
	
	lines = sys.stdin.readlines()
	for line in lines:
		if (_top < N-1):
			( u, v, k) = map(int , line.strip().split())
			nodes[u] = Node(u,k)
			tour[_top] = (v,u) 
			_top += 1
		else :
			data = map(int , line.strip().split())
			
			if (len(data) == 4):
				v = data[1] ^ data[0]
				u = data[2] ^ data[0]
				k = data[3] ^ data[0]
				
				nodes[u] = Node(u,k)
				
				tour[_top] = (v,u) 
				_top += 1
 
			else:
				#query
				queries[_top_q] = (data[1],data[2])
				_top_q += 1
	
	firstTraverse(nodes, tour, _top)
	#tour = None
	
	cur_branch = Branch()
	branches = [cur_branch ] 
	traverse(nodes[R], cur_branch , branches)
	
	
	#for k in nodes.keys():
		#print k, nodes[k].numChildren, nodes[k].cumulChildren
		#for l in nodes[k].children:
		#	print l.val
		#print "----"
		#print k, nodes[k].branch, nodes[k].level
	
	
	for b in branches:
		#print b, b.counter
		b.init()
		
		#print b.inline, b.inline_root
 
		
	last_answer  = 0
 
	#print 0
	
	for i in xrange(_top_q):
		(v,k) = queries[i]
		v = v ^ last_answer
		k = k ^ last_answer
		
		_min = nodes[v].getMin(k)
		_max = nodes[v].getMax(k)
		
		print _min, _max
		
		last_answer = _min ^ _max
	
def test():
	N = 250000
	
	# print N, 0 
	# print 1, 1
	# for i in xrange(1,N):
		# print i+1 , i, i+1
	
	root = 0
 
	inline = [0] *(4*30*N)
	inline[0] = 0 #default bit min, MAX
	
	top = 4
	
	for i in xrange(N):
		rep = bin(i)[2:].zfill(MASK)
		
		cur = root
		
		for c in rep:
			if (i > inline[cur]):
				inline[cur] = i
			
			child = cur + 2 + int(c)
			if  inline[child] == 0 :
				inline[child] = top
				inline[top] = i
				top += 4
				
			cur = inline[child]
			
			#if cur.down[digit] != None:
			#	cur.setDown(digit,None)
			#cur = cur.down[digit]
	
if __name__ == "__main__":
	
	#s= time.time()
	main()
	#test()
 
	#print time.time()-s   