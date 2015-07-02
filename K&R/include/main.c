#include <stdio.h>
#include "parseuri.h"

main()
{
	char *url = "www.url2io.com/articlen";
	char path[100];
	char cgi_args[100];

	parse_url(url, path, cgi_args);
	printf("url: %s\npath: %s\ncgi_args: %s\n", url, path, cgi_args);
}
