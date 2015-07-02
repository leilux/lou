#include <stdio.h>


int foo(int x)
{
	printf("%d\n", x);
	return 1;
}

main()
{
	int foo(int);
	int (*fp)(int);
	fp = foo;
	fp(3);
	(*fp)(3);
}
