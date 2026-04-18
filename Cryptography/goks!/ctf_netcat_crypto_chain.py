import socket
import threading
import os
import sys
import base64
import binascii
import random
import time

HOST = '0.0.0.0'
PORT = 7766

WORDS = [
    'kubra lompat','nasi uduk','gorengan panas','kopi manis','baju kebesaran','sepeda rusak',
    'ayam kampung','pisang goreng','sate manis','sambel pedas','bebek nyasar','mie ayam',
    'pizza kebakar','burger jumbo','kentang goreng','kerupuk renyah','telur dadar','tahu bulat',
    'tempe goreng','eskrim coklat','bola kecil','boneka lucu','topi unik','jaket tebal',
    'sepatu baru','gitar klasik','drum keras','piano tua','lampu nyala','meja kayu',
    'kursi goyang','laptop lemot','monitor besar','keyboard rusak','mouse geser','lampion merah',
    'balon merah','kaos basah','jaket hujan','tas sekolah','kancut superman','sandal swalow',
    'botol plastik','gelas pecah','sendok panjang','garpu bengkok','piring cantik','mangkok besar','kipas angin'
]

def rot13_encode(s: str) -> str:
    def rot13_char(c):
        o = ord(c)
        if 65 <= o <= 90:
            return chr((o - 65 + 13) % 26 + 65)
        if 97 <= o <= 122:
            return chr((o - 97 + 13) % 26 + 97)
        return c
    return ''.join(rot13_char(c) for c in s)

def rot47_encode(s: str) -> str:
    out = []
    for ch in s:
        o = ord(ch)
        if 33 <= o <= 126:
            out.append(chr(33 + ((o - 33 + 47) % 94)))
        else:
            out.append(ch)
    return ''.join(out)

def ascii_numeric_encode(s: str) -> str:
    return ' '.join(str(ord(c)) for c in s)

STAGES = [
    ('base64', lambda s: base64.b64encode(s.encode()).decode(), 20),
    ('base32', lambda s: base64.b32encode(s.encode()).decode(), 15),
    ('rot13',  lambda s: rot13_encode(s), 10),
    ('rot47',  lambda s: rot47_encode(s), 5),
    ('ascii',  lambda s: ascii_numeric_encode(s), 5),
    ('hex',    lambda s: binascii.hexlify(s.encode()).decode(), 5),
]

FLAG = 'SMKN22{horeeee_wkwkwkwkwkw_seneng_dong😂}'

WELCOME = (
    "*** Selamat datang di Dunia Crypto Super Gokil!🤗 ***\n"
    "Siap-siap nerima 6 string gokil yang bikin ketawa dan garuk kepala!😅\n"
    "Aturan main: jawab dengan kata-kata yang sesuai, jangan ngasal!🤪\n\n"
)

def generate_plaintext():
    return random.choice(WORDS)

# Fungsi safe_send untuk mencegah BrokenPipeError
def safe_send(conn, text):
    try:
        conn.sendall(text.encode('utf-8'))
    except (BrokenPipeError, ConnectionResetError):
        pass

def send_slow(conn, text, delay=0.03):
    try:
        for ch in text:
            safe_send(conn, ch)
            time.sleep(delay)
    except Exception:
        pass

def progress_bar_text(remaining, total, width=30):
    frac = max(0.0, min(1.0, remaining / total))
    filled = int(frac * width)
    bar = '[' + ('=' * filled) + (' ' * (width - filled)) + ']'
    return f"(waktu {total}s) Sisa waktu: {remaining:2d}s {bar}"

def show_countdown(conn, total):
    try:
        for rem in range(total, 0, -1):
            line = '\r' + progress_bar_text(rem, total)
            safe_send(conn, line)
            time.sleep(1)
        safe_send(conn, '\r' + ' ' * 80 + '\r')
    except Exception:
        pass

def recv_with_timeout(conn, timeout):
    conn.settimeout(timeout)
    try:
        data = b''
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                return None
            data += chunk
            if b'\n' in data:
                line, _, _ = data.partition(b'\n')
                return line.decode('utf-8', errors='ignore')
    except socket.timeout:
        return None
    finally:
        conn.settimeout(None)

def handle_client(conn, addr):
    try:
        send_slow(conn, WELCOME)
        for i, (name, encoder, timeout) in enumerate(STAGES):
            plaintext = generate_plaintext()
            encoded = encoder(plaintext)

            safe_send(conn, "\n")
            safe_send(conn, f"sung ah: {name.upper()}\n")
            safe_send(conn, f"Decode ini deh: {encoded}\n")

            show_countdown(conn, timeout)

            safe_send(conn, "Jawaban nye ape nih? : ")
            answer = recv_with_timeout(conn, 5)

            if answer is None:
                safe_send(conn, f"\nUps, nggak ngejawab sama sekali! masa gak bisa sih?😫, yaudah deh sampe ketemu lagi.\n ouhh yaa Jawaban benernya: {plaintext}\n")
                return
            if answer.strip() != plaintext:
                safe_send(conn, f"\nWaduh salah lagi!😳 Jawabannya tuh: {plaintext}. wkwkwkwkwkwk nice-try'\n")
                return
            else:
                # cek apakah ini tahap terakhir
                if i == len(STAGES) - 1:
                    safe_send(conn, "\nYeay, bener!🤩 keren juga lho.\n")
                else:
                    safe_send(conn, "\nYeay, bener!🤩 keren juga lho. Lanjut yee, yang SEMANGAT yaa\n")

        send_slow(conn, f"\nSemua tahap selesai! Kamu gokil banget! mau flag? tungguin yaa bentar servernya ngantuk kwkwkwwkwk'\n")
        send_slow(conn, f"bercandaaa ini flagnya: {FLAG}\n")
    finally:
        conn.close()

def start_server():
    print(f"MEmulai server Crypto Gokil di {HOST}:{PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(6)
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print('\nyaaa kok ninggalin?, akuh padahal gak mau kamu pergi')
    finally:
        s.close()

if __name__ == '__main__':
    start_server()
