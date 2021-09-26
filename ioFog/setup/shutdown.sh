#!/bin/bash

KEY_PATH=./keys/id_rsa
for VAR in $(compgen -e); do
    if echo "$VAR" | grep -q '^IO_FOG_HOST_'; then
        VAR_NAME=$(echo "$VAR" | sed -e 's/^IO_FOG_HOST_//' -e 's/__/./g' | tr '[:upper:]' '[:lower:]' | tr -d '[:cntrl:]')
        VAR_VALUE=$(echo "${!VAR}" | tr -d '[:cntrl:]')
        echo "Shutting down $VAR_VALUE ..."
        ssh -i $KEY_PATH $VAR_VALUE 'sudo shutdown now'
    fi
done
