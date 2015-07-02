#include <stdio.h>
#include <string.h>

/* itob: convert n to characters in s - base b */
void itob(int n, char s[], int b)
{
	int i, j, sign;
	void reverse(char s[]);

	if ((sign = n) < 0)
		n = -n;
	i = 0;
	do {
		j = n % b;
		s[i++] = (j <= 9) ? j+'0' : j+'a'-10;
	} while ((n /= b) > 0);
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
	int n = 0xff88;
	char s[100];
	int b = 16;
	itob(n, s, b);
	printf("convert %x to characters in %s - base %d\n", n, s, b);
}
