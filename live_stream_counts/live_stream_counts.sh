#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

API_VERSION="v7.0"
PAGE_ID_CSV_FILE=$1
ACCESS_TOKEN_FILE=$2

# Read the access token file
ACCESS_TOKEN=$(cat ${ACCESS_TOKEN_FILE})

# print the headers
echo "PAGE_ID,VIDEO_ID,BROADCAST_TIME,LIVE_VIEWS,LIKES,PERMALINK_URL"

while IFS="," read -r PAGE_NAME PAGE_URL REST
do
    if [ -z "${PAGE_URL}" ]; then
        # echo "Page url blank, skipping"
        continue
    fi

    PAGE_ID="$(echo ${PAGE_URL} | grep / | cut -d/ -f4-)"

    if [ -z "${PAGE_ID}" ]; then
        # echo "Page ID blank, skipping"
        continue
    fi

    # echo "processing page ${PAGE_ID}"

    # for docs see https://developers.facebook.com/docs/graph-api/reference/page/live_videos/
    # for testing see https://developers.facebook.com/tools/explorer/

    # check the existing spending limit
    LIVE_STREAMS_JSON="$(curl -X GET -s -G \
                    --data access_token=${ACCESS_TOKEN} \
                    --data fields="live_views,status,permalink_url,creation_time,video,broadcast_start_time,likes.summary(true),description" \
                    --data limit=10000 \
                    https://graph.facebook.com/${API_VERSION}/${PAGE_ID}/live_videos)"

    # post process the results
    LIVE_STREAM_COUNT="$(echo ${LIVE_STREAMS_JSON} | jq '.data' | jq length)"
    COUNTER=0
    while [ ${COUNTER} -lt ${LIVE_STREAM_COUNT} ]
    do
        DATA_ENTRY="$(echo ${LIVE_STREAMS_JSON} | jq '.data' | jq .[${COUNTER}])"
        # echo "debug" ${COUNTER} ${DATA_ENTRY}
        VIDEO_ID="$(echo ${DATA_ENTRY} | jq -r '.video.id')"
        LIVE_VIEWS="$(echo ${DATA_ENTRY} | jq -r '.live_views')"
        BROADCAST_TIME="$(echo ${DATA_ENTRY} | jq -r '.broadcast_start_time')"
        PERMALINK_URL="$(echo ${DATA_ENTRY} | jq -r '.permalink_url')"
        LIKES="$(echo ${DATA_ENTRY} | jq -r '.likes.summary.total_count')"
        # print each row
        echo "${PAGE_ID},${VIDEO_ID},${BROADCAST_TIME},${LIVE_VIEWS},${LIKES},${PERMALINK_URL}"
        ((COUNTER++))
    done

done < ${PAGE_ID_CSV_FILE}

echo "done"
