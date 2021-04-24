# replace missing actas in downloaded
import json

from bajame_actas import download_by_ids

estados_incompleto = [
    'ACTA ELECTORAL ANULADA',
    'ACTA SIN FIRMAS',
    'ERROR MATERIAL',
    'ILEGIBILIDAD',
    'INCOMPLETA',
    'MESA NO INSTALADA',
    'OTRAS OBSERVACIONES',
    'VOTOS IMPUGNADOS',
]

data = dict()

all_ids = set()


with open('complete.json', 'r') as handle:
    for i in handle.readlines():
        i = json.loads(i)
        key = f'mesa {i["mesa_numero"]} ubigeo {i["ubigeo"]} org politica {i["org_politica"]}'
        data[key] = i
print(len(data))

to_replace = []

with open('missing.json', 'r') as handle:
    for i in handle:
        i = json.loads(i)
        key = f'mesa {i["mesa_numero"]} ubigeo {i["ubigeo"]} org politica {i["org_politica"]}'
        if i['estado_proceso'] == 'CONTABILIZADAS NORMALES':
            data[key] = i

with open("fixed.json", "w") as handle:
    for key, value in data.items():
        handle.write(json.dumps(value) + '\n')

