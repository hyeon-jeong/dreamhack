#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main(){
    char buf[8] = {};
    char secret[16] = {};

    strcpy(secret, "secret message");
    read(0, buf, 10);

    printf("%s\n", buf);
}