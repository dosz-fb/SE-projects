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
    preChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v7.0/act_${AD_ACCOUNT_ID}?access_token=${ACCESS_TOKEN}&fields=spend_cap%2Camount_spent)"
    echo "pre = $preChange"
    doChange="$(curl -X POST -s \
                    --data spend_cap=${SPEND_CAP} \
                    --data access_token=${ACCESS_TOKEN} \
                    https://graph.facebook.com/v6.0/act_${AD_ACCOUNT_ID})"
    echo "do = $doChange"
    postChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/v7.0/act_${AD_ACCOUNT_ID})"
    echo "post = $postChange"
done < ${AD_ACCOUNTS_CSV_FILE}

echo "done"

#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

AD_ACCOUNTS_FILE=$1
ACCESS_TOKEN_FILE=$2

ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})
for AD_ACCOUNT_ID in $(cat ${AD_ACCOUNTS_FILE}); do
done

echo "done"


#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

API_VERSION="v7.0"
AD_ACCOUNTS_CSV_FILE=$1
ACCESS_TOKEN_FILE=$2

# Read the access token file
ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})

while IFS="," read -r AD_ACCOUNT_ID SPEND_CAP
do
    echo "action = set spend cap for account ${AD_ACCOUNT_ID} to ${SPEND_CAP}"

    # check the current value
    preChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/${API_VERSION}/act_${AD_ACCOUNT_ID}?access_token=${ACCESS_TOKEN}&fields=spend_cap%2Camount_spent)"
    echo "pre = $preChange"

    # set the spend cap value
    doChange="$(curl -X POST -s \
                    --data spend_cap=${SPEND_CAP} \
                    --data access_token=${ACCESS_TOKEN} \
                    https://graph.facebook.com/${API_VERSION}/act_${AD_ACCOUNT_ID})"
    echo "do = $doChange"

    # check the changed value
    postChange="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields=spend_cap,amount_spent \
                    https://graph.facebook.com/${API_VERSION}/act_${AD_ACCOUNT_ID})"
    echo "post = $postChange"

done < ${AD_ACCOUNTS_CSV_FILE}

echo "done"
