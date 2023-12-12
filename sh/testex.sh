#!/usr/bin/env bash

set -o nounset

while IFS=$'\t' read -r name password
do
    ./testex/testex "$name" "$password" # < /dev/null
done < 'users.txt'
