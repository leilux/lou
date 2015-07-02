#ifndef parse_uri
#define parse_uri

void get_url_from_request(char *request_line, char *url);
void parse_url(char *uri, char *path, char *cgiargs);

#endif
