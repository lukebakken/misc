#!/usr/bin/env bash

set -o nounset

while IFS=$'\t' read -r name password
do
    escript ./test.escript "$name" "$password"
done < 'users.txt'
