#!/bin/bash

for ((x = 60; x <= 960; x *= 2))
do  
    python3 tweet.py
    echo "exit code: $?"
    sleep $x
done