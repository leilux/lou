#include<stdio.h>

/* binsearch find x in v[0] <= v[1] <= ... <= v[n-1] */
int binsearch(int x, int v[], int n)
{
	int low, high, mid;
	low = 0;
	high = n - 1;
	mid = (low+high) / 2;
	while (low <= high && x != v[mid]) {
		if (x < v[mid])
			high = mid - 1;
		else
			low = mid + 1;
		mid = (low+high) / 2;
	}
	if (x == v[mid])
		return mid;
	else
		return -1;
}

main()
{
	int x = 4;
	const int n = 6;
	int v[6] = {1,2,3,4,5,6};

	printf("find %d in v[] at %d\n", x, binsearch(x, v, n));
}
