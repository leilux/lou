#include <string.h>

/* reverse: reverse string s in place */
void reverse(char s[])
{
	void reverser(char s[], int i, int len);

	reverser(s, 0, strlen(s));
}

/* reverse: reverse string s in place; recursive */
void reverser(char s[], int i, int len)
{
	int c, j;

	j = len - (i + 1);
	if (i < j) {
		c = s[i];
		s[i] = s[j];
		s[j] = c;
		reverser(s, ++i, len);
	}
}

main()
{
	char s[] = "hello";
	
	printf("%s reverse to ", s);
	reverse(s);
	printf("%s\n", s);
}
