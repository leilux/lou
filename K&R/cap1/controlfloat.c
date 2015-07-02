#include <stdio.h>
#include <stdlib.h>

int main(void)
{
	float f = 1.234567;
	char buf[100];
	while(scanf("%f", &f) == 1) {
		sprintf(buf, "%.3f", f);
		f = atof(buf);
		printf("%s\n", buf);
		printf("%f\n", f);
	
	}
	return 0;
}

