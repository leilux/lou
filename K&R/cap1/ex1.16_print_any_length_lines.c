#include <stdio.h>

/* 修改打印最长文本行的程序的主程序main，使之可以打印任意长度的输入行的长度，并尽可能多地打印文本。 */

#define MAXLINE 1000

int getline4me(char line[], int maxline);
void copy(char to[], char from[]);

/* print the longest line */
int main(void)
{
	int len;
	int max;
	char line[MAXLINE];
	char longest[MAXLINE];

	max = 0;
	while ((len = getline4me(line, MAXLINE)) > 0)
		if (len > max) {
			max = len;
			copy(longest, line);
		}
	if (max > 0)
        printf("longest is %d str: %s\n", max, longest);
	return 0;
}

/* funciton getline: read line to s and return it's len */
int getline4me(char s[], int lim)
{
	int c,i, j;

	for (i=0, j=0; (c=getchar())!=EOF && c!='\n'; ++i) {
        if (i < lim -1)
            s[j++] = c;
    }
	if (c == '\n') {
        if (i <= lim - 1)
            s[j++] = c;
        ++i;
    }
	s[j] = '\0';
	return i;
}
/* function copy: copy from to to; assum to long enough */
void copy(char to[], char from[])
{
	int i;
	i = 0;
	while ((to[i] = from[i]) != '\0')
		++i;
}
