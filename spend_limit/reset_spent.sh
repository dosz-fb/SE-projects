#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

AD_ACCOUNTS_FILE=$1
ACCESS_TOKEN_FILE=$2

ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})
for AD_ACCOUNT_ID in $(cat ${AD_ACCOUNTS_FILE}); do
    # check the existing spending limit
    preChange="$(curl -X GET -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v6.0/act_${AD_ACCOUNT_ID})"
    echo "pre = $preChange"

    # reset the spent counter
    doChange="$(curl -X POST \
                    --data spend_cap_action=reset \
                    --data access_token=${ACCESS_TOKEN} \
                    https://graph.facebook.com/v6.0/act_${AD_ACCOUNT_ID})"
    echo "do = $doChange"

    # check the new spending limit
    postChange="$(curl -X GET -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v6.0/act_${AD_ACCOUNT_ID})"
    echo "post = $postChange"
done

echo "done"
