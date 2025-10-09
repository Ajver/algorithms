#!/bin/bash

liczba=$(( ( RANDOM % 100 )  + 1 ))

echo "Zgadnij liczbe z przedialu od 1-100!"
echo "random: $liczba"

for i in {1..7}; do
    proba=($i + 1)
    read -p "Proba $proba: " val
    
    if [[ $val == $liczba ]]; then
        echo "BRAWO!"
        exit
    else
        echo "jeszcze raz..."
    fi
done

echo "Niestety, wykorzystales wszystkie proby..."
