
#include <stdio.h>
int secret;
int main() {
  char format[0x100];
  printf("Address of `secret`: %p\n", &secret);
  printf("Format: ");
  scanf("%[^\n]", format);
  printf(format);
  printf("Secret: %d", secret);
  return 0;
}