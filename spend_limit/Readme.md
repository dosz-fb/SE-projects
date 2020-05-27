# Adjust Ad Account Spend Limits

A script to update spend_cap for a list of ad accounts.
Another script to reset the amount_spent for a list of ad accounts.

see https://developers.facebook.com/docs/marketing-api/reference/ad-account#Updating

## Requirements:

* sample_ad_accounts.csv - is a file that contains a comma separated account and spend cap value on multiple lines
  ```
    12345, 100
    67890, 200
    1233, 300.5
    12424, 400
  ```
* sample_access_token.txt - file containing only the access token that can edit your ad accounts
  ```
    EAABsbCS.....
  ```
  
## Usage:

```
# To set the spend limit, run this script
# bash spend_limit_cap.sh AD_ACCOUNTS_CAP_CSV ACCESS_TOKEN_FILE

bash spend_limit_cap.sh sample_ad_accounts.txt sample_access_token.txt 100.00
```

```
# When you want to reset the spent counter, can use this script
# bash spend_limit_reset.sh AD_ACCOUNTS_CAP_CSV ACCESS_TOKEN_FILE

bash spend_limit_reset.sh sample_ad_accounts.txt sample_access_token.txt
```
