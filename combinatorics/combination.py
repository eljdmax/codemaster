#!/bin/python
import time
import math
 
#from decimal import *
#getcontext().prec = 50
from Queue import PriorityQueue
from itertools import chain, combinations
 
#import bisect
 
#pi = pi / Decimal(10**100)

def get_base_digits(n,b):
	d = []
	while n > 0:
		d.append(n % b)
		n  = n // b

	return d

# get degree of p in n! (exponent of p in the factorization of n!)
def fact_exp(n,p):
	e = 0
	u = p
	t = n
	while u <= t:
		e += t//u
		u *= p

	return e
	
	
# Extended Euclidean GCD
# compute x,y for ax + by = gcd(a,b)
# here, a,b are coprime, meaning gcd(a,b) = 1
def egcd(a, b):
	x,y, u,v = 0,1, 1,0
	while a != 0:
		q, r = b//a, b%a
		m, n = x-u*q, y-v*q
		b,a, x,y, u,v = a,r, u,v, m,n
	gcd = b
	return (x, y)
	
	

def crt(congruences, m):
	
	# combine congruences
	result = 0
	for congruence in congruences:
		s, t = egcd(m//congruence[1],congruence[1])
		result += (congruence[0]*s*m)//congruence[1]

	return result%m
	
	
def lucas(n, k, p):
	
	dn = get_base_digits(n,p)
	dk = get_base_digits(k,p)
	
	delta =  len(dn) - len(dk)
	if ( delta > 0 ):
		dk.extend( [0] * delta)
	elif ( delta < 0 ):
		delta = -1 * delta
		dn.extend( [0] * delta)
		
	
#print dn
	#print dk
	
	work = []
	for i in range(len(dn)):
		if (dk[i] > dn[i]):
			return 0
		
		if (dk[i] < dn[i]):
			work.append( (dn[i] , dk[i]) )
		
	sol = 1
	for elem in work:
		sol  = (sol * fermat_binom_advanced(elem[0], elem[1], p) ) % p
	
	return sol
	
	
# Using Fermat's little theorem to compute nCk mod p
# considering cancelation of p in numerator and denominator
# Note: p must be prime
def fermat_binom_advanced(n,k,p):
	# check if degrees work out
	num_degree = fact_exp(n,p) - fact_exp(n-k,p)
	den_degree = fact_exp(k,p)
	if num_degree > den_degree:
		return 0

	# calculate numerator and cancel out occurrences of p
	num = 1
	for i in range(n,n-k,-1):
		cur = i
		while cur%p == 0:
			cur //= p
		num = (num*cur)%p

	# calculate denominator and cancel out occurrences of p
	denom = 1
	for i in range(1,k+1):
		cur = i
		while cur%p == 0:
			cur //= p
		denom = (denom*cur)%p

	# numerator * denominator^(p-2) (mod p)
	return (num * pow(denom,p-2,p))%p
	
def compute(n,k, facts, m):
	# build congruences for all prime factors
	congruences = []
	for p in facts:
		# add (binom,p) to congruence list
		congruences.append((lucas(n,k,p),p))

	# use CRT to combine congruences to one solution
	return crt(congruences, m)

def loopFacto(k,top,facto):
	sol = facto[top-1]
	for i in range(top,k+1):
		sol = i*sol
		
	return sol

def extendedFacto(x, p, facto):

	m = x//p
	
	return facto[x]  / (facto[m] * (p**m)  )
	

def theo2(u, p , r, exFacto, facto, _mod, target_mod, target_totient):
	
	if u == 1:
		return exFacto[p] % target_mod
	
	
	beta = [0] * (r+1) #1 to r

	#print r
	
	_exclude = -1
	mul = 1
	for i in range(1,r+1):
		if (u == i):
			_exclude = i
		else:
			mul *= (u*u-i*i)
	
	#print mul, top
	if (_exclude != -1):
		beta[_exclude] = ( u * mul   ) 
		denom = _exclude
		for i in range(1,r+1):
			if i != _exclude :
				denom *= (_exclude*_exclude - i*i)
				
		beta[_exclude] = beta[_exclude] / denom
		
	else:
		for j in range(r, 0, -1):
			beta[j] = ( u * mul / (u*u - j*j)  ) 
			denom = j
			for i in range(1,r+1):
				if i != j :
					denom *= (j*j - i*i)
			
			
			beta[j] = beta[j] / denom
	
	#print beta

	
	combi = 1
	test = u/2
	n = 0
	for j in range(1,r+1):
		n += p
		if ( not n in exFacto ):
			exFacto[n] = extendedFacto(n,p,facto)
		
		test += (j/2) * beta[j] 
		
		if beta[j] >= 0:
			val =  pow( exFacto[n], beta[j], target_mod)  # alpha[j]%_new_mod ???
		else:
			val =  pow( pow( exFacto[n] , target_totient-1,target_mod) , -1* beta[j] , target_mod )
		
		combi = (combi * val) % target_mod
	
	#print _inv, combi
	_inv = 1
	if (p==2) and (test%2 == 1):
		_inv = -1
	
	_combi = (_inv * combi) % target_mod
	  
	return _combi  
	
	
def extendedFacto2(x, p, q, _mod, facto):
	v = x%p
	u = x/p
	
	#print u, v
	
	alpha = [0] * q #1 to q-1
	
	_new_mod = _mod/p #????
	
	_exclude = -1
	mul = 1
	for i in range(1,q):
		if (u == i):
			_exclude = i
		else:
			mul *= (u-i)
	
	
	
	
	
	if (_exclude != -1):
		alpha[_exclude] = ( u * mul  ) 
		denom = _exclude
		for i in range(1,q):
			if i != _exclude :
				denom *= (_exclude - i)
				
		alpha[_exclude] = alpha[_exclude] / denom  #cumu??
		
	else:
		top = q-2
		_sign = 1
		for j in range(q-1, 0, -1):
			alpha[j] = ( u * mul / (u - j)  ) / ( _sign * j * facto[top]* facto[q-2-top])
			_sign = _sign*-1
			top -= 1

		
	#print alpha
	
	exFacto = { 0:1, 1:1}
	n = v
	m = 0
	if ( not v in exFacto ):
		exFacto[v] = extendedFacto(v,p,facto)
		
	totient = _mod - (_mod/p)
	
	combi = 1
	for j in range(1,q):
		n += p
		m += p
		if ( not n in exFacto ):
			exFacto[n] = extendedFacto(n,p,facto)
			
		if ( not m in exFacto ):
			exFacto[m] = extendedFacto(m,p,facto)
		
		x =  (exFacto[n] *  pow(exFacto[m] * exFacto[v], totient-1,_mod) ) % _mod ## with modulo ?

		if alpha[j] >= 0:
			val =  pow(x, alpha[j], _mod)  # alpha[j]%_new_mod ???
		else:
			val =  pow( pow(x, totient-1,_mod) , -1* alpha[j] , _mod )
		
		combi = (combi * val) % _mod
	
	#print combi
	
	if ( not p in exFacto ):
		exFacto[p] = extendedFacto(p,p,facto)
		
	
	r = q/2
	new_q  = 2*r + 1
	if ( p**r == 2) or ( new_q  == p) or ( new_q == p*p):
		new_q -= 1
	
	if (new_q < q):
		r += 1
		new_q = 2*r + 1
		if (p**r == 2) or (new_q == p) or (new_q == p*p):
			new_q -= 1
	
	#print r, new_q
	target_mod, target_totient = p**new_q , p**new_q - p**(new_q-1)
	
	
	return ( exFacto[v] *  ( theo2(u, p , r, exFacto, facto,  _mod, target_mod, target_totient) % _mod ) * combi ) %_mod
	
	

	

def process(n, k, elem, _mod, facto):
	
	p, q = elem
	
	if q == 1:
		return lucas(n, k, p)
	
	r = n - k
		
	
	dn = get_base_digits(n,p)
	dk = get_base_digits(k,p)
	
	delta =  len(dn) - len(dk)
	if ( delta > 0 ):
		dk.extend( [0] * delta)
		
	
	dr = get_base_digits(r,p)
	delta =  len(dn) - len(dr)
	if ( delta > 0 ):
		dr.extend( [0] * delta)
	
	
	d = len(dn)
	
	N = [0]*d
	M = [0]*d
	R = [0]*d
	E = [0]*d
	
	if (dk[0] + dr[0]) >= p:
		E[0] = 1
	for i in range(1,d):
		if (dk[i] + dr[i] + E[i-1]) >= p:
			E[i] = 1
	
	
	N[d-1] = dn[d-1]
	M[d-1] = dk[d-1]
	R[d-1] = dr[d-1]
	
	for i in range(d-2, -1, -1):
		N[i] = (dn[i] + p*N[i+1]) % _mod
		M[i] = (dk[i] + p*M[i+1]) % _mod
		R[i] = (dr[i] + p*R[i+1]) % _mod
		
		E[i] = E[i] + E[i+1]
		
	
	totient = _mod - (_mod/p)
	
	num = 1
	denom = 1
	
	exFacto = { 0:1, 1:1}
	
	for i in range(d):
		if ( not N[i] in exFacto ):
			exFacto[N[i]] = extendedFacto2(N[i],p,q,_mod,facto)
		if ( not M[i] in exFacto ):
			exFacto[M[i]] = extendedFacto2(M[i],p,q,_mod,facto)
		if ( not R[i] in exFacto ):
			exFacto[R[i]] = extendedFacto2(R[i],p,q,_mod,facto)
			
		num = (num * exFacto[N[i]] ) % _mod
		denom =  (denom * exFacto[M[i]] * exFacto[R[i]] ) % _mod
		
	
	if ((p == 2) and (q >= 3)) or (q > d):
		_sign = 1
	else:
		_sign = (-1)**(E[q-1])
	
	
	sol =  (_sign*num * pow(denom,totient-1,_mod))%_mod

	return ( sol * (p**E[0]) ) % _mod
	
	
def compute2(n,k, facts, m, facto):
	# build congruences for all prime factors
	congruences = []
	for elem in facts:
		# add (binom,p) to congruence list
		_mod = elem[0]**elem[1]
		congruences.append((process(n,k,elem,_mod,facto),_mod))

	# use CRT to combine congruences to one solution
	return crt(congruences, m)
	

def get_div(x):
	_top = 10**3
	
	num = []
	
	for i in range(2,_top):
		if (x%i) == 0:
			q = 0
			while (x%i) == 0 :
				x //= i
				q += 1
				
			num.append( (i,q) )
			
			if x == 1:
				return num
				
	num.append( (x,1) )
	
	return num
	
def main():
	
	import sys
	#from operator import itemgetter
	#from sets import Set
	
	_top= 20001
	facto = [1]*_top
	
	for i in range(2,_top):
		facto[i] = i*facto[i-1]
	
	
	T = int(sys.stdin.readline().strip())
	
	for _ in range(T):
		(N, K, M) = map(int , sys.stdin.readline().strip().split())
	
		alpha = N/K
		beta = K - (N%K)
	
		if beta == K:
			print alpha, 1
			continue
		
		print alpha+1, compute2(beta+alpha, alpha, get_div(M), M, facto)
		
	
	
	
def test():
	#15 = 3*5
	#facts = [2, 3, 5, 11, 19]
	#print compute(92,10, facts, 2*3*5*11*19 )
	
	
	_top = 20001
	facto = [1]*_top
	
	for i in range(2,_top):
		facto[i] = i*facto[i-1]
		
		
	#print extendedFacto2(3, 3,3 , 3**3, facto)
	
	# print compute2(16, 5, get_div(3**3), 3**3, facto) 
	# return 
	#exFacto = {}
	
	
	#2,2,2 ,, 
	# for p in  [ 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199] :
	# #for p in [7]:
		# exFacto = {}
		# exFacto[p] = extendedFacto(p,p,facto)
			
		# #for q in range(6,7):
		# for q in range(2,(50 / p) + 3):
			# _mod = p**q 
			
			# r = q/2
			# new_q  = 2*r + 1
			# if ( p**r == 2) or ( new_q  == p) or ( new_q == p*p):
				# new_q -= 1
			
			# if (new_q < q):
				# r += 1
				# new_q = 2*r + 1
				# if (p**r == 2) or (new_q == p) or (new_q == p*p):
					# new_q -= 1
			
			# #print r, new_q
			# target_mod, target_totient = p**new_q , p**new_q - p**(new_q-1)
			
			# for u in range(100,1000): #for u in range(2,100):
				
				# #print ":", theo2(u, p , r, exFacto, facto,  _mod, target_mod, target_totient)  ,  extendedFacto(u*p,p,facto)% target_mod
				# val = theo2(u, p , r, exFacto, facto,  _mod, target_mod, target_totient)
				# if  val != extendedFacto(u*p,p,facto)%target_mod :
					# print p,q,u
					# return
	
	# return 
	
	
	#print compute2(12,10, facts, 4 )
	
	#print process(33,17,facts[0],8) # 1166803110
	#print process(33,19,facts[0],4) # 818809200
	#print process(55,18,facts[0],8)  # 144079707346575
	#print process(16,5,facts[0],27)  #4368 
	
	
	#print process(33,17,facts[0],3**3, facto) # 4950
	
	#print compute2(33,17,facts,167*167*23, facto) , 1166803110 % (167*167*23)
	
	# for i in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]:
		# #print process(55,18, get_div(i**2), i**2), 144079707346575 % i**2
		# for k in range(6,15):
			# if process(33,17, (i,k), i**k, facto) != 1166803110 % (i**k) :
				# print i, k
	
	
	
	# for k in range(2,10**6):
		# if compute2(10000,5000,get_div(k), k, facto) != 159179026353243894833759727364152118865300583745761455042831910351777263712009579866326285394422221774335859829932262055804632908708020739850879872195958489620417578664585801840995875120689143315978135317405145347319967052139450253847727733600831205378448823951274321755502883180927364644281795459349368900235462880547366282927213220919726803062157839769855248683450847868894994611262023360235298989458928488427591110374321646235202929095545845304023492927787143123978410362592908300075421733055365492425368306281530729653340889255650690875150647615944622376204326852230062678211259375951657115342848245333181068684095284004284699504359257817996430741389422649447586626281862183757541280362546881388544759125956185871468454381861463662350728468211441655465743993284005794170022128691686189379747227886202239788372897602049671018976190617859305826168808117556117796960379809282174855477301204105813490546271598511886613777441541105636943056820725244819431050256487494579628837604295079872914178005301024149340722579759834860211640098545723183096418633688898312145597072469454456651789081935386062566029368316522506271595824234037562793787332887113614352737971292965638066368798136853809235306441396478979814279989804419587974310478889401271971015441216840096344652939528524306710003806696307699257220104426311836533049067512198270012436774453339363870022811792535618814009571973175044979333952276086203573893932977683234377126461503016956149960119508206705891127875644018328002477885570580594271739655617247279703665698618080801965541235756564655565433970795513642117996823482940891493286717047038936158996297545140449708716896119990505242038078767450450863985246304067167020269491256064620583001761300622284757510662566106193771435587218537809620026913816305961756296827876710659465040754767228071475821687019166324258201685893281454941849633219010250326331594361831605955344426680189751351988451293306946591872301020473208721181284611163964165765568933940740976656925878728168406935207314430178725136178015792747114729015831170907171194578298482944164359840658473384707719418659651955333974514346503817616197612616157040354559466774548777412765471478663541418800111962602957335265945686584369721309686983612640564990207924247805354140963069566603071195931569172626802351518208786515546937379638760504643715547953097876650816797000176926659286918757094175117347665748132703540903393455409827319346571309202004128279611588827972847323501797969972562671972826347017756606331304016075551520523318404592756797612244679324194846919392918520452394577675953326869067443192793756095658856432124228522403516658454319704009054696329636363817791559641205005685702690372838060388519713403611629040056633420468941761593824568608770545269390456038883755973215629222766342326791030991205489279359135464145696802130792488795541350742383065293811197486421347908348956557941526999776837834147059039199747891501916363639677591945387535180152498052210450701705508838093544209022455222930021060372371375638589078163387440553649120  % k :
			# print k 
			# return 
	
	n = (101**2)*(43**2)
	print compute2(10**17,2,get_div( n ), n  , facto)
	
	print ((10**17 * (10**17 - 1)) /2 ) % n
			
if __name__ == "__main__":
	
	#s= time.time()
	main()
	#test()

	#print time.time()-s  