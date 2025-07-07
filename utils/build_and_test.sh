#!/bin/bash
mkdir -p build
cd build
cmake ..
make
ctest --output-on-failure | tee ../output/logs/test_results.log