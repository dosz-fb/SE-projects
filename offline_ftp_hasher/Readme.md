# Hash Offline Events CSV for sFTP

A script to hash the 'match_key' columns of a csv for the offline events ftp upload.

https://developers.facebook.com/docs/marketing-api/offline-conversions/sftp

## Requirements:

* sample.inputs.csv - is a file that contains a the unhashed events data
  ```
    currency,event_name,event_time,match_key.country,match_key.ct,match_key.email,match_key.fn,match_key.ln,match_key.phone,match_key.st,match_key.zip,value
    USD,Purchase,1579496400,US,Stanford,abc@tfbnw.net,Boris,Johnson,12345673423,California,94305,127374
    USD,Purchase,1584158400,US,Boston,def@tfbnw.net,Donald,Trump,12345672857,Massachusetts,02117,84413
    USD,Purchase,1580187600,US,Menlo Park,hij@tfbnw.net,Justin,Trudeau,12345671618,California,94025,82092
  ```
  
## Usage:

```
python3 offline_events_hasher.py -husage: offline_events_hasher.py [-h] [-v] [-o OUTPUT_FILE] -i INPUT_FILE

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        CSV file output name (default: output.csv)
  -i INPUT_FILE, --input_file INPUT_FILE
                        CSV file containing the unhashed event data
```

```
# example:

python3 offline_ftp_hasher.py -i sample.inputs.csv -o sample.output.csv
```

## Web UI

To setup the upload using the UI, navigate to:

https://business.facebook.com > Events Manager > Upload Offline Events

## API Method

An alternative to the sftp upload is using the API:

https://developers.facebook.com/docs/marketing-api/offline-conversions
