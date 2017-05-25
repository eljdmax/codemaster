#!/usr/bin/python
 
import math
import Queue as queue
from decimal import *
getcontext().prec = 20

## modulo query ranged:
##     m1: maintain sorted list of ai modulo x, search according to range
##     m2: loop with large gap check existence, search according to range
##     m3: 
## search : upper_bound(R) - lower_bound(L)

def lower_bound(nums, target):
	#bisect.bisect_left
	l, r = 0, len(nums) - 1
	while l <= r:
		mid = l + (r - l) / 2
		if nums[mid] >= target:
			r = mid - 1
		else:
			l = mid + 1
	return l
	
	
def upper_bound(nums, target):
	#bisect.bisect_right
	l, r = 0, len(nums) - 1
	while l <= r:
		mid = l + (r - l) / 2
		if nums[mid] > target:
			r = mid - 1
		else:
			l = mid + 1
	return l
	

## Fast Fourier Transform (multiplication in nlogn)

def pi():
	#Compute Pi to the current precision.

	getcontext().prec += 2  # extra digits for intermediate steps
	three = Decimal(3)	  # substitute "three=3.0" for regular floats
	lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
	while s != lasts:
		lasts = s
		n, na = n+na, na+8
		d, da = d+da, da+32
		t = (t * n) / d
		s += t
	getcontext().prec -= 2
	return +s			   # unary plus applies the new precision

def compRound(z, pre, scale = 1):
	
	_cur =  int(round(z.real,pre))
	_offset = 0 if (_cur % scale == 0) else 1
	return _cur/scale + _offset
	
def FastFourierTransform(A, _cache):
	n = len(A)
	if n == 1:
		return A
	
	if (A in _cache):
		return _cache[A]
	
	nl  = n >> 1
	
	U = ()
	V = ()
	
	for i in xrange(nl):
		ci = i << 1
		U = U + (A[ci],)
		V = V + (A[ci+1],)
	
	#print U, V
	FU = FastFourierTransform(U, _cache)
	FV = FastFourierTransform(V, _cache)
		
	#nroot = complex( cos(_fpi/Decimal(n)) , sin(_fpi/Decimal(n)) )
	nroot = complex( math.cos(_fpi/Decimal(n)) , math.sin(_fpi/Decimal(n)) )
	w = complex(1,0)
	
	FA = ()
	NFA = ()
	for i in xrange(nl):
		FA =  FA + (FU[i] + w*FV[i],)
		NFA  = NFA + ( FU[i] - w*FV[i],)
		w = w*nroot
		
	_cache[A] = FA+NFA
	return _cache[A]
	
	
def InverseFastFourierTransform(A, _cache):
	n = len(A)
	if n == 1:
		return A
	
	if A in _cache :
		return _cache[A]
	
	nl  = n >> 1
	
	U = ()
	V = ()
	
	for i in xrange(nl):
		ci = i << 1
		U = U + (A[ci],)
		V = V + (A[ci+1],)
	
	#print U, V
	FU = InverseFastFourierTransform(U, _cache)
	
	FV = InverseFastFourierTransform(V, _cache)
		
	#nroot = complex( cos(_fpi/Decimal(n)) , Decimal(-1)*sin(_fpi/Decimal(n)) )
	nroot = complex( math.cos(_fpi/Decimal(n)) ,  -1*math.sin(_fpi/Decimal(n)) )
	w = complex(1,0)
	
	FA = ()
	NFA = ()
	for i in xrange(nl):
		FA =  FA + (FU[i] + w*FV[i],)
		NFA  = NFA + ( FU[i] - w*FV[i],)

		w = w*nroot
		
	
	_cache[A] = FA+NFA
	return _cache[A] 


def FastFourierMultiply(A,B):
	
	la = len(A)
	lb = len(B)
	
	lt = (la + lb)
	#print lt
	
	l = len(bin(lt-1))-2
	el = 2**l
	print el
	
	A.extend([0]*( el - la))
	B.extend([0]*( el - lb))
	
	_cache = {}
	FA = FastFourierTransform(tuple(A),_cache)
	FB = FastFourierTransform(tuple(B),_cache)
	
	
	R = [0]*el
	for i in xrange(el):
		R[i] = FA[i]*FB[i]
	
	FR  = InverseFastFourierTransform(tuple(R),{})
	
	for i in xrange(el):
		R[i]  =  compRound(FR[i],14,el)
	
	return R

