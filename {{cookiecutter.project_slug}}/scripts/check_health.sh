#!/bin/bash

# Check if directory is mounted
path=("/app/upload" "/app/output")

for item in "${path[@]}"
do
    ls $item > /dev/null

    if [ $? -ne 0 ]; then
        echo "$item Mount error"
        exit 1
    fi
done
