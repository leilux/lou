#include<stdio.h>


main ()
{
	/* NO,YES枚举名，loop枚举常量，okloop枚举变量 
	 * 会对okloop的值进行类型检查
	 * */
	enum loop { NO, YES };
	enum loop okloop = YES;
	
	int i = 0;
	char c;
	int lim = 100;
	char s[lim];

	while (okloop == YES) 
	{
		if (i >= lim - 2)
			okloop = NO;
		else if ((c = getchar()) == '\n')
			okloop = NO;
		else if (c == EOF)
			okloop = NO;
		else {
			s[i] = c;
			++i;
		}
	}
	s[i] = '\0';
	printf("out: %s\n", s);
	printf("last: %d\n", s[++i]);
}
