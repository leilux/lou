#include<stdio.h>

/* lower: convert c to lower case (ASCII only) */
int lower(int c)
{
	return (c >= 'A' && c <= 'Z') ? c + 'a' - 'A' : c;
}

main()
{
	char c = 'Q';
	printf("%c to lower case is %c\n", c, lower(c));
}
