import json
import csv
import sys


input_file = sys.argv[1]

data = []
with open(input_file, 'r') as handle:
    for i in handle.readlines():
        i = json.loads(i)
        data.append(i)


with open("output.csv", "w") as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data:
        writer.writerow(i)
