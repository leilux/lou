#include<stdio.h>

/* escape: expand newline and tab into visible sequences */
/* 		   while copying the string t to s */
void escape(char s[], char t[])
{
	int i, j;

	for (i=j=0; t[i] != '\0'; i++)
		switch (t[i]) {
		case '\n':
			s[j++] = '\\';
			s[j++] = 'n';
			break;
		case '\t':
			s[j++] = '\\';
			s[j++] = 't';
			break;
		default:
			s[j++] = t[i];
			break;
		}
	s[j] = '\0';
}

/* unescape: convert escape sequences into real characters */
/* 			 while copying the string t to s */
void unescape(char s[], char t[])
{
	int i, j;

	for (i=j=0; t[i] != '\0'; i++)
		if (t[i] != '\\')
			s[j++] = t[i];
		else 
			switch(t[++i]) {
			case 'n':
				s[j++] = '\n';
				break;
			case 't':
				s[j++] = '\t';
				break;
			default:
				s[j++] = '\\'; // 有bug
				s[j++] = t[i];
				break;
			}
	s[j] = '\0';
}

main()
{
	char t[] = "ab 	";
	char s[100];
	char t1[] = "ab\\t\\\\t";
	char s1[100];
	escape(s, t);
	printf("escape '%s' to '%s'\n", t, s);
	unescape(s1, t1);
	printf("unescape '%s' to '%s'\n", t1, s1);
}
