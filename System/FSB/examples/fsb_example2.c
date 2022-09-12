// gcc -o fsb_example2 fsb_example2.c
#include <stdio.h>
int main()
{
	int ret = 0;
	printf("1234%1$n\n", &ret);
	printf("ret: %d\n", ret);
}
