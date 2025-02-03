import os
import json
import csv

def work():
    input_json_file = [f for f in os.listdir() if f.endswith('.json')]
    if len(input_json_file) != 1:
        print("Folder musi zawierać dokładnie jeden plik .json ze skryptem do przetłumaczenia.")
        return
    
    input_json_file = input_json_file[0]
    with open(input_json_file, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    
        # Pliki CSV
    character_data_csv = "character_data.csv"  # Plik CSV z danymi postaci
    translations_csv = "translations_pl_PL.csv"  # Plik CSV z tłumaczeniami

    # Wczytaj dane z pliku character_data.csv
    character_data = {}
    with open(character_data_csv, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            character_data[row['id']] = row

    # Wczytaj dane z pliku translations_pl_PL.csv
    translations = {}
    with open(translations_csv, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            translations[row['id']] = row

    # Tworzenie nowego JSON-a
    new_json_data = []
    for item in json_data:
        if isinstance(item, dict) and item['id'] == '_meta':
            new_json_data.append(item)  # Zachowaj oryginalne mapy
        elif isinstance(item, str) or isinstance(item, dict):
            # Dodaj nową mapę, jeśli klucz istnieje w danych CSV
            idd = ''
            if isinstance(item, dict):
                idd = item['id']
            else:
                idd = item
            merged_map = character_data.get(idd, {}).copy()
            if idd in translations:
                merged_map.update({k: v for k, v in translations[idd].items() if v})
            
            if 'id' in merged_map:
                merged_map['id'] = f"pl_PL_{merged_map['id']}"

            for key in ['reminders', 'remindersGlobal']:
                if key in merged_map:
                    if merged_map[key] == "":
                        merged_map[key] = []
                    else:
                        merged_map[key] = merged_map[key].split(',')
            
            for key in ['firstNight', 'otherNight']:
                if key in merged_map:
                    try:
                        merged_map[key] = float(merged_map[key])
                    except ValueError:
                        print("error",key,merged_map['id'])
                        merged_map[key] = 0.0
            
            if 'setup' in merged_map:
                if merged_map['setup'] == 'true' or merged_map['setup'] == 'True':
                    merged_map['setup'] = True
                else:
                    merged_map['setup'] = False
                    
            if 'edition' in merged_map:
                merged_map['edition'] = 'custom'

            new_json_data.append(merged_map)
    

    # Nazwa nowego pliku JSON
    output_json_file = input_json_file.replace('.json', '_PL.json')

    # Zapisz nowy plik JSON
    with open(output_json_file, 'w', encoding='utf-8') as output_file:
        json.dump(new_json_data, output_file, ensure_ascii=False, indent=4)

    print(f"Nowy plik JSON zapisany jako: {output_json_file}")

if __name__ == "__main__":
    work()