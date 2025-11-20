#!/bin/bash

n=1000
k=1200


for i in {1..20}; do
    for t in {1..4}; do
        ./psum $n $k $t
    done
done
