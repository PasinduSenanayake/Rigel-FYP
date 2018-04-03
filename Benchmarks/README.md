
## Initialization

1. Benchmark and related files need to be copied into " ../../Sandbox " folder.
2. Install relevant Pre-Requirements for the benchmark
3. Execute the relevant script inside the "Framework" folder.

## Benchmarks

### 1. CpuBenchPrimeFinder
1.1 Category - LoopSchedular <br/>
1.2 Pre-Requirements - gmp.h, openssl/md5.h  [ Both Available Online ]<br />
1.3 Script
```sh
python Initializer.py -fp /home/path/to/Framework/Sandbox/CpuBenchPrimeFinder.c -fa "[numberscheckforprime] --multithreaded --printdigits" -ca "-lgmp -lssl -lcrypto"
```
1.4 Changeable options  

```sh
1. numberscheckforprime
```
### 2. SleepIterator
2.1 Category - LoopSchedular <br/>
2.2 Pre-Requirements - None <br />
2.3 Script
```sh
python Initializer.py -fp /home/path/to/Framework/Sandbox/SleepIterator.c -fa "[iterations]"

[iterations] - Integer (Any positive value)
```
2.4 Changeable options  

```sh
1. iterations
```
### 3. RandomSleep
3.1 Category - LoopSchedular <br/>
3.2 Pre-Requirements - Numgen.c <br />
3.3 Script
```sh
1. gcc -o numfile Numgen.c -lm && ./numfile [randomness] [iterations]
2. python Initializer.py -fp /home/path/to/Framework/Sandbox/SleepIterator.c -fa "[numberofthreads] [iterations]"

[randomness] - Integer (Any positive value)
[iterations] - Integer (In both places same value need to be given)
[numberofthreads] - Number of threads wil be used to execute this program
```
3.4 Changeable options  

```sh
1. randomness 2. iterations 3. numberofthreads
