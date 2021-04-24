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

all_ids = set()

data = []

with open('complete.json', 'r') as handle:
    for i in handle.readlines():
        i = json.loads(i)
        data.append(i)
        number = int(i['mesa_numero'])
        all_ids.add(number)

missing = set()

for i in range(1, 82_000):
    if i not in all_ids:
        missing.add(i)

print(f'missing {len(missing)}')
print(f'downloading missing {missing}')

download_by_ids(list(missing))

incomplete_downloaded = set()
with open('missing1.json', 'r') as handle:
    for i in handle:
        i = json.loads(i)
        number = int(i['mesa_numero'])
        incomplete_downloaded.add(number)

incomplete_ids = set()

for i in data:
    estado = i['estado_proceso']
    if estado in estados_incompleto and i['mesa_numero'] not in incomplete_downloaded:
        incomplete_ids.add(i['mesa_numero'])

with open('cleaned.json', 'w') as handle:
    for i in data:
        if i['mesa_numero'] in incomplete_ids:
            continue
        handle.write(json.dumps(i) + '\n')

print(f'to update {len(incomplete_ids)}')
download_by_ids(list(incomplete_ids))
