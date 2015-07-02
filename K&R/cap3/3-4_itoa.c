#include <stdio.h>
#include <string.h>
#include <limits.h>

#define abs(x) ((x) < 0 ? -(x) : (x))

/* itoa: convert n to characters in s - modified */
void itoa(int n, char s[])
{
	int i, sign;
	void reverse(char s[]);

	sign = n;
	i = 0;
	do {
		s[i++] = abs(n % 10) + '0';
	} while ((n /= 10) != 0);
	if (sign < 0)
		s[i++] = '-';
	s[i] = '\0';
	reverse(s);
}

void reverse(char s[])
{
	int c, i, j;

	for (i = 0, j = strlen(s)-1; i < j; i++, j--) {
		c = s[i];
		s[i] = s[j];
		s[j] = c;
	}
}

main()
{
	int n = INT_MIN;
	char s[100];
	itoa(n, s);
	printf("%d to %s\n", n, s);
}
