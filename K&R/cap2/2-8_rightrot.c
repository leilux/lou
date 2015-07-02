#include<stdio.h>

/* rightrot: rotate x to the right by n positions */
unsigned rightrot(unsigned x, int n)
{
	int wordlength(void);
	int rbit;

	while (n-- > 0) {
		rbit = (x & 1) << (wordlength() - 1);
		x = x >> 1;
		x = x | rbit;
	}
	return x;
}

int wordlength(void)
{
	int i;
	unsigned v = (unsigned) ~0;

	for (i = 1; (v = v >> 1) > 0; i++)
		;
	return i;
}

main()
{
	int n = 4;
	unsigned x = 0xfffffff1;
	printf("rotate %x to the right by %d positions is %x\n", x, n, rightrot(x, n));
}
