
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
python Initializer.py -fp /home/path/to/Framework/Sandbox/CpuBenchPrimeFinder.c -fa "10000 --multithreaded --printdigits" -ca "-lgmp -lssl -lcrypto"
```
1.4 Changeable options  

```sh
In -fa "10000 --multithreaded --printdigits" any positive value can be given instead of 10000
```
### 2. SleepIterator
2.1 Category - LoopSchedular <br/>
2.2 Pre-Requirements - None <br />
2.3 Script
```sh
python Initializer.py -fp /home/path/to/Framework/Sandbox/SleepIterator.c -fa "400"
```
2.4 Changeable options  

```sh
In -fa "400" any positive value can be given instead of 400
