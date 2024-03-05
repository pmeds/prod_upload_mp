import pandas as pd
import requests
import hashlib
from concurrent.futures import ThreadPoolExecutor
import time
import warnings

print("Waiting for 15 seconds for EKV to reach eventual consistency. Please be patient.")
time.sleep(15)


requests.packages.urllib3.disable_warnings()

# Function to process each row
def process_row(row):
    source_data = row['source']
    destination = row['destination']
    host = row['hostname']
    fRedirect = 'https://' + host + destination
    url = 'https://www.playstation.com' + source_data
    headers = {"Accept": "text/html"}

    # Make the GET request, with allow_redirects set to false
    response = requests.get(url, headers=headers, allow_redirects=False)
    rresponse = response.status_code
    rlocation = response.headers.get('Location', None)
    source_hash = hashlib.sha256(source_data.encode('utf-8')).hexdigest()
    if rresponse != 301:
        print(f"Status code {rresponse} is incorrect for URL {url}, hash {source_hash}")
    elif rresponse == 301 and fRedirect != rlocation:
        print(f"Status code is correct, but the returned redirect {rlocation} is incorrect for incoming URL {url}")
        print(f"The correct redirect is {fRedirect}. Please review the rules {source_hash} uploaded to EKV")
    elif rresponse == 301 and fRedirect == rlocation:
        print("All good")


def main():
    file_name = "test-delete3.xlsx"
    df = pd.read_excel(file_name, engine='openpyxl')

    # Define the number of threads
    num_threads = 4  # Example: Set this to the desired number of threads

    # Use ThreadPoolExecutor to process rows in parallel, specifying the number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process_row, df.to_dict('records'))


if __name__ == "__main__":
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    main()