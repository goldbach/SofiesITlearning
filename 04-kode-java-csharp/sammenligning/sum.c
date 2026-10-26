#include <stdio.h>
#include <time.h>

int main(void) {
    clock_t start = clock();
    long total = 0;
    for (long i = 0; i < 100000000; i++) {
        total += i % 7;
    }
    printf("%ld %.2f s\n", total, (double)(clock() - start) / CLOCKS_PER_SEC);
    return 0;
}
