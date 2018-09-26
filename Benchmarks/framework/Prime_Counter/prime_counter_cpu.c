# include <stdlib.h>
# include <stdio.h>
# include <omp.h>

int main ( int argc, char *argv[] );
void prime_number_sweep (int n_hi );
int prime_number ( int n );


//----> AdditionalCodeHook



int main ( int argc, char *argv[] )

{

  int n_hi;

  n_hi = atoi( argv[1]);


  prime_number_sweep ( n_hi);

  return 0;
}


void prime_number_sweep (  int n_hi )

{
  int i;
  int n;
  int primes;
  double wtime;

  printf ( "         N        Pi          Time\n" );
  printf ( "\n" );


    primes = prime_number ( n_hi );

  return;
}


int prime_number ( int n )

{
  int i;
  int j;
  int prime;
  int total = 0;

# pragma omp parallel for shared ( n ) private ( i, j, prime ) schedule(static)
  for ( i = 2; i <= n; i++ )
  {
    prime = 1;

    for ( j = 2; j < i; j++ )
    {
      if ( i % j == 0 )
      {
        prime = 0;
        break;
      }
    }
    total = total + prime;
  }

  return total;
}
