#include <stdio.h>

/* expand: expand shortand notation in s1 into string s2 */
void expand(char s1[], char s2[])
{
	char c;
	int i, j;

	i = j = 0;
	while ((c = s1[i++]) != '\0')
		if (s1[i] == '-' && s1[i+1] >= c) {
			i++;
			while (c < s1[i])
				s2[j++] = c++;
		} else
			s2[j++] = c;
	s2[j] = '\0';
}

main()
{
	char s1[] = "-0-9\na-z\na-b-d\n0-9\n";
	char s2[100];

	expand(s1, s2);
	printf("expand %s <=to=>\n %s", s1, s2);
}