def FastFourier3SUM(A,B):
	M = max(max(A),max(B))
	
	#print M
	
	bin_A = [0]*(M+1)
	for i in xrange(len(A)):
		bin_A[A[i]]  += 1 
		
	
	bin_B = [0]*(M+1)
	for i in xrange(len(B)):
		bin_B[B[i]]  += 1 
	
	#print bin_A, bin_B
	
	
	return FastFourierMultiply(bin_A,bin_B)
	


## Hull complex
## Sort-like algo with CCW

#X, Y global coordinates
TURN_COUNTER, TURN_CLOCK, TURN_NONE = (1, -1, 0)

class Node:
	
	def __init__(self,index):
		self.index = index
		self.prev = index
		self.next = index

	def setPrev(self, prev):
		self.prev = prev

	def setNext(self, next):
		self.next = next
	
	def __repr__( self ):
		return "next->"+ str(self.next)+ " | prev->"+str(self.prev) + "\n"

def CCW(X, Y, a, b, c):
	return cmp( (Y[c] - Y[a])*(X[b] - X[a]) - (Y[b] - Y[a])*(X[c] - X[a]) , 0)

	
def March(X,Y,N,p):
	q = (p+1)%N
	for i in xrange(2,N):
		t = (p+i)%N
		if CCW(X,Y,p, t, q) == TURN_COUNTER:
			q = t
	
	return q

def JarvisMarch(X,Y):
	ml = 0
	N = len(X)
	for i in xrange(1,N):
		if (X[i] < X[ml]):
			ml = i
	hull = { ml: Node(ml) }
	
	p = ml
	np = March(X,Y,N,p)
	while np != ml :

		hull[np] = Node(np)
		hull[np].setPrev(p)
		hull[p].setNext(np)
		
		p = np
		np = March(X,Y,N,p)
	
	hull[np].setPrev(p)
	hull[p].setNext(np)
	
	return hull
	
def mergeHull(X,Y,p,hull_left,q,hull_right):

	for k in hull_right:
		hull_left[k] = hull_right[k]
	
	#bridges -p, -q
	
	hull_left[-q] = Node(q)
	hull_left[-p] = Node(p)
	
	hull_left[-q].setPrev(hull_left[q].prev)
	hull_left[hull_left[q].prev].setNext(-q)
	
	hull_left[-p].setPrev(hull_left[p].prev)
	hull_left[hull_left[p].prev].setNext(-p)
	
	hull_left[-q].setNext(p)
	hull_left[p].setPrev(-q)
	
	hull_left[-p].setNext(q)
	hull_left[q].setPrev(-p)
	
	
	_mod = 1
	
	# process bridge -q::p
	prev = -q

	while _mod == 1:
		_mod = 0
		cur = prev
		next = hull_left[cur].next
		prev = hull_left[cur].prev
		
		while( CCW(X,Y,abs(cur),abs(prev),abs(next)) == TURN_COUNTER ):
			hull_left[next].setPrev(prev)
			hull_left[prev].setNext(next)
			del hull_left[cur]
			_mod = 1
			#print "deleting ", cur
			cur = prev
			prev = hull_left[cur].prev

	
		cur = next
		next = hull_left[cur].next
		prev = hull_left[cur].prev
		
		while( CCW(X,Y,abs(cur),abs(prev),abs(next)) == TURN_COUNTER ):
			hull_left[next].setPrev(prev)
			hull_left[prev].setNext(next)
			del hull_left[cur]
			_mod = 1
			#print "deleting ", cur
			cur = next
			next = hull_left[cur].prev

	
	_mod = 1
	# process bridge -p::q
	prev = -p
	
	while _mod == 1:
		_mod = 0
		cur = prev
		next = hull_left[cur].next
		prev = hull_left[cur].prev
		
		while( CCW(X,Y,abs(cur),abs(prev),abs(next)) == TURN_COUNTER ):
			hull_left[next].setPrev(prev)
			hull_left[prev].setNext(next)
			del hull_left[cur]
			_mod = 1
			#print "deleting ", cur
			cur = prev
			prev = hull_left[cur].prev
	
		cur = next
		next = hull_left[cur].next
		prev = hull_left[cur].prev

		while( CCW(X,Y,abs(cur),abs(prev),abs(next)) == TURN_COUNTER ):
			hull_left[next].setPrev(prev)
			hull_left[prev].setNext(next)
			del hull_left[cur]
			_mod = 1
			#print "deleting ", cur
			cur = next
			next = hull_left[cur].prev
	
	
	if (-p in hull_left): #p shouldn't be
		next = hull_left[-p].next
		prev = hull_left[-p].prev
		
		del hull_left[-p]
		hull_left[p] = Node(p)
		
		hull_left[p].setNext(next)
		hull_left[next].setPrev(p)
		
		hull_left[p].setPrev(prev)
		hull_left[prev].setNext(p)
	
	if (-q in hull_left): #q shouldn't be
		next = hull_left[-q].next
		prev = hull_left[-q].prev
		
		del hull_left[-q]
		hull_left[q] = Node(q)
		
		hull_left[q].setNext(next)
		hull_left[next].setPrev(q)
		
		hull_left[q].setPrev(prev)
		hull_left[prev].setNext(q)
	
	
	return hull_left
	
		
		
		
		
		
