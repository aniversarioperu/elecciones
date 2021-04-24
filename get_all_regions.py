import json

data = []

break_ = False
j = 0

with open("complete.json", "r") as handle:
    for i in handle.readlines():
        j += 1
        data.append(json.loads(i))
        if break_ and j > 1000:
            break

print(len(data))

# get a list of regions and all votes
regions = dict()
frepap = dict()
frepap_distritos = dict()

for i in data:
    department = i.get("departamento")
    if department not in regions:
        regions[department] = 0
    if department not in frepap:
        frepap[department] = 0

    try:
        votos = int(i.get('total_votos', 0))
    except:
        votos = 0

    regions[department] += votos

    if 'frepap' in i['org_politica'].lower():
        frepap[department] += votos

        if department == 'LIMA':
            dist = f'{i["provincia"]}-{i["distrito"]}'
            if dist not in frepap_distritos:
                frepap_distritos[dist] = 0
            frepap_distritos[dist] += votos


with open('todos_votos.csv', 'w') as handle:
    for k, v in regions.items():
        handle.write(f"{k},{v}\n")
print(regions)

with open('frepap_votos.csv', 'w') as handle:
    for k, v in frepap.items():
        handle.write(f"{k},{v}\n")
print(frepap)

# frepap per distrito de lima
with open('frepap_votos_lima.csv', 'w') as handle:
    for k, v in frepap_distritos.items():
        handle.write(f"{k},{v}\n")
