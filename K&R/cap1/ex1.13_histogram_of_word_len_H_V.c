#include <stdio.h>
/* 编写一个程序，打印输入中单词长度的直方图。水平方向的直方图比较容易，垂直方向的直方图则要困难些。*/
#define IN  1
#define OUT 0

void hHistogram(int hight[], int len) 
{
	int i, j;
	for (i = 0; i< len; i++) {
		printf("%x", i);	//print the tag
		for (j = 0; j<hight[i]; j++) printf("||");
		printf("\n");
	}
}

void vHistogram(int hight[], int len) 
{
	int i, max;
	max = 0;
	// get max
	for (i = 0; i<len; i++) 
		if (max < hight[i]) max = hight[i];
	printf("max : %d\n",max);
	// print the histogram
	for ( ;max >= 1; max--) {
		for (i = 0; i<len; i++) {
			if (hight[i] > max) printf(" ___");
			else if (hight[i] == max) printf(" ___");
			else printf("    ");
		}
		printf("\n");
	}
	// print the tag
	for (i = 0; i<len; i++) 
		printf("  %x ",i);

	printf("\n");
}

main() 
{
	// assum word length < 16
	int hight[16] = {0};
	int c, i, state;
	i = 0;
	state = OUT;

	while ((c = getchar()) != '\n') {
		if (c == ' ' || c == '\n' || c == '\t') {
			++hight[i];
			i = 0;
			state = OUT;
		}
		else {
			i++;
			state = IN;
		}
	}

	int len;
	len = sizeof(hight) / sizeof(hight[0]);

	// print histogram
	hHistogram(hight, len);
	vHistogram(hight, len);
}
/* Testing word
 ASCII stands for American Standard Code for Information Interchange. Computers can only understand numbers, so an ASCII code is the numerical representation of a character such as 'a' or '@' or an action of some sort. ASCII was developed a long time ago and now the non-printing characters are rarely used for their original purpose. Below is the ASCII character table and this includes descriptions of the first 32 non-printing characters. ASCII was actually designed for use with teletypes and so the descriptions are somewhat obscure. If someone says they want your CV however in ASCII format, all this means is they want 'plain' text with no formatting such as tabs, bold or underscoring - the raw format that any computer can understand. This is usually so they can easily import the file into their own applications without issues. Notepad.exe creates ASCII text, or in MS Word you can save a file as 'text only'
 */
