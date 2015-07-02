/* strcat: concatentate t to the end of s; pointer version */
void strcat(char *s, char *t)
{
	while(*s)
		s++;
	while (*s++ = *t++)
		;
}

/* strend: return 1 if string t occurs at the end of s strend("","") ==> 0 */
int strend(s, t)
{
	char *bs = s;
	char *bt = t;

	for ( ; *s; s++)
		;
	for ( ; *t; t++)
		;
	for ( ; *s == *t; s--, t--)
		if (t == bt || s == bs)
			break;
	if (*s == *t && t == bt && *s != '\0')
		return 1;
	else
		return 0;
}

/* strncpy: copy n characters from t to s */
void strncpy(char *s, char *t, int n)
{
	while (*t && n-- > 0)
		*s++ = *t++;
	while (n-- > 0)
		*s++ = '\0';
}

/* strncat: concatenate n characters of t to the end of s */
void strncat(char *s, char *t, int n)
{
	void strncpy(char *s, char *t, int n);
	int strlen(char *);

	strncpy(s+strlen(s), t, n);
}

/* strncmp: compare at most n characters of t with s */
int strncmp(char *s, char *t, int n)
{
	for ( ; *s == *t; s++, t++)
		if (*s == '\0' || --n <= 0)
			return 0;
	return *s - *t;
}

main()
{
}
