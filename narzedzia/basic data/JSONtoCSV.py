import json
import csv
import os

input_json_file = "characters.json"  
with open(input_json_file, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)


images = {}
with open('images.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        images[row['id']] = row['url']

fields_data = []
for entry in json_data:
    fields = entry["fields"].copy()
    
    idd = fields["character_id"]
    if idd in images.keys():
        fields["image_url"] = images[idd]

    fields_data.append(fields)

output_csv_file = "output.csv"

with open(output_csv_file, 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fields_data[0].keys())
    writer.writeheader()
    writer.writerows(fields_data)

print(f"Dane zostały zapisane do pliku: {output_csv_file}")