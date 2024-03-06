import pandas as pd
import hashlib
import csv
import re

filename = "test-delete3.xlsx"
###print(filename)

df = pd.read_excel(filename, engine='openpyxl')
header = ['hash', 'source', 'destination', 'host']

# Pre-compile the regular expressions
games_re = re.compile(r'games|editorial|ps4-games|ps-vr-games|ps-plus|on_ps3|on-psvita|spongebob|ace-combat|ps-vr2')
support_re = re.compile(r'support|soporte')

# Initialize dictionaries to hold categorized data
games_data, support_data, general_data = [], [], []

for index, row in df.iterrows():
    source_data = row['source']
    source_hash = hashlib.sha256(source_data.encode('utf-8')).hexdigest()
    destination = row['destination']
    host = row['hostname']
    ekvitem = [source_hash, source_data, destination, host]

    if games_re.search(source_data):
        games_data.append(ekvitem)
    elif support_re.search(source_data):
        support_data.append(ekvitem)
    else:
        general_data.append(ekvitem)

# Write data to files
def write_data(filename, header, data):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

write_data('mp-test-games-upload.csv', header, games_data)
write_data('mp-test-support-upload.csv', header, support_data)
write_data('mp-test-general-upload.csv', header, general_data)
