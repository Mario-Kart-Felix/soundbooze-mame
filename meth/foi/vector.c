#include <stdio.h>
#include <math.h>

#include <time.h>
#include <stdlib.h>

#include <omp.h>

// ts < 0.02 [400x200]
// gcc -Wall -O3 -fopenmp vector.c -o vector -lm

/* [packing, padding, barrier, sync]

def zeropad(A):

    Z = numpy.zeros(131072)
    P = []

    for a in A:
        P.append(a)

    for i in range(len(A), len(Z)):
            P.append(0)

    return P

A = numpy.array([1, 2, 3, 4, 5, 6, 7, 8])
P = zeropad(A)

*/

const unsigned int N = 131072;
typedef int v4si __attribute__ (( vector_size(131072 * sizeof(int)) ));

unsigned int
_sum(const unsigned int a[], const unsigned int N) 
{

  unsigned int ls = 0, s = 0; 

  #pragma omp parallel private(ls) shared(s) 
  { 
    ls = 0; 
    #pragma omp for schedule(static,1) 
    for (int i=0; i< N; i++) {
      ls += a[i]; 
    }
    #pragma omp critical 
    s += ls;
  } 

  return s;
}

unsigned int
sum_abs_diff(unsigned int z1[], unsigned int z2[])
{
  v4si va, vb, vsad;

  unsigned int i;
  unsigned int _abssub[N];

  #pragma omp parallel for
  for (i = 0; i < N; i++) {
    va[i] = z1[i];
    vb[i] = z2[i];
  }

  vsad = vb - va;

  #pragma omp parallel for
  for (i = 0; i < N; i++) {
    _abssub[i] = __builtin_abs(vsad[i]);
  }

  return _sum(_abssub, N);
}

float
rmse (unsigned int z1[], unsigned int z2[])
{
  v4si va, vb, vsub, vpow;

  unsigned int _pow[N];

  unsigned int sumpow;
  float meanpow;
  float sqrt;

  unsigned int i;

  #pragma omp parallel for
  for (i = 0; i < N; i++) {
    va[i] = z1[i];
    vb[i] = z2[i];
  }

  vsub = vb - va;
 
  #pragma omp parallel for
  for (i = 0; i < N; i++) {
    vpow[i] = __builtin_powi(vsub[i], 2);
  }

  #pragma omp parallel for
  for (i = 0; i < N; i++) {
    _pow[i] = vpow[i];
  }

  sumpow = _sum(_pow, N);
  meanpow = sumpow/N;

  sqrt = __builtin_sqrt(meanpow);

  return sqrt;
}

/*
float
ssim (unsigned int z1[], unsigned int z2[])
{
}
*/

int main()
{

  double t = 0.0;

  unsigned int z1[N];
  unsigned int z2[N];
   
  unsigned int i;

  srand((unsigned) time(NULL));

  for(i = 0 ; i < N ;i++) {
    z1[i] = rand() % 255;
    z2[i] = rand() % 255;
  }

	clock_t begin = clock();
  printf("%.5f\n", rmse(z1, z2));
  clock_t end = clock();

  t = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("%f s\n", t);

  begin = clock();
  printf("%d\n", sum_abs_diff(z1, z2));
  end = clock();

  t = (double)(end - begin) / CLOCKS_PER_SEC;
  printf("%f s\n", t);

  return 0;
}
