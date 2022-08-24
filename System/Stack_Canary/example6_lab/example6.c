#include <stdio.h>

void give_shell(){
    system("/bin/sh");
}

int main(void){
    char buf[32] = {};

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    printf("Input1 : ");
    read(0, buf, 512);
    printf("Your input : %s", buf);
    printf("Input2 : ");
    read(0, buf, 512);
}