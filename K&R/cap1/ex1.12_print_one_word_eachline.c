#include <stdio.h>

#define IN  1
#define OUT 0

/* 编写一个程序，以每行一个单词的形式打印其输入。*/
main() 
{
	int c, state;
	state = OUT;

	while ((c = getchar()) != '\n') {
		if (c == ' ' || c == '\n' || c == '\t') {
			// end of word print '\n'
			if(state == IN) putchar('\n');
			state = OUT;
		}
		else {
			putchar(c);
			state = IN;
		}
	}
	printf("|\n");
}