def recurMarch(X,Y,a,b):
	
	l = b-a
	if l == 2:
		hull = {a: Node(a), a+1: Node(a+1), b: Node(b) }
		if (CCW(X,Y,a,a+1,b) == TURN_COUNTER ):
			hull[a].setNext(a+1)
			hull[a+1].setNext(b)
			hull[b].setNext(a)
			
			hull[a].setPrev(b)
			hull[a+1].setPrev(a)
			hull[b].setPrev(a+1)
		else:
			hull[a].setNext(b)
			hull[b].setNext(a+1)
			hull[a+1].setNext(a)
			
			hull[a].setPrev(a+1)
			hull[b].setPrev(a)
			hull[a+1].setPrev(b)
		
		return hull
	elif l == 1:
		hull = {a: Node(a), b: Node(b)}
		hull[a].setNext(b)
		hull[a].setPrev(b)
		hull[b].setNext(a)
		hull[b].setPrev(a)
		return hull
	elif l == 0:
		return {a: Node(a)}
		
	m = (a+b)/2
	
	hull_left = recurMarch(X,Y,a,m)
	hull_right = recurMarch(X,Y,m+1,b)
	
	return mergeHull(X,Y,m,hull_left,m+1,hull_right)
	
def FastJarvisMarch(X,Y):
	#(X,Y) sorted by key X
	#sorted_XY = sorted( [(X[i],Y[i]) for i in range(len(X)) ], key=lambda k: k[0]  )
	#for i in range(len(X)):
	#	X[i] =sorted_XY[i][0]
	#	Y[i] =sorted_XY[i][1]
	
	N = len(X)
	
	return recurMarch(X,Y, 0,N-1)

def ThreePenny(hull,ml,X,Y):
	
	a = hull[ml].next
	b = hull[a].next
	c = hull[b].next
	
	while ( b != ml) :
		if CCW(X,Y,a,b,c) == TURN_COUNTER :
			a = b
			b = c
			c = hull[c].next
		else:
			hull[a].setNext(c)
			hull[c].setPrev(a)
			del hull[b]
			
			a = hull[a].prev
			b = hull[a].next
			c = hull[b].next
	
	return hull
	
def GrahamScan(X,Y):
	ml = 0
	N = len(X)
	for i in xrange(1,N):
		if (X[i] < X[ml]):
			ml = i
			
	hull = { ml: Node(ml) }
	
	cur = ml
	for next in  sorted( [ (ml + i)%N for i in range(1,N)] , cmp=lambda a, b: CCW(X,Y,ml,b,a)):
		hull[next] = Node(next)
		hull[cur].setNext(next)
		hull[next].setPrev(cur)
		cur = next
	
	hull[cur].setNext(ml)
	hull[ml].setPrev(cur)
	
	
	return (ml,ThreePenny(hull,ml,X,Y))

