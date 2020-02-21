#include <stdio.h>
#include <stdlib.h>
#include <time.h>


int
func(const int n, const char *s)
{
  int r;
  double d;
  srand(time(NULL));
  r = rand();
  printf("%d\n", r);
  d = (double)(r - RAND_MAX / 2) / (RAND_MAX / 2);
  printf("%f\n", d);
  return 0;
}


int
main(void)
{
  int i =10;
  func(i, "text");
  return 0;
}

