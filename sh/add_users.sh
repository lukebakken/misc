#!/usr/bin/env bash

# set -o xtrace
set -o errexit
set -o nounset
set -o pipefail

while IFS=$'\t' read -r name password
do
    echo "USER: $name"
    set +o errexit
    /home/lbakken/development/rabbitmq/rabbitmq-server/sbin/rabbitmqctl add_user "$name" "$password"
    set -o errexit
    /home/lbakken/development/rabbitmq/rabbitmq-server/sbin/rabbitmqctl set_permissions "$name" '.*' '.*' '.*'
    /home/lbakken/development/rabbitmq/rabbitmq-server/sbin/rabbitmqctl list_user_permissions "$name"
    echo
done < 'users.txt'

/home/lbakken/development/rabbitmq/rabbitmq-server/sbin/rabbitmqctl list_users
