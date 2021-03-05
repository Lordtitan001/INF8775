#!/bin/bash/python

has_algo="false"
has_path="false"
has_d_couple="false"
has_d_time="false"
args=""


check_algo() {
    if [ $algo != 'brute' ] && [ $algo != 'recursif' ] && [ $algo != 'seuil' ]
    then
        echo "-a $algo is not a valid parameter. Choose between {brute, recursif, seuil}";
        exit -1
    else 
        has_algo="true"
        args="$args -a $algo "
    fi
}

check_path() {
    has_path="true"
    args="$args -e $path "
}

check_d_couple() {
    has_d_couple="true"
    args="$args -p true "
}

check_d_time() {
    has_d_time="true"
    args="$args -t true "
}

while getopts a:e:p:t: flag
do
    case "${flag}" in
        a) algo=${OPTARG}; check_algo;;
        e) path=${OPTARG}; check_path;;
        p) d_couple=${OPTARG}; check_d_couple;;
        t) d_time=${OPTARG}; check_d_time;;
    esac
done


launch_code() {
    ./solution.py $args
}

if [ $has_algo = "true" ] && [ $has_path = "true" ]
then
    launch_code
else
    echo "Please add all the mandatory parameters: { -a {brute, recursif, seuil} -e CHEMIN_EXEMPLAIRE }"
fi