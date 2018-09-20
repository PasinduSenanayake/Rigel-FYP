#ifdef _POMP
#  undef _POMP
#endif
#define _POMP 200110

#include "dummy.c.opari.inc"
#line 1 "dummy.c"
#define LEN 30000
#define LEN2 500

int dummy(float a[LEN], float b[LEN], float c[LEN], float d[LEN], float e[LEN], float aa[LEN2][LEN2], float bb[LEN2][LEN2], float cc[LEN2][LEN2], float s){
	// --  called in each loop to make all computations appear required
	return 0;
}

