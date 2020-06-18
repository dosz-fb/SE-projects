#!/usr/bin/env python3
# coding: utf-8

import argparse
import csv
import hashlib

###########################

SCRIPT_VERSION = "2020.06.18.a"

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {SCRIPT_VERSION}')
parser.add_argument('-o', '--output_file', help="CSV file output name (default: output.csv)", default="output.csv")
parser.add_argument('-i', '--input_file', help="CSV file containing the unhashed event data", required=True)
args = parser.parse_args()

print("Processing:")
print("  input_file:", args.input_file)
print("  output_file:", args.output_file)

###########################


def normalizeHash(x):
    s = str(x).encode('utf-8')
    s = s.strip()
    s = s.lower()
    return hashlib.sha256(s).hexdigest()


def hashMatchKeys(columns):
    # replaces columns with the hashed value if it starts with a certain string
    for header in columns:
        if header.startswith("match_key."):
            columns[header] = [normalizeHash(x) for x in columns[header]]
    return columns


def readInput(inputFile):
    """
    if source csv is:
    header1,header2,header3
    value1a,value2a,value3a
    value1b,value2b,value3b

    then returns
    headers=[header1,header2,header3]
    columns={
        header1:[value1a,value1b],
        header2:[value2a,value2b],
        header3:[value3a,value3b],
    }
    """
    with open(inputFile) as inFile:
        reader = csv.reader(inFile)

        headers = next(reader, None)

        column = {}
        for h in headers:
            column[h] = []

        for row in reader:
            for h, v in zip(headers, row):
                column[h].append(v)

        return headers, column


def writeOutput(outputFile, headers, columns):
    with open(outputFile, "w") as outFile:
        outwriter = csv.writer(outFile)

        # add header
        outwriter.writerow(headers)

        # add contents
        numRows = len(columns[headers[0]])
        for i in range(numRows):
            row = []
            for header in headers:
                row.append(columns[header][i])
            outwriter.writerow(row)


def run():
    headers, columns = readInput(args.input_file)
    processedColumns = hashMatchKeys(columns)
    writeOutput(args.output_file, headers, processedColumns)


run()
