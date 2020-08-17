#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

API_VERSION="v8.0"
PAGE_ID_CSV_FILE=$1
ACCESS_TOKEN_FILE=$2

# Read the access token file
ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})

while IFS="," read -r PAGE_NAME PAGE_URL REST
do
    if [ -z "${PAGE_URL}" ]; then
        echo "Page url blank, skipping"
        continue
    fi

    PAGE_ID="$(echo ${PAGE_URL} | grep / | cut -d/ -f4-)"

    if [ -z "${PAGE_ID}" ]; then
        echo "Page ID blank, skipping"
        continue
    fi

    # echo "processing page ${PAGE_ID}"

    # check the existing spending limit
    LIVE_STREAMS_JSON="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data limit=10000 \
                    https://graph.facebook.com/${API_VERSION}/${PAGE_ID}/live_videos)"

    # post process the results
    LIVE_STREAM_COUNT="$(echo ${LIVE_STREAMS_JSON} | jq '.data' | jq length)"
    echo "${PAGE_ID} ${LIVE_STREAM_COUNT}"

done < ${PAGE_ID_CSV_FILE}

echo "done"
