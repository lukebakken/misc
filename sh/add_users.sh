#!/usr/bin/env bash

# set -o xtrace
set -o errexit
set -o nounset
set -o pipefail

while IFS=$'\t' read -r name password
do
    /home/lbakken/development/rabbitmq/rabbitmq-server/sbin/rabbitmqctl add_user "$name" "$password"
done < 'users.txt'
