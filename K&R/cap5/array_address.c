#include <stdio.h>
#include <string.h>

#define SIZE 4

main()
{
	char ca[] = "hello";
	char *str = "hello";
	int ia[SIZE];
	int i;
	char *p;
	p = &ca[0];

	for (i = 0; i < strlen(ca); i++)
		printf("char a[%d] addr %u\n", i, (int)&ca[i]);
	printf("ca + 1 = %u + 1 = %u\n", (unsigned)&ca[--i], (unsigned)(&ca[i] + 1));

	for (i = 0; i < SIZE; i++)
		printf("int a[%d] addr %u\n", i, (int)&ia[i]);
	/* int型指针加1： 地址加4 */
	printf("ia + 1 = %u + 1 = %u\n", (unsigned)&ia[--i], (unsigned)(&ia[i] + 1));

	char *cp;
	int *ip;
	float *fp;
	void *vp;
	printf("sizeof char * is %u\n", sizeof cp);
	printf("sizeof int * is %u\n", sizeof ip);
	printf("sizeof float * is %u\n", sizeof fp);
	printf("sizeof void * is %u\n", sizeof vp);
	printf("sizeof char ca[] = \"%s\" is %u\n", ca, sizeof ca);
	printf("sizeof int ia[%d] is %u\n", SIZE, sizeof ia);

	printf("ca[]: %s\n", ca);
	printf("%c, %c\n", p[0], p[1]);

	printf("[begin] ca[] %s\n", ca);
	test_array_name(ca);
	printf("[end] ca[] %s\n", ca);

	str++;
	printf("[begin] str %s\n", str);
	test_array_name(str);
	printf("[end] str %s\n", str);

}

void test_array_name(char *s)
{
	s++;
	printf("[in] ca[] %s\n", s);
}
