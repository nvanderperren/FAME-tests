#!/bin/bash
doel_folder=$2

for folder in $1/*
do
    echo $folder
    cd $folder
    name=${PWD##*/}
    echo $name
    doel="$doel_folder/$name"
    mkdir $doel
    rsync -ra *.jpg $doel
done
