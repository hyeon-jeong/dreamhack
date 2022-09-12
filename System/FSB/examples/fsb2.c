#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
void initialize() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
}
void get_shell() {
	system("/bin/sh");
}
int main()
{
	char buf[256];
	initialize();
	memset(buf, 0, sizeof(buf));
	printf("Input: ");
	read(0, buf, sizeof(buf)-1);
	printf(buf);
	exit(0);
}























