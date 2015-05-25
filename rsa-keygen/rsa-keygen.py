import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
from tools import *
import math
import random
from fractions import gcd

KEY_GEN = "/RSA-keygen"
CHALLENGE_URL = KEY_GEN + "/challenge" + NAME
PK_URL = KEY_GEN  + "/PK" + NAME
CONFIRM_URL = KEY_GEN + "/confirmation" + NAME

PRIMES_SECTION = "Primes"
P_SECTION = "p"
Q_SECTION = "q"

E = 'e'
N = 'n'
M = 'm'

CIPHER = "ciphertext"

def est_premier(p):
	if p == 1:
		return False
	if p == 2:
		return True
	if p % 2 == 0:
		return False
	if p % 10 == 5:
		return False

	p_str = str(p)
	sum_digits = 0
	for digit_str in p_str:
		sum_digits += int(digit_str)
	if sum_digits % 3 == 0:
		return False

	sqr = math.sqrt(p)
	cpt = 3
	while(cpt <= sqr):
		if(p % cpt == 0):
			return False
		cpt += 2

	return True

def get_challenge():
	"""Return the e part of the private key"""
	print("Retreiving challenge from the server...")
	srv = clt.Server(BASE_URL)
	try:
		return srv.query(CHALLENGE_URL)[E]
	except clt.ServerError as err:
		print_serverError_exit(err)

def send_key(e, n):
	"""Send the key to the server. And return the cipher given by the server"""
	print("sending the key to the server...")
	param = {N: n, E: e}
	srv = clt.Server(BASE_URL)
	try:
		result = srv.query(PK_URL, param)
		return int(result[CIPHER])
	except clt.ServerError as err:
		print_serverError_exit(err)

def decipher(c, d, n):
	return pow(c, d, n)

def send_message(message):
	"""Send the message to the server."""
	param = {M : message}
	srv = clt.Server(BASE_URL)
	print("sending the message to the server...")
	try:
		result = srv.query(CONFIRM_URL, param)
		print(result)
	except clt.ServerError as err:
		print_serverError_exit(err)

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

if __name__ == "__main__":
	p = q = e = n = d = None
	if not os.path.exists("../primes.ini"):
		print("Computing big number...")
		p = compute_big_prime();
		q = compute_big_prime();
		save_primes(p, q)
	else:
		print("Reading primes numbers from file...")
		p, q = read_primes()
	e = get_challenge()
	n = p*q
	d = modinv(e, (p-1)*(q-1))

	if gcd((p - 1)*(q - 1), e) == 1:
		print("p and q are correct!\n:-)")
	else:
		print("p and q are not correct!\n:-(")
		exit(1)

	cipher = send_key(e, n)
	message = decipher(cipher, d, n)
	send_message(message)
