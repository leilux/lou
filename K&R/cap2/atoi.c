#include<stdio.h>

int atoi(char s[])
{
	int i, n, sign;
	for (i = 0; isspace(s[i]); i++)
		sign = (s[i]=='-') ? -1:1;
	if (s[i]=='+' || s[i]=='-')
		i++;
	n = 0;
	for (i = 0; s[i] >= '0' && s[i] <= '9'; ++i)
		n = 10 * n + (s[i] - '0');
	return n;
}

main()
{
}
