#include <stdio.h>

#define NOTASPACE 'a'
#define SPACE     ' '

/* 编写一个将输入复制到输出的程序，并将其中连续的多个空格用一个空格代替。*/

main() 
{
	int c, pre;

	pre = NOTASPACE;

	while ((c = getchar()) != '\n') {
		if ((pre == SPACE) && (c == SPACE))
			;
		else putchar(c);

		pre = c;
	}
	printf("|\n");
}
