import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))

import client as clt
from tools import *
import configparser as cp

RSA_REDUC = "/RSA-reductions"
CHALLENGE_URL = RSA_REDUC + "/phi/challenge/" + NAME

PHI = "phi"
E = "e"
N = "n"
CHALLENGE_SECTION = "challenge"

def get_challenge():
    srv = clt.Server(BASE_URL)
    try:
        param = srv.query(CHALLENGE_URL)
        return param[PHI], param[E], param[N]
    except clt.ServerError as err:
        print_serverError_exit(err)

# def save_challenge(phi, e, n):
#     conffile = open("challenge.ini", 'w')
#     conffile.write("[" + CHALLENGE_SECTION + "]")
#     conffile.write("\nphi=" + str(phi))
#     conffile.write("\nn=" + str(n))
#     conffile.write("\ne=" + str(e))
#     conffile.close()

# def read_challenge(file="challenge.ini"):
#     config = cp.ConfigParser()
#     config.read

def isqrt(n):
    """ renvoie le plus grand entier k tel que k^2 <= n. Méthode de Newton."""
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x
    
if __name__ == "__main__":
    phi, e, n = get_challenge()
    print(PHI  + ": "  + str(phi))
    print("==============")
    print(E  + ": "  + str(e))
    print("==============")
    print(N  + ": "  + str(n))
    print("==============")

    sqrt_n = isqrt(n)
    print("sqrt : " + str(sqrt_n))

    # When it's cold outside, I like to run this script
    for p in range(sqrt_n, 1, -1):
        print("new p")
        for q in range(sqrt_n, 1, -1):
            if phi == n - (p + q - 1):
               srv = clt.Server(BASE_URL) 
               print(srv.query("</RSA-reductions/phi/check/dewarumez"))
               exit(0)
    

