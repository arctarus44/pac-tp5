import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))

import client as clt
from tools import *
import random
from fractions import gcd
import hashlib

RABIN = "/Rabin-signature/"
CHALLENGE_URL = RABIN + "challenge" + NAME

PRIMES_SECTION = "Primes"
P_SECTION = "p"
Q_SECTION = "q"

N = "n"
M = "m"

def is_square(apositiveint):
	x = apositiveint // 2
	seen = set([x])
	while x * x != apositiveint:
		x = (x + (apositiveint // x)) // 2
		if x in seen:
			return False
		seen.add(x)
	return True

def compute_big_prime(size=2048):
	"""Return a big prime number"""
	i = 1
	while True:
		prime = random.getrandbits(size)
		if est_premier(prime):
			return prime
		else:
			print("attempt no " + str(i))
			i+=1

def save_primes(p, q):
	primes_f = open(filename, 'w')
	primes_f.writelines("[" + PRIMES_SECTION  + "]" + "\n")
	primes_f.writelines(P_SECTION + " = " + str(p) + "\n")
	primes_f.writelines(Q_SECTION + " = " + str(q) + "\n")
	primes_f.close()

def read_primes():
	import configparser as cp
	p_key = cp.ConfigParser()
	p_key.read("../primes.ini")
	p = int(p_key[PRIMES_SECTION][P_SECTION])
	q = int(p_key[PRIMES_SECTION][Q_SECTION])
	return p, q

def get_message(n):
	print("Sending public key to the server...")
	srv = clt.Server(BASE_URL)
	try:
		return srv.query(CHALLENGE_URL, {N: n})[M]
	except clt.ServerError as err:
		print_serverError_exit(err)

def sign(message):
	sha = hashlib.sha256()
	padding = random.getrandbits(128)
	y = int(str(message) + str(padding), base=16)
	sha.update(bytes(y))
	while not is_square(sha.digest()):
		print("attempt")
		padding = random.getrandbits
		y = int(str(message) + str(padding), base=16)
		sha.update(y)
	print("find it")
	# x = math.sqrt(btes(message + padding))



if __name__ == "__main__":
	p = q = n = b = None
	if not os.path.exists("../primes.ini"):
		print("Computing big number...")
		p = compute_big_prime();
		q = compute_big_prime();
		save_primes(p, q)
	else:
		print("Reading primes numbers from file...")
		p, q = read_primes()
	n = p*q
	b = random.randint(2, n - 1)
	m = get_message(n)
	print(type(m))
	print(m)
	sign(m)
