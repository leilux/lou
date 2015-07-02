#include<stdio.h>

/* invert: inverts the n bits of x that begin at position p */
unsigned invert(unsigned x, int p, int n)
{
	/* 0^0 0 1^0 1
	 * 0^1 1 1^1 0 invert
	 */
	return x ^ (~(~0 << n) << (p+1-n));
}

main()
{
	int p = 3;
	int n = 4;
	unsigned x = 0xfff7;
	printf("inverts the %d bits of %x that begin at position %d is %x\n", n, x, p, invert(x, p, n));
}
