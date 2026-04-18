from Crypto.Util.number import *

flag = b'AAAAAAAAAAA'
e = 65537

p,q = [getPrime(301) for _ in range(2)]
n   = p*q

pt = bytes_to_long(flag)
ct = pow(pt,e,n)


print(f"p = {p}")
print(f"q = {q}")
print(f"ciphertext = {ct}")
print(f"e = {e}")