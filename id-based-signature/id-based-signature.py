import os
import sys
import os.path
sys.path.append(os.path.join(os.getcwd(), '..',))

import client as clt
from tools import *
import hashlib
import random
import base64

ID_SIGNATURE = "/id-based-signature"
KEY_DIST_CENTER = "/KDC"
P_KEY = "/PK"
KEYGEN = "/keygen"

KDC_GET_PK_URL = ID_SIGNATURE + KEY_DIST_CENTER + P_KEY
KDC_GET_SK_URL = ID_SIGNATURE + KEY_DIST_CENTER + KEYGEN + NAME
KDC_CHCK_URL   = ID_SIGNATURE + "/check/" + NAME

N = "n"
E = "e"
S = "s"
T = "t"
M = "m"

SECRET_KEY = "secret-key"

def get_kdc_pub_key():
    srv = clt.Server(BASE_URL)
    try:
        param = srv.query(KDC_GET_PK_URL)
        return param[N], param[E]
    except clt.ServerError as err:
        print_serverError_exit(err)

def get_secret_key():
    srv = clt.Server(BASE_URL)
    try:
        return srv.query(KDC_GET_SK_URL)[SECRET_KEY]
    except clt.ServerError as err:
        print_serverError_exit(err)

def sign(s_key, n, e, message="yoloswag"):
    msg_byte = message.encode()
    r = random.randint(1, n-1)    
    t = pow(r, e, n)
    sha256 = hashlib.sha256()
    t_hex = "{0:0512x}".format(t)
    t_bytes = base64.b16decode(t_hex.encode(), casefold=True)
    m_t = msg_byte + t_bytes
    sha256.update(m_t)
    s = s_key * pow(r, int(sha256.hexdigest(), base=16), n) % n
    return {S:s, T:t, M: message} 

if __name__ == "__main__":
    n, e = get_kdc_pub_key()
    s_key = get_secret_key()
    r = random.randint(1, n -1)

    srv = clt.Server(BASE_URL)
    print(srv.query(KDC_CHCK_URL, sign(s_key, n, e)))
