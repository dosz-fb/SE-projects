# Live Stream Counts

Count the number of live streams per fb page.

See https://developers.facebook.com/docs/graph-api/reference/page/live_videos/

## Requirements

* bash
* curl
* jq

### Required Files

 * page_ids.csv - csv file containing the page names and urls
    ```
      Page Name 1,http://facebook.com/123,
      Page Name 2,http://facebook.com/456,
    ```
 * access_token.txt - file containing only the access token that can access your ad accounts
    ```
      EAABsbCS.....
    ```

## Usage:

```
bash live_stream_counts.sh page_ids.csv access_token.txt > out.csv
```


### Outputs

 * outputs the statistics for each video for each page to standard out, which is piped to a csv file
    ```
      PAGE_ID,VIDEO_ID,BROADCAST_TIME,LIVE_VIEWS,LIKES,PERMALINK_URL
      123,789,2019-11-29T18:39:41+0000,0,3,/123/videos/789/
      123,345,2019-11-29T17:39:33+0000,0,4,/123/videos/345/
      456,246,2019-07-13T19:44:30+0000,0,5,/456/videos/246/
    ```
