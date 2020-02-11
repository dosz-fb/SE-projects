# Campaign Script

Used to pull fb insights data into a csv.

## Requirements

* Python 3
* Requests library (pip3 install requests)

### Required Files

 * accounts.txt - file containing a list of ad account id's separated by new lines
    ```
      12345
      67890
      1233
      12424
    ```
 * token.txt - file containing only the access token that can access your ad accounts
    ```
      EAABsbCS.....
    ```

## Usage:

```
python3 campaign_data.py --version

python3 campaign_data.py --ad_accounts_file accounts.txt --access_token_file token.txt --start_time 2020-02-04 --end_time 2020-02-11 --output_file output.csv
```
