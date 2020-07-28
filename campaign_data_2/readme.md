# Campaign Script 2

Used to pull fb insights data into a csv, including custom conversions.

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
python3 campaign_data_2.py --version

python3 campaign_data_2.py --ad_accounts_file accounts.txt --access_token_file token.txt --output_file output.csv
```


### Output Files

 * output.csv - file containing a list of ad account id's separated by new lines
    ```
      "account_id","account_name","campaign_id","campaign_name","account_currency","spend","reach","frequency","impressions","cpm","clicks","cpc","ctr","inline_link_clicks","inline_link_click_ctr","cost_per_inline_link_click","date_start","date_stop"
      "12345","account 12345","23457","campaign name","USD","129.12","45074","5.398804","252803","26.580516","346","6.038966","0.357005","266","0.269705","2.661129","2019-07-01","2019-07-31"
    ```
