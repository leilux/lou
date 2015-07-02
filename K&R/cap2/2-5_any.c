#include<stdio.h>

/* any: return first location in s1 where any char from s2 occurs */
int any(char s1[], char s2[])
{
	int i, j;

	for (i=0; s1[i] != '\0'; i++)
		for (j=0; s2[j] != '\0'; j++)
			if (s1[i] == s2[j])
				return i;
	return -1;
}

char * my_strpbrk(const char *s1 ,const char *s2)
{
   const char *c = s2;
   if (!*s1)
      return (char *) NULL;

   while (*s1) {
      for (c = s2; *c; c++)
        if (*s1 == *c)
           break;

      if (*c)
        break;

      s1++;
   }

   if (*c == '/0')
      s1 = NULL;

   return (char *) s1;
}

main()
{
	char *s1 = "hello world";
	char *s2 = "ol";
	printf("%s in %s %d\n", s2, s1, any(s1, s2));
}
