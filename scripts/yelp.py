from dotenv import load_dotenv
import os
import requests
import json
import csv

load_dotenv()

# https://www.yelp.com/developers/documentation/v3/get_started
# https://spectralops.io/blog/yelp-api-guide/
base = 'https://api.yelp.com/v3'
headers = {
	"Authorization": "Bearer " + os.getenv("YELP_KEY")
}
default_location = "Stockton, CA"

def save_to_file(filename, data):
	counter = 0
	while(os.path.exists(f'data/{filename}{counter}.json')):
		counter += 1
	path = f'data/{filename}{counter}.json'
	with open(path, 'w') as f:
		json.dump(data, f)

def search_business(query):
	path = '/businesses/search?'
	url = base + path + query
	print(url)
	page = requests.get(url, headers=headers)
	data = page.json()
	save_to_file('food',data)

for i in range(0,15):
	search_business(f'categories=restaurants&location=Stockton,CA&limit=50&offset={50*i}')