#include<stdio.h>

/* count 1 bits in x - faster version */
int bitcount(unsigned x)
{
	int n = 0;
	while(x>0) {
		x &= (x-1);
		n++;
	}
	return n;
}

main()
{
	unsigned x = 0xff;
	printf("total %d 1 in %x\n", bitcount(x), x);
}
