#!/bin/bash

n=3000
k=50000


for i in {1..5}; do
    for t in {1..10}; do
        ./psum $n $k $t
    done
done
