#include <stdio.h>
#include <math.h>

/* itoa: convert n tp characters in s; recursive */
void itoa(int n, char s[])
{
	static int i;

	if (n / 10)
		itoa(n/10, s);
	else {
		i = 0;
		if (n < 0)
			s[i++] = '-';
	}
	s[i++] = abs(n) % 10 + '0';
	s[i] = '\0';
}

main()
{
	int n = 12345;
	char s[100];
	itoa(n, s);
	printf("convert %d to %s\n", n, s);
}
