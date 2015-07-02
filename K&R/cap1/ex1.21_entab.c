/*
 * 编写程序entab，将空格串换为最少数量的制表符和空格，
 * 但要保持单词之间的间隔不变。
 * 假设制表符终止位的位置与练习1-20的detab程序的情况相同。
 * 当使用一个制表符或者一个空格都可以到达下一个制表符终止位时，
 * 选用哪一种替换字符比较好？
 * */ 
#include <stdio.h>
#define SPACE2TAB 8
#define MAXLINE   1000

int getline4me(char line[], int lim);
void entab(char line[], int len);

int main(void)
{
	int i, len;
	char line[MAXLINE];
	while ((len = getline4me(line, MAXLINE)) > 0) {
		entab(line, len);
		printf("%s\n", line);
//		for (i=0; line[i] != '\0'; i++) {
//			if (line[i] == '\t') printf("\\t");
//			else putchar(line[i]);
//		}
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

void entab(char line[], int len)
{
	int i, j, position, now, nspace;
	char buffer[SPACE2TAB];
	char stop;

	nspace = 0;
	position = 1;
	now = 0;

	for (i=0; i < len; i++) {
		if (line[i] == '\t' || position == SPACE2TAB) {
			if (position == SPACE2TAB && line[i] != ' ' && line[i] != '\t') {
				stop = line[i];
				nspace = 0;
			}
			else 
				stop = '\t';
			for (j=0; j < position - 1 - nspace; now++, j++)
				line[now] = buffer[j];
			line[now++] = stop;
			nspace = 0;
			position = 1;
		}
		else {
			nspace = line[i] == ' '? nspace++ : 0;
			buffer[position-1] = line[i];
			position++;
		}
	}
	// the end of string
	for (j=0; j < position - 1; now++, j++)
		line[now] = buffer[j];
	line[now] = '\0';
}
