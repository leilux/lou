#include <stdio.h>
#define MAXLINE 1000
/*编写函数reverse(s), 将字符串s中的字符顺序颠倒。使用该函数编写一个程序，每次颠倒一个输入行中的字符顺序。*/
void reverse(char s[])
{
	int i, len;
	for (len=0; s[len] != '\0'; ++len) 
		;
	char temp[len];
	for (i=0; i<len; i++)
		temp[len-1-i] = s[i];
	for (i=0; i<len; i++)
		s[i] = temp[i];
}
int getline4me(char s[], int lim)
{
	int c,i;

	for (i=0; i<lim-1 && (c=getchar())!=EOF && c!='\n'; ++i)
		s[i] = c;
	if (c == '\n') {
		s[i] = c;
		++i;
	}
	s[i] = '\0';
	return i;
}
int main()
{
	int i, len;
	char line[MAXLINE];
	len = getline4me(line, MAXLINE);
	reverse(line);
	for (i=0; i<len; i++)
		putchar(line[i]);
	printf("|\n");
	return 0;
}

