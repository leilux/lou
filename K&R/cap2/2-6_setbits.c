#include<stdio.h>

/* setbits: set n bits of x at position p with bits of y */
unsigned setbits(unsigned x, int p, int n, unsigned y)
{
	return x & ~(~(~0 << n) << (p+1-n)) |
		  (y &   ~(~0 << n)) << (p+1-n);
}

main()
{
	unsigned x = 0xf1f0;
	unsigned y = 0xfff8;
	int p = 3;
	int n = 4;
	printf("set %d bits of %x at position %d with bits of %x is %x\n", \
			n, x, p, y, setbits(x, p, n, y));
}
