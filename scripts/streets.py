import requests
from bs4 import BeautifulSoup as bs
import csv

url = 'https://geographic.org/streetview/usa/ca/san_joaquin/stockton.html'
csv_name = 'streets'

page = requests.get(url)
print(page.status_code)
soup = bs(page.text, features='lxml')
res = soup.find_all('span', class_='listspan')
streets = res[0].find_all('a')

index = 0

saved_streets = []
with open(f'data/compiled/{csv_name}.csv', 'w', newline='') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(['index', 'street'])

	print('Appending...')
	for r in streets:
		if(r.string in saved_streets):
			print('already added: ' + r.string)
		else:
			writer.writerow([index, r.string])
			index += 1
			print(r.string)
			saved_streets.append(r.string)
	print(f'Finished appending streets. {index} indices.')