#include<stdio.h>

#define STR1 "hello, "
#define STR2 "world"

/* 拼接字符串常量（字面字符串）*/
main()
{
	char *s = STR1 STR2 "%d \n";
	printf(STR1 STR2 "\n");
	printf(s, 2);
}
