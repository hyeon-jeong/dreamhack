// gcc -o init_fini_array init_fini_array.c -Wl,-z,norelro
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

void alarm_handler() {
    puts("TIME OUT");
    exit(-1);
}

void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, alarm_handler);
    alarm(60);
}

int main(int argc, char *argv[]) {
    long *ptr;
    size_t size;

    initialize();

    printf("stdout: %p\n", stdout); //edi, 0x400acd

    printf("Size: ");
    scanf("%ld", &size); 

    ptr = malloc(size); // size(rbp-0x18)

    printf("Data: ");
    read(0, ptr, size); // size(rbp-0x18), ptr(rbp-0x10)

    *(long *)*ptr = *(ptr+1);
   
    free(ptr);
    free(ptr);  // call 0x400770 <free@plt>

    system("/bin/sh"); // call 0x400788 <system@plt>, "/bin/sh" 0x400aeb
    return 0;
}
