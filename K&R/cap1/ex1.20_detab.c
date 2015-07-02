/* 
 * 编写程序detab，将输入中的制表符替换成适当数目的空格，使空格充满到下一个制表符终止位的地方。
 * 假设制表符终止位的位置是固定的，比如每隔n列就会出现一个制表符终止位。n应该作为变量还是符号常量呢？ 
 * when line's length > MAXLINE it not work correct.
*/
#include <stdio.h>

#define SPACE4TABSTOPS 8
#define MAXLINE 1000
#define SPACE ' '
#define TAB	  '\t'

int getline4me(char line[], int maxline);
int getSpace4Tabstops(int offset, int tabsize);
void detab(char line[], int len);

int main(void)
{
	int len;
	char line[MAXLINE];
	while ((len = getline4me(line, MAXLINE)) > 0) {
		detab(line, len);
	}
	return 0;
}

/* funciton getline: read line to s and return it's len */
int getline4me(char s[], int lim)
{
	int c, i;

	/* tip-1 : because of the getchar(), it can be right answer when the i 
	 * over MAXLINE.
	 */
	for (i = 0; (i < lim - 1) && (c = getchar()) != EOF && c != '\n'; ++i)
	{
		s[i] = c;
	}
	if (c == '\n') {
		s[i] = c;
		i++;
	}
	s[i] = '\0';
	return i;
}

int getSpace4Tabstops(int offset, int tabsize)
{
	return tabsize - (offset % tabsize);
}

void detab(char line[], int len)
{
//	printf("\nrun detab\n");
	int i, j;
	int nspace, position;

	for (i=0, position=1; i<=len; i++) {
		if (line[i] == TAB) {
			nspace = getSpace4Tabstops(position-1, SPACE4TABSTOPS);
			position = 1;
			// print char
			for(j=0; j<nspace; j++) putchar(SPACE);
		}
		else {
			position++;
			// print char
			putchar(line[i]);
		}
	}
}
