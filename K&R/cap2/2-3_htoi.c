#include<stdio.h>

#define YES 1
#define NO  0

/* htoi: convert hexadecimal string s to integer 0x可选*/
int htoi(char s[]);

main() 
{
	printf("hex 0x11 is %d\n", htoi("0x11"));
	printf("hex 11 is %d\n", htoi("11"));
}


int htoi(char s[]) 
{
	int hexdigit, i, inhex, n;

	i = 0;
	if (s[i] == '0') {
		++i;
		if (s[i] == 'x' || s[i] == 'X')
			++i;
	}
	n = 0; 				/* integer value to be returned */
	inhex = YES; 		/* assume valid hexadecimal digit */
	for ( ; inhex == YES; ++i) {
		if (s[i] >= '0' && s[i] <= '9')
			hexdigit = s[i] - '0';
		else if (s[i] >= 'a' && s[i] <= 'f')
			hexdigit = s[i] - 'a' + 10;
		else if (s[i] >= 'A' && s[i] <= 'F')
			hexdigit = s[i] - 'A' + 10;
		else
			inhex = NO; 	/* not a valid hexadecimal digit */
		if (inhex == YES)
			n = 16 * n + hexdigit;

	}
	return n;
}

