# Live Stream Counts

Count the number of live streams per fb page

## Requirements

* bash
* curl
* jq

### Required Files

 * page_ids.csv - csv file containing the page names and urls
    ```
      Simi Valley,http://facebook.com/123010591950,
      South Holland,http://facebook.com/45644618821862,
    ```
 * access_token.txt - file containing only the access token that can access your ad accounts
    ```
      EAABsbCS.....
    ```

## Usage:

```
bash live_stream_counts.sh page_ids.csv access_token.txt
```


### Outputs

 * outputs the page id and the count to standard out
    ```
      123010591950 12
      45644618821862 4
    ```
