#!/bin/bash


# read -p "Podaj tekst: " tekst
# read -p "Wybierz (e-encrypt / d-decrypt): " wyb
# read -p "Podaj offset: " offset

tekst="CezZar"
wyb="d"
offset=3


############################


chr() {
  [ "$1" -lt 256 ] || return 1
  printf "\\$(printf '%03o' "$1")"
}

ord() {
  LC_CTYPE=C printf '%d' "'$1"
}



dlugoscAlfabetu=$[ $(ord "Z") - $(ord "A") + 1]
# echo "Caly $dlugoscAlfabetu"

if [ $wyb == "e" ]; then
    echo "Enkryptowanie"

elif [[ $wyb == "d" ]]; then
    echo "Dekryptowanie"
    offset=$[ - $offset ]
else
    echo "Nieznana opcja: $wyb"
    exit
fi

while [[ $offset -lt 0 ]]; do
    offset=$[$offset + $dlugoscAlfabetu]
done


for (( i=0; i<${#tekst}; i++ )); do
    # echo "${tekst:$i:1}"
    asciiNum=$(ord "${tekst:$i:1}")
    # echo "najp $asciiNum"

    if [[ $asciiNum -ge $(ord "a") ]]; then
        # Mala
        asciiOffset=$(ord "a")
    else
        # Duza
        asciiOffset=$(ord "A")
    fi


    alfNum=$[$asciiNum - $asciiOffset]
    alfNum=$[$alfNum + $offset]
    alfNum=$[$alfNum % $dlugoscAlfabetu]
    newNum=$[$alfNum + $asciiOffset]
    # echo "pozni $alfNum + $asciiOffset = $newNum"

    newChar=$(chr $newNum)
    printf $newChar

done

echo ""