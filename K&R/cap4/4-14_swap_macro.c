#include <stdio.h>

#define swap(t,x,y) {t x ## y;  \
	   			   	 x ## y = x; \
					 x = y; \
					 y = x ## y;}

main()
{
	int x = 1;
	int y = 0;
	printf(" x - y = %d\n", x - y);
	swap(int, x, y);
	printf(" x - y = %d\n", x - y);
}


