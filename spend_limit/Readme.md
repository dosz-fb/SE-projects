# Adjust Ad Account Spend Limits

A script to update spend_cap for a list of ad accounts.
Another script to reset the amount_spent for a list of ad accounts.

see https://developers.facebook.com/docs/marketing-api/reference/ad-account#Updating

## Requirements:

* accounts.txt - is a file that contains ad accounts separated by new lines
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
# To set the spend limit, run this script
# bash spend_limit_sh AD_ACCOUNTS_FILE ACCESS_TOKEN_FILE SPEND_CAP_FLOAT

bash spend_limit.sh accounts.txt token.txt 100.00
```

```
# When you want to reset the spent counter, can use this script
# bash reset_spent.sh AD_ACCOUNTS_FILE ACCESS_TOKEN_FILE

bash reset_spent.sh accounts.txt token.txt
```
