#include <stdio.h>

void give_shell(void){
    system("/bin/sh");
}

void vuln(void){
    char buf[32] = {};

    printf("Input1 > ");
    read(0, buf, 512);

    printf(buf);

    printf("Input2 > ");
    read(0, buf, 512);
}

int main(void){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    vuln();
}

