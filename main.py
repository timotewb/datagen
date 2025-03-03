from _collections_abc import dict_keys
from typing import Dict, List
from faker import Faker
from datetime import datetime, timedelta
import csv
import json
import os
import random
import uuid

fake:Faker = Faker()
now: datetime = datetime.now()
master_ts: int = 0
unique_ids_list: List[str] = list()

def create_target_directory(target_dir: str) -> str:
    try:
        os.makedirs(os.path.join('data',target_dir), exist_ok=True)
        print(f"Directory '{target_dir}' created successfully or already exists.")
        return os.path.join('data',target_dir)
    except Exception as e:
        print(f"An error occurred while creating directory '{target_dir}': {e}")
        return ''

def generate_unique_ids(num_ids: int) -> List[str]:
    """Generates a list of 'num_ids' unique IDs."""
    unique_ids: List[str] = [ str(uuid.uuid4()) for _ in range(num_ids) ]
    return unique_ids

def choose_random_id(ids_list: List[str]) -> str:
    """Randomly selects an ID from the given list of IDs."""
    if not ids_list:
        raise ValueError("The list of IDs is empty.")
    return random.choice(ids_list)

# for each key in the template generate the data for each entry 'count' times
def generate_random_data(template: Dict[str,str], count:int =1) -> List[Dict[str, str]]:
    data_list:List[Dict[str,str]] = list()
    for _ in range(count):
        data_entry: Dict[str,str] = dict()
        for k, v in template.items():
            data_entry[k] = generate_feild_data(v)
        data_list.append(data_entry)
    return data_list

def generate_feild_data(field_type: str) -> str:
    global master_ts
    if field_type == 'name':
        return fake.name()
    elif field_type == 'datetime':
        return fake.date_time_between(start_date=datetime(now.year, now.month, now.day), end_date=datetime(now.year, now.month, now.day) + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S %Z%z")
    elif field_type == 'address':
        return fake.address()
    elif field_type == 'email':
        return fake.email()
    elif field_type == 'date':
        return fake.date()
    elif field_type == 'random_int':
        return str(random.randint(1, 10000000000000))
    elif field_type == 'random_string':
        return fake.text(100)
    elif field_type == 'ts':
        master_ts+=1
        return str(master_ts)
    elif field_type == 'id':
        return choose_random_id(unique_ids_list)
    else:
        return 'unknown'

def write_csv(data_list: List[Dict[str,str]], file_path: str) -> None:
    if data_list:
        keys: dict_keys[str, str] = data_list[ 0 ].keys()
        with open(file_path, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data_list)
    print(f"Generated CSV file: {file_path}")

def write_json(data_list: List[Dict[str,str]], file_path: str) -> None:
    with open(file_path, 'w') as output_file:
        json.dump(data_list, output_file, indent=2)
    print(f"Generated JSON file: {file_path}")


#----------------------------------------------------------------------------------------
# main
#----------------------------------------------------------------------------------------
def main(template: Dict[str, str], file_count: int, file_format: str, target_directory: str, rows_per_file: int, num_ids: int) -> None:
    global unique_ids_list
    target_directory = create_target_directory(target_directory)
    unique_ids_list = generate_unique_ids(num_ids)
    for i in range(file_count):
        data_list: List[Dict[str, str]] = generate_random_data(template, count=rows_per_file) 
        file_path: str = os.path.join(target_directory, f"output_file_{i + 1}.{file_format}")
        if file_format == 'csv':
            write_csv(data_list, file_path)
        elif file_format == 'json':
            write_json(data_list, file_path)
        else:
            print("Unsupported file format. Please use 'csv' or 'json'.")

if __name__ == "__main__":
    template: Dict[str, str] = {
        "id":"id",
        "ts": "ts",
        "name": "name",
        "address": "address",
        "email": "email",
        "date": "date",
        "random_int": "random_int",
        "random_string": "random_string"
    }

    file_count = int(input("Enter the number of files to generate: "))
    rows_per_file = int(input("Enter the number of row per file to generate: "))
    num_ids = int(input("Enter the number of unique ids to generate: "))
    file_format: str = input("Enter file format (csv/json): ").strip().lower()
    target_directory: str = input("Enter the target directory: ").strip()

    main(template, file_count, file_format, target_directory, rows_per_file, num_ids)