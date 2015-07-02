#include <stdio.h>
#define MAXLINE 1000
/*删除每一个输入行末尾的空格及制表符，并删除完全是空格的行。*/
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
int rstrip(char line[]) 
{
	int i, len;
	len = getline4me(line, MAXLINE);
	i = len - 1;
	if (len >= MAXLINE) return MAXLINE;
	else {
		while (( line[i-1] == ' ' || line[i-1] == '\t') && (i >= 1)) {
			i--;
		}
	}
	return i;
}

int main() 
{
	int i, len;
	char line[MAXLINE];
	len = rstrip(line);
	// print the str after rstrip
	for (i=0; i<len; i++) 
		putchar(line[i]);
	printf("|\n");
	return 0;
}
