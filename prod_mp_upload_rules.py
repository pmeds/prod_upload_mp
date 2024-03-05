import csv
import json
import requests
import sys
import warnings
import urllib3
from concurrent.futures import ThreadPoolExecutor


requests.packages.urllib3.disable_warnings()
# Function to send POST request
def send_post_request(row):
    json_data = json.dumps(row)
    print(json_data)
    url = 'https://paulm-sony.test.edgekey.net/upload'
    headers = {"Content-type": "application/json"}
    response = requests.post(url, data=json_data, headers=headers, verify=False)
    rheaders = response.headers
    rresponse = response.status_code
    print(rresponse, rheaders)

def main(file_name):
    if file_name:
        reader = csv.DictReader(open(file_name))
        rows = list(reader)  # Convert iterator to list to reuse it

        # Define the number of threads
        num_threads = 4  # Example: Set this to the desired number of threads

        # Use ThreadPoolExecutor to send POST requests in parallel
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(send_post_request, rows)

if __name__ == "__main__":
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')

    # Check if argument was passed
    if len(sys.argv) < 2:
        print('No file provided, no rules to upload')
        sys.exit()
    else:
        file_name = sys.argv[1]
        main(file_name)
