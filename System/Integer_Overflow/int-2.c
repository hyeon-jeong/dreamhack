// int-2.c
char *create_tbl(unsigned int width, unsigned int height, char *row) {
	unsigned int n;
	int i;
	char *buf;
	n = width * height;
	buf = (char *)malloc(n);
	
	if(!buf)
		return NULL;
	for(i = 0; i < height; i++)
		memcpy(&buf[i * width], row, width);
	return buf;
}

