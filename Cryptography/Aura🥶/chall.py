from base64 import b64encode
import random

flag = "SMKN22{Mas_nya_sigma_aura_banget_tapi_emang_iya?}"
big_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
small_chars = "abcdefghijklmnopqrstuvwxyz"

random.seed(0xdeadbeef)
def encrypt(msg, key):
    encrypted = ""
    for i in msg:
        if i.isalpha():
            if i.isupper():
                encrypted += big_chars[(big_chars.index(i) + key) % len(big_chars)]
            else:
                encrypted += small_chars[(small_chars.index(i) + key) % len(small_chars)]
        else:
            encrypted += i
    return encrypted

def write(name, msg):
    with open(name, 'w') as f:
        f.write(msg)
    return True

def main():
    key = random.randint(1, 255)
    enc = encrypt(flag, key)
    enc2 = b64encode(enc.encode()).decode()
    write('flag.enc', enc2)

if __name__ == '__main__':
    main()
