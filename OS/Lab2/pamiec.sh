#!/bin/bash

echo "Za chwile wyswietle 5 liter. Twoim zadaniem jest zapamietac je i wpisac w KOLEJNOSCI ALFABETYCZNEJ!"
read -n 1 -p "Kliknij dowolny klawisz aby kontynuowac..."
echo ""

points=0

alphabetical_order() {
    s="$1"

    spaceless=$(echo "$s" | tr -d " ")

    sorted=$(echo "$spaceless" | fold -w1 | sort | tr -d "\n")
    
    if [ "$spaceless" = "$sorted" ]; then
        return 0  # TO JEST PRAWDAAAAA! AaaaA :C
    else
        return 1
    fi
}


for i in {1..2}; do
    clear
    
    letters=$(echo {A..Z} | tr ' ' '\n' | shuf | head -n 5)
    echo $letters;
    sleep 3
    
    clear

    echo "Wpisz litery w kolejnosci alfabetycznej:"
    read val

    val="${val^^}"

    echo "Wpisanee: $val"

    if alphabetical_order "$val"; then
        echo "jest alfabetycznie"
        points=$[points + 1]
    else
        echo "niealfabetyczne"
    fi

    for ((i=0; i<${#val}; i++)); do
        char="${val:$i:1}"

        if [[ "$char" == " " ]]; then
            continue
        fi

        if [[ "$letters" =~ $char ]]; then
            echo "poprawna litera: $char"
            points=$[points + 1]
        else
            echo "Niepoprawna litera: $char !!!"
        fi
    done

    sleep 3

done

echo "Zebrane punkty: $points"
