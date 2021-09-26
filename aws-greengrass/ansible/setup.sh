#!/bin/bash
mkdir -p keys

KEY_PATH=./keys/id_rsa
ssh-keygen -t rsa -b 2048 -C $USER_MAIL -f $KEY_PATH -q -N ""

set -e
for VAR in $(compgen -e); do
    if echo "$VAR" | grep -q '^GREENGRASS_CORE_HOST_'; then
        VAR_NAME=$(echo "$VAR" | sed -e 's/^GREENGRASS_CORE_HOST_//' -e 's/__/./g' | tr '[:upper:]' '[:lower:]' | tr -d '[:cntrl:]')
        VAR_VALUE=$(echo "${!VAR}" | tr -d '[:cntrl:]')
        echo "Copy $KEY_PATH to host $VAR_VALUE"

        if ssh-copy-id -f -i $KEY_PATH $VAR_VALUE; then
            ssh -i $KEY_PATH $VAR_VALUE 'sudo sed -i "s/PasswordAuthentication yes/PasswordAuthentication no/g" /etc/ssh/sshd_config; sudo systemctl restart ssh'
        fi
    fi
done
