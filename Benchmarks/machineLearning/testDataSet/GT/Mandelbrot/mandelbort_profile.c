# include <stdlib.h>
# include <stdio.h>
# include <math.h>
# include <time.h>

#define size 500

//----> AdditionalCodeHook


int main ( void )

{
  int m = 500;
  int n = 500;

  int b[m][size];
  int c;
  int c_max;
  int count[m][size];
  int count_max = 20000;
  int g[m][size];
  int i;
  int ierror;
  int j;
  int jhi;
  int jlo;
  int k;
  char *output_filename = "mandelbrot.ppm";
  FILE *output_unit;
  int r[m][size];

  double x_max =   1.25;
  double x_min = - 2.25;
  double x;
  double x1;
  double x2;
  double y_max =   1.75;
  double y_min = - 1.75;
  double y;
  double y1;
  double y2;





  for ( int i = 0; i < m; i++ )
  {
    for ( int j = 0; j < n; j++ )
    {
    double  x = ( ( double ) (     j - 1 ) * x_max
          + ( double ) ( m - j     ) * x_min )
          / ( double ) ( m     - 1 );

    double  y = ( ( double ) (     i - 1 ) * y_max
          + ( double ) ( n - i     ) * y_min )
          / ( double ) ( n     - 1 );

      count[i][j] = 0;

    double  x1 = x;
    double  y1 = y;

      for ( int k = 1; k <= count_max; k++ )
      {
      double  x2 = x1 * x1 - y1 * y1 + x;
      double  y2 = 2 * x1 * y1 + y;

        if ( x2 < -2.0 || 2.0 < x2 || y2 < -2.0 || 2.0 < y2 )
        {
          count[i][j] = k;
          break;
        }
        x1 = x2;
        y1 = y2;
      }

      if ( ( count[i][j] % 2 ) == 1 )
      {
        r[i][j] = 255;
        g[i][j] = 255;
        b[i][j] = 255;
      }
      else
      {
        c = ( int ) ( 255.0 * sqrt ( sqrt ( sqrt (
          ( ( double ) ( count[i][j] ) / ( double ) ( count_max ) ) ) ) ) );
        r[i][j] = 3 * c / 5;
        g[i][j] = 3 * c / 5;
        b[i][j] = c;
      }
    }
  }




  return 0;
}
