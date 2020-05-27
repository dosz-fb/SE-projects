#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

AD_ACCOUNTS_CSV_FILE=$1
ACCESS_TOKEN_FILE=$2

# Read the access token file
ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})

while IFS="," read -r AD_ACCOUNT_ID SPEND_CAP
do
    if [ -z "${AD_ACCOUNT_ID}" ]; then
        echo "action = account is blank, skipping"
        continue
    fi

    if [ -z "${SPEND_CAP}" ]; then
        echo "action = spend cap for account ${AD_ACCOUNT_ID} is blank, skipping"
        continue
    fi

    echo "action = set spend cap for account ${AD_ACCOUNT_ID} to ${SPEND_CAP}"
    
    # check the existing spending limit
    preChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v7.0/act_${AD_ACCOUNT_ID})"
    echo "pre = $preChange"
    
    # change the spend limit value
    doChange="$(curl -X POST -s \
                    --data spend_cap=${SPEND_CAP} \
                    --data access_token=${ACCESS_TOKEN} \
                    https://graph.facebook.com/v6.0/act_${AD_ACCOUNT_ID})"
    echo "do = $doChange"
    
    # check the new spending limit
    postChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v7.0/act_${AD_ACCOUNT_ID})"
    echo "post = $postChange"
done < ${AD_ACCOUNTS_CSV_FILE}

echo "done"
