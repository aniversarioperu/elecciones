import csv
from random import randint
from time import sleep
import requests
import json
import sys

MAX_RETRIES = 5

def do_get(url, retry=0):
    res = s.get(url)
    if res.status_code == 404:
        return None
    data = res.json()
    if not data:
        if retry > MAX_RETRIES:
            return None
        retry += 1
        sleep(1 * retry * retry)
        return do_get(url, retry)
    return data

base_url = "https://2601202919738512020.eleccionescongresales2020.pe/v1/ECE2020/mesas/detalle/"

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'Origin': 'https://resultados.eleccionescongresales2020.pe',
    'X-Requested-With': 'XMLHttpRequest'
})

def download_by_ids(all_ids):
    for i in all_ids:
        if i == 0:
            continue
        # sleep(randint(0, 2))
        acta = f"{i}".zfill(6)
        url = f"{base_url}{acta}"
        print(acta)

        data = do_get(url)
        data['acta'] = acta
        with open("all_data.json", "a") as handle:
            handle.write(json.dumps(data) + "\n")

crawled_so_far = []
try:
    with open("all_data.json", "r") as handle:
        for line in handle:
            line = json.loads(line)
            try:
                acta = line['acta']
            except:
                continue
            crawled_so_far.append(int(acta))
except FileNotFoundError:
    pass

input_file = sys.argv[1]

all_ids = []
with open(input_file, 'r') as handle:
    for line in handle:
        line = int(line.strip())
        if line not in crawled_so_far:
            all_ids.append(line)

print(len(all_ids))

download_by_ids(all_ids)
