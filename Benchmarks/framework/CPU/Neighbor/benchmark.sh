#!/bin/sh
#
# Author: Soeren Gebbert
# License: GPL >=2

#
# requires gcc 4.7+
# 
# See also: http://wiki.gentoo.org/wiki/Safe_CFLAGS

gcc -Wall -fopenmp -lgomp -Ofast neighbor_bench.c -o neighbor

echo "openMP tests 1/2/4 threads...:"

export OMP_NUM_THREADS=1
time -p ./neighbor 5000 5000 23
export OMP_NUM_THREADS=2
time -p ./neighbor 5000 5000 23
export OMP_NUM_THREADS=4
time -p ./neighbor 5000 5000 23

echo "------------------------------"
echo "openMP tests 1/2/4 threads with AVX-i...:"

# requires recent processors, see
# http://en.wikipedia.org/wiki/Advanced_Vector_Extensions

# keep precision: -fno-fast-math
gcc -Wall -fopenmp -lgomp -Ofast -march=core-avx-i neighbor_bench.c -o neighbor

export OMP_NUM_THREADS=1
time -p ./neighbor 5000 5000 23
export OMP_NUM_THREADS=2
time -p ./neighbor 5000 5000 23
export OMP_NUM_THREADS=4
time -p ./neighbor 5000 5000 23

