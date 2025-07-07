#!/bin/bash
lcov --capture --directory . --output-file ../output/coverage/coverage.info
genhtml ../output/coverage/coverage.info --output-directory ../output/coverage/html
