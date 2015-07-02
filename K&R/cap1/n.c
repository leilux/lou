// /*1.2*/ 
// #include <stdio.h>
//   /* 当fahr=0,20,...,300时，分别打印华式温度与摄氏温度对照表*/
//   main()
//   { 
//   	int fahr, celsius;
//   	int lower, upper, step;
//   
//   	lower = 0;    /* 温度表的下限 */
//   	upper = 300;  /* 温度表的上限 */
//   	step = 20;    /* 步长 */
//   
//   	fahr = lower;
//   	while (fahr <= upper) {
//   		celsius = 5 * (fahr-32) / 9;
//   		printf("%d\t%d\n", fahr, celsius);
//   		fahr = fahr + step;
//   	}
//   }
// 
// /*1.3*/
// #include <stdio.h>
// /* print fathr - celsius */
// main()
// {
// 	int fahr;
// 
// 	for (fahr = 0; fahr <= 300; fahr = fahr + 20)
// 		printf("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
// }
// 
// /*1.4*/
// #include <stdio.h>
// 
// #define LOWER 0
// #define UPPER 300
// #define STEP  20
// main()
// {
// 	int fahr;
// 	for (fahr = LOWER; fahr <= UPPER; fahr = fahr + STEP)
// 		printf("%3d %6.1f\n", fahr, (5.0/9.0)*(fahr-32));
// }

/*1.5.1*/
// #include <stdio.h>
// 
// main()
// {
// 	int c;
// 	printf("%d", EOF);
// 	while ((c = getchar()) != EOF) {
// 			putchar(c);
// 			printf("c is %d\n", c);
// 	}
// }

/*1.5.2*/
// #include <stdio.h>
// /* v1 */
// main()
// {
// 	long nc;
// 	nc = 0;
// 	while (getchar() != EOF)
// 			++nc;
// 	printf("%ld\n", nc);
// }

// #include <stdio.h>
// /* v2 */
// main()
// {
// 	double nc;
// 	for (nc = 0; getchar() != '\n'; ++nc)
// 		;
// 	printf("%.0f\n", nc);
// }

/*1.5.3*/
// 	#include <stdio.h>
// 	main()
// 	{
// 		intc, nl;
// 		nl = 0;
// 		while ((c = getchar()) != EOF)
// 			if (c == '\n') ++nl;
// 		printf("%d\n", nl);
// 	}

/*1.5.4*/
// #include <stdio.h>
// 
// #define IN  1 /* in word */
// #define OUT 0 /* out word */
// 
// main()
// {
// 	int c, nl, nw, nc, state;
// 
// 	state = OUT;
// 	nl = nw = nc = 0;
// 	while ((c = getchar()) != '\n') {
// 		++nc;
// 		if (c == '\n')
// 			++nl;
// 		if (c == ' ' || c == '\n' || c == '\t')
// 			state = OUT;
// 		else if (state == OUT) {
// 			state = IN;
// 			++nw;
// 		}
// 	}
// 	printf("%d %d %d\n", nl, nw, nc);
// }

/*1.6*/
// #include <stdio.h>
// 
// main()
// {
// 	int c, i, nwhite, nother;
// 	int ndigit[10];
// 
// 	nwhite = nother = 0;
// 	for (i = 0; i < 10; ++i)
// 		ndigit[i] = 0;
// 
// 	while ((c = getchar()) != '\n')
// 		if (c >= '0' && c <='9')
// 			++ndigit[c-'0'];
// 		else if (c == ' ' || c == '\n' || c == '\t')
// 			++nwhite;
// 		else ++nother;
// 	printf("digits = ");
// 	for (i = 0; i < 10; ++i)
// 		printf(" %d", ndigit[i]);
// 	printf(", white space = %d, other = %d\n",
// 			nwhite, nother);
// }

/*1.9*/
#include <stdio.h>
#define MAXLINE 1000

int getline4me(char line[], int maxline);
void copy(char to[], char from[]);

/* print the longest line */
main()
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
		printf("%s", longest);
	return 0;
}

/* funciton getline: read str to s and return it's len */
int getline4me(char s[], int lim)
{
	int c,i;

	for (i=0; i<lim-1 && (c=getchar())!=EOF && c!='\n'; ++i)
		s[i] = c;
	if (c == '\n') {
		s[i] = c;
		++i;
	}
	s[i] = '\0';
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