def getTangent(X,Y,hulls_list, hulls, offset, cur_p, tar_h):
	
	S = len(hulls_list[tar_h])
	L = 0
	R = S
	
	cl = hulls_list[tar_h][L]
	L_prev = CCW(X,Y,cur_p, offset[tar_h] + cl, offset[tar_h] +  hulls[tar_h][cl].prev)
	L_next = CCW(X,Y,cur_p, offset[tar_h] + cl, offset[tar_h] +  hulls[tar_h][cl].next)
	
	if (  L_prev != TURN_CLOCK  ) and ( L_next != TURN_CLOCK ):
		return L
		
	
	while L<R:
	
		M = (L+R) / 2
		c = hulls_list[tar_h][M]
		M_prev = CCW(X,Y,cur_p, offset[tar_h] + c, offset[tar_h] +  hulls[tar_h][c].prev)
		M_next = CCW(X,Y,cur_p, offset[tar_h] + c, offset[tar_h] +  hulls[tar_h][c].next)
		M_side = CCW(X,Y,cur_p, offset[tar_h] + cl, offset[tar_h] + c)
		
		
		if (  M_prev != TURN_CLOCK  ) and ( M_next != TURN_CLOCK ):
			return M
			
		if ( ( M_side == TURN_COUNTER ) and ( L_prev == L_next or L_next == TURN_CLOCK ) ) or ( M_side != TURN_COUNTER and M_prev == TURN_CLOCK  ):
			R = M
		
		else:
			#L = M + 1
			#L_Prev = -1 * M_next
			L = M
			cl = hulls_list[tar_h][L]
			L_prev = CCW(X,Y,cur_p, offset[tar_h] + cl, offset[tar_h] +  hulls[tar_h][cl].prev)
			L_Next  = CCW(X,Y,cur_p, offset[tar_h] + cl, offset[tar_h] +  hulls[tar_h][cl].next)
	
	return L 

def Shatter(X,Y,N,h):
	
	if N <= h:
		(ml,hulls) = GrahamScan(X,Y)
		return hulls
	
	_offset = 0 if( N%h == 0) else 1
	parts = (N/h) + _offset

	hulls = [0] * ( parts )
	hulls_list = [0] * ( parts )
	offset = [0] * ( parts )
	
	
	_s = 0
	_e = h
	for i in range(parts):
		offset[i] = _s
		(ml,hulls[i]) = GrahamScan(X[_s:_e],Y[_s:_e])
		l = len(hulls[i])
		hulls_list[i] = [0]*(l)
		
		hulls_list[i][0] = ml
		for j in range(1,l):
			ml = hulls[i][ml].next
			hulls_list[i][j] =  ml
		
		_s = _e
		_e = _e + h
	
	
	#print hulls
	#print hulls_list
	
	
	
	cur_h = 0
	cur_p = 0
	
	final_hull = {0: Node(0)}
	for j in range(1,h+1):
		
		next_p  =  offset[cur_h]  + hulls[cur_h][cur_p - offset[cur_h]].next 
		next_h = cur_h
	
		for i in range(1,parts):
			tar_h = (cur_h+i)%parts
			t = offset[tar_h] + hulls_list[tar_h][getTangent(X,Y,hulls_list, hulls, offset, cur_p, tar_h)]
			if CCW(X,Y,cur_p, t, next_p) == TURN_COUNTER:
				next_p  = t
				next_h = tar_h
	
	
		if next_p == 0:
			final_hull[cur_p].setNext(next_p)
			final_hull[next_p].setPrev(cur_p)
			return final_hull
			
		final_hull[next_p] = Node(next_p)
		final_hull[cur_p].setNext(next_p)
		final_hull[next_p].setPrev(cur_p)
		
		
			
		#print cur_p, cur_h, " === " ,next_p , next_h
		cur_p = next_p
		cur_h = next_h
	
	
	return None
	
def ChanShatter(X,Y):
	
	ml = 0
	N = len(X)
	for i in xrange(1,N):
		if (X[i] < X[ml]):
			ml = i
	
	#swap ml and 0
	if (ml != 0):
		tmp_X = X[0]
		tmp_Y = Y[0]
		X[0] = X[ml]
		Y[0] = Y[ml]
		X[ml] = tmp_X
		Y[ml] = tmp_Y
	
	#print ml
	
	h = 3 #3
	hulls = None
	while (hulls == None):
		#print "h ", h
		hulls = Shatter(X,Y,N,h)
		h = h*3
	
	return hulls