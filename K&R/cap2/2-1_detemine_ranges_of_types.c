#include<stdio.h>
#include<limits.h>

/* determine ranges of types */
void detemine_from_limits()
{
	/* sigined types */
	printf("signed char min = %d\n", SCHAR_MIN);
	printf("signed char max = %d\n", SCHAR_MAX);
	printf("signed short min = %d\n", SHRT_MIN);
	printf("signed short max = %d\n", SHRT_MAX);
	printf("signed int min = %d\n", INT_MIN);
	printf("signed int max = %d\n", INT_MAX);
	printf("signed long min = %d\n", LONG_MIN);
	printf("signed long max = %d\n", LONG_MAX);
	/* unsigned types */
	printf("unsigned char max = %u\n", UCHAR_MAX);
	printf("unsigned short max = %u\n", USHRT_MAX);
	printf("unsigned int max = %u\n", UINT_MAX);
	printf("unsigned long max = %u\n", ULONG_MAX);
}

void detemine_by_calculate()
{
	/* signed types */
	printf("signed char min = %d\n", -(char)((unsigned char) ~ 0 >> 1));
	printf("signed char max = %d\n", (char)((unsigned char) ~ 0 >> 1));
	printf("signed short min = %d\n", -(short)((unsigned short) ~ 0 >> 1));
	printf("signed short max = %d\n", (short)((unsigned short) ~ 0 >> 1));
	printf("signed int min = %d\n", -(int)((unsigned int) ~0 >> 1));
	printf("signed int max = %d\n", (int)((unsigned int) ~0 >> 1));
	printf("signed long min = %d\n", -(long)((unsigned long) ~0 >> 1));
	printf("signed long max = %d\n", (long)((unsigned long) ~0 >> 1));

	/* unsigned types */
	printf("unsigned char max = %u\n", (unsigned char) ~0);
	printf("unsigned short max = %u\n", (unsigned short) ~0);
	printf("unsigned int max = %u\n", (unsigned int) ~0);
	printf("unsigned long max = %u\n", (unsigned long) ~0);
}

main()
{
	printf("detemine_from_limits\n");
	detemine_from_limits();

	printf("detemine_by_calculate\n");
	detemine_by_calculate();
}