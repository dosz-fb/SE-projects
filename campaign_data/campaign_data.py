#!/usr/bin/env python3
# coding: utf-8

import requests
import re
import csv
import time
import argparse

###########################

SCRIPT_VERSION = "2020.02.11.a"
API_VERSION = "v5.0"

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {SCRIPT_VERSION}')
parser.add_argument('-o', '--output_file', default="output.csv", help="CSV file output name (default: output.csv)")
parser.add_argument('-d', '--ad_accounts_file', help="File with all the ad account id's separated by new lines", required=True)
parser.add_argument('-a', '--access_token_file', help="File with the facebook access token to make API calls", required=True)
args = parser.parse_args()

print("Processing:")
print("  ad_account_ids_file:", args.ad_accounts_file)
print("  access_token_file:", args.access_token_file)
print("  output_file: ", args.output_file)

###########################

stats = {
    "start_time": time.time(),
    "success_count": 0,
    "error_count": 0,
    "conversion_errors": dict(),
    "conversion_count": 0,
    "conversion_size": 0,
    "insight_errors": dict(),
    "insight_count": 0,
    "insight_size": 0,
    "had_error": None,
}

###########################

# get time ranges
time_ranges = [
    {"start": "2020-02-04", "end": "2020-02-11"},
]

###########################

ACCESS_TOKEN = ""
with open(args.access_token_file, "r") as access_token_file:
    lines = access_token_file.readlines()
    ACCESS_TOKEN = lines[0].strip()
    if len(ACCESS_TOKEN) == 0:
        raise Exception("Error: Access Token is invalid")
    #print(ACCESS_TOKEN)

AD_ACCOUNT_IDS=[]
with open(args.ad_accounts_file, "r") as account_file:
    lines = account_file.readlines()
    accounts = [line.strip() for line in lines if len(line.strip()) > 0]
    AD_ACCOUNT_IDS = [account for account in accounts if not account.startswith("#")]
    print("Number of Ad Accounts: ", len(AD_ACCOUNT_IDS))

###########################

# get custom conversion ids

# map<ad_account_id, map<cc_id, cc_name>>
conversions = dict()

for i, AD_ACCOUNT_ID in enumerate(AD_ACCOUNT_IDS):
    url = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/customconversions?fields=name&limit=500&access_token={ACCESS_TOKEN}"
    resp = requests.get(url)

    if resp.status_code != 200:
        stats["conversion_errors"][AD_ACCOUNT_ID] = resp.json()
        stats["error_count"] += 1
        continue

    stats["success_count"] += 1
    stats["conversion_size"] += len(resp.content)
    data = resp.json().get("data")
    code_mapping = dict()
    for entry in data:
        # TODO: this is pretty custom for one customer
        name = entry.get("name")
        if len(name.split(" - ")) == 0:
            continue
        code_mapping[entry.get("id")] = name.split(" - ")[0]
    conversions[AD_ACCOUNT_ID] = code_mapping
    stats["conversion_count"] += 1

###########################

# quit if the access token is bad
if stats["success_count"] == 0 and stats["error_count"] > 0:
    stats["end_time"] = time.time()
    print("Execution time (s): ", stats["end_time"] - stats["start_time"])
    print(stats)
    raise Exception("No successful API calls, Access Token is probably bad (expired/no permissions)")

###########################

def dumpOutput(insights):
    # get all rows
    all_columns = []
    for entry in insights:
        for key in entry.keys():
            if key not in all_columns:
                all_columns.append(key)

    # flatten data and clean up missing rows
    with open(args.output_file, "w") as csvfile:
        outwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)

        # add header
        outwriter.writerow(all_columns)

        # add contents
        for entry in insights:
            row = []
            for column in all_columns:
                row.append(entry.get(column))
            outwriter.writerow(row)

    stats["end_time"] = time.time()
    print("Execution time (s): ", stats["end_time"] - stats["start_time"])
    print(stats)

###########################

# get the insights for the adsets

# map<ad_account_id, map<campaign_id, insight_json>>
insights = []

try:
    for i, AD_ACCOUNT_ID in enumerate(AD_ACCOUNT_IDS):
        if i % 5 == 0:
            print(f"Processing ad account id entry {i + 1}")

        for time_range in time_ranges:
            start_time_range = time_range["start"]
            end_time_range = time_range["end"]
            params = {
                "fields": "account_id,account_name,campaign_id,campaign_name,reach,impressions,frequency,spend,cpm,cpc,actions",
                "level": "campaign",
                "limit": 5000,
                "attribution_windows": "28d_click,28d_view",
                "time_range": """{"since":"%s","until":"%s"}""" % (start_time_range, end_time_range),
                "access_token": ACCESS_TOKEN,
            }
            url = f"https://graph.facebook.com/{API_VERSION}/act_{AD_ACCOUNT_ID}/insights"
            resp = requests.get(url, params = params)
            #insights?fields=reach,spend,campaign_id,campaign_name,cpm,cpc,frequency,impressions,actions&level=campaign&attribution_windows=28d_click,28d_view&time_range={"since":"2020-02-04","until":"2020-02-11"}

            if resp.status_code != 200:
                stats["insight_errors"][f"{AD_ACCOUNT_ID}/{start_time_range}"] = resp.json()
                stats["error_count"] += 1
                continue

            stats["success_count"] += 1
            stats["insight_size"] += len(resp.content)
            if len(resp.json().get("data")) == 0:
                continue

            insight_data = resp.json().get("data")

            for insight in insight_data:

                # convert the custom conversions from action
                actions = insight.pop("actions", [])
                for action in actions:
                    if "offsite_conversion.custom" not in action.get("action_type"):
                        # not interested in this action type
                        continue
                    # convert the type to the name and add it to the dict
                    conversion_ids = re.findall('[0-9]+', action.get("action_type"))

                    if len(conversion_ids) == 0:
                        continue

                    conversion_id = conversion_ids[0]
                    if conversion_id in conversions[AD_ACCOUNT_ID]:
                        insight[conversions[AD_ACCOUNT_ID][conversion_id]] = action.get("value")

                insights.append(insight)
                stats["insight_count"] += 1
except :
    dumpOutput(insights)
    print("Done with errors")

else:
    # remove errors if there's nothing wrong
    stats.pop("conversion_errors")
    stats.pop("insight_errors")

    dumpOutput(insights)
    print("Done all")
