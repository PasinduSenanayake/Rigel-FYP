/*
 * Copyright 1993-2015 NVIDIA Corporation.  All rights reserved.
 *
 * Please refer to the NVIDIA end user license agreement (EULA) associated
 * with this source code for terms and conditions that govern your use of
 * this software. Any use, reproduction, disclosure, or distribution of
 * this software and related documentation outside the terms of the EULA
 * is strictly prohibited.
 *
 */
/* This sample queries the properties of the CUDA devices present in the system via CUDA Runtime API. */

// Shared Utilities (QA Testing)

// std::system includes
#include <memory>
#include <iostream>

#include <cuda_runtime.h>
#include "helper_cuda.h"



int *pArgc = NULL;
char **pArgv = NULL;

#if CUDART_VERSION < 5000

// CUDA-C includes
#include <cuda.h>

// This function wraps the CUDA Driver API into a template function
template <class T>
inline void getCudaAttribute(T *attribute, CUdevice_attribute device_attribute, int device)
{
    CUresult error =    cuDeviceGetAttribute(attribute, device_attribute, device);

    if (CUDA_SUCCESS != error)
    {
        fprintf(stderr, "cuSafeCallNoSync() Driver API error = %04d from file <%s>, line %i.\n",
                error, __FILE__, __LINE__);

        exit(EXIT_FAILURE);
    }
}

#endif /* CUDART_VERSION < 5000 */

////////////////////////////////////////////////////////////////////////////////
// Program main
////////////////////////////////////////////////////////////////////////////////
int
main(int argc, char **argv)
{
    pArgc = &argc;
    pArgv = argv;
    int deviceCount = 0;
    cudaError_t error_id = cudaGetDeviceCount(&deviceCount);

    if (error_id != cudaSuccess)
    {
        printf("cudaGetDeviceCount returned %d\n-> %s\n", (int)error_id, cudaGetErrorString(error_id));
        printf("Result = FAIL\n");
        exit(EXIT_FAILURE);
    }

    printf("Detected devices =%d \n", deviceCount);


    int dev, driverVersion = 0, runtimeVersion = 0;

    for (dev = 0; dev < deviceCount; ++dev)
    {
        cudaSetDevice(dev);
        cudaDeviceProp deviceProp;
        cudaGetDeviceProperties(&deviceProp, dev);

        printf("\nDevice_%d:%s\n", dev, deviceProp.name);

        // Console log
        cudaDriverGetVersion(&driverVersion);
        cudaRuntimeGetVersion(&runtimeVersion);
        printf("  CUDA Driver Version / Runtime Version          %d.%d / %d.%d\n", driverVersion/1000, (driverVersion%100)/10, runtimeVersion/1000, (runtimeVersion%100)/10);
        printf("  CUDA Capability Major/Minor version number:    %d.%d\n", deviceProp.major, deviceProp.minor);

        char msg[256];
        SPRINTF(msg, "  Total amount of global memory:                 %.0f MBytes (%llu bytes)\n",
                (float)deviceProp.totalGlobalMem/1048576.0f, (unsigned long long) deviceProp.totalGlobalMem);
        printf("%s", msg);
        printf("  Multiprocessors:                              %2d\n",deviceProp.multiProcessorCount);
        printf("  CUDA Cores/MP:                                 %3d \n",_ConvertSMVer2Cores(deviceProp.major, deviceProp.minor));
        //printf("  GPU Max Clock rate:                            %.0f MHz (%0.2f GHz)\n", deviceProp.clockRate * 1e-3f, deviceProp.clockRate * 1e-6f);


#if CUDART_VERSION >= 5000

        if (deviceProp.l2CacheSize)
        {
           printf("  L2 Cache Size:                                 %d bytes\n", deviceProp.l2CacheSize);
        }

#else
        // This only available in CUDA 4.0-4.2 (but these were only exposed in the CUDA Driver API)
        int memoryClock;
        getCudaAttribute<int>(&memoryClock, CU_DEVICE_ATTRIBUTE_MEMORY_CLOCK_RATE, dev);
        //printf("  Memory Clock rate:                             %.0f Mhz\n", memoryClock * 1e-3f);
        int memBusWidth;
        getCudaAttribute<int>(&memBusWidth, CU_DEVICE_ATTRIBUTE_GLOBAL_MEMORY_BUS_WIDTH, dev);
        //printf("  Memory Bus Width:                              %d-bit\n", memBusWidth);
        int L2CacheSize;
        getCudaAttribute<int>(&L2CacheSize, CU_DEVICE_ATTRIBUTE_L2_CACHE_SIZE, dev);

        if (L2CacheSize)
        {
            printf("  L2 Cache Size:                                 %d bytes\n", L2CacheSize);
        }

#endif

        printf("  Total amount of constant memory:               %lu bytes\n", deviceProp.totalConstMem);
        printf("  Total amount of shared memory per block:       %lu bytes\n", deviceProp.sharedMemPerBlock);
        printf("  Total number of registers available per block: %d\n", deviceProp.regsPerBlock);
        printf("  Warp size:                                     %d\n", deviceProp.warpSize);
        printf("  Maximum number of threads per multiprocessor:  %d\n", deviceProp.maxThreadsPerMultiProcessor);
        printf("  Maximum number of threads per block:           %d\n", deviceProp.maxThreadsPerBlock);

    }

    if (deviceCount >= 2)
    {
        cudaDeviceProp prop[64];
        int gpuid[64];
        int gpu_p2p_count = 0;

        for (int i=0; i < deviceCount; i++)
        {
            checkCudaErrors(cudaGetDeviceProperties(&prop[i], i));

            // Only boards based on Fermi or later can support P2P
            if ((prop[i].major >= 2)
#if defined(WIN32) || defined(_WIN32) || defined(WIN64) || defined(_WIN64)
                // on Windows (64-bit), the Tesla Compute Cluster driver for windows must be enabled to support this
                && prop[i].tccDriver
#endif
               )
            {
                // This is an array of P2P capable GPUs
                gpuid[gpu_p2p_count++] = i;
            }
        }

        // Show all the combinations of support P2P GPUs
        int can_access_peer;

        if (gpu_p2p_count >= 2)
        {
            for (int i = 0; i < gpu_p2p_count; i++)
            {
                for (int j = 0; j < gpu_p2p_count; j++)
                {
                    if (gpuid[i] == gpuid[j])
                    {
                        continue;
                    }
                    checkCudaErrors(cudaDeviceCanAccessPeer(&can_access_peer, gpuid[i], gpuid[j]));
                        printf("> Peer access from %s (GPU%d) -> %s (GPU%d) : %s\n", prop[gpuid[i]].name, gpuid[i],
                           prop[gpuid[j]].name, gpuid[j] ,
                           can_access_peer ? "Yes" : "No");
                }
            }
        }
    }
    exit(EXIT_SUCCESS);
}
