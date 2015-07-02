#include <stdio.h>

#define SPACE   ' '
#define TAB     '\t'
#define ENTER   '\n'

/* 1-8 编写一个统计空格、制表符与换行符个数的程序。*/

main()
{
	int c;
	int sc, tc, ec;
 	sc = 0;           
	tc = 0;
 	ec = 0;

	while ((c = getchar()) != '\n') {
		if (c == SPACE) ++sc;
		else if (c == TAB) ++tc;
		else if (c == ENTER) ++ec;
	}
	printf("Space : %d\n", sc);
	printf("Tab : %d\n", tc);
	printf("Enter : %d\n", ec);
}

