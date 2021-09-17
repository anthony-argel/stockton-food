import json
import csv
import os

if(os.path.exists('data/compiled') == False):
	os.mkdir('data/compiled')

# take json file and turn it into csv
def compile_json(filename):
	with open(f'data/{filename}.json', 'r') as json_file:
		data = json.load(json_file)

		mode = 'w'
		if(os.path.exists(f'data/compiled/food.csv')):
			mode = 'a'
		with open(f'data/compiled/food.csv', mode = mode, newline='', encoding= 'utf-8') as csv_file:
			writer = csv.writer(csv_file)
			headers = ['id', 'name','image_url', 'is_closed','url','review_count','categories','rating','latitude','longitude','address1','address2','phone_no']
			if (mode == 'w'):
				writer.writerow(headers)
			for biz in data['businesses']:
				row = []
				row.append(biz['id'])
				row.append(biz['name'].replace(',', ''))
				row.append(biz['image_url'])
				row.append(biz['is_closed'])
				row.append(biz['url'])
				row.append(biz['review_count'])
				categories = ''
				for i in biz['categories']:
					categories += i['title'] + ' '
				row.append(categories)
				row.append(biz['rating'])
				row.append(biz['coordinates']['latitude'])
				row.append(biz['coordinates']['longitude'])
				if(isinstance(biz['location']['address1'], str)):
					row.append(biz['location']['address1'].replace(',',''))
				else:
					row.append(biz['location']['address1'])
				address = ''
				for i in biz['location']['display_address']:
					address += i + ' '
				address = address.replace(',', '')
				row.append(address)
				row.append(biz['phone'])
				writer.writerow(row)

def compile_multiple(name_base, range_start, range_end):
	for i in range(range_start,range_end):
		compile_json(f'{name_base}{i}')

def compile_categories():
	categories = []

	for i in range(0, 14):
		filename = f'data/food{i}.json'
		with open(filename, 'r') as json_file:
			data = json.load(json_file)

			for biz in data['businesses']:
				for cat in biz['categories']:
					categories.append(cat['title'])

	#print(categories)
	#print("Number of categories found: " + str(len(categories)))
	#print("Number of UNIQUE categories found: " + str(len(set(categories))))

	unique_categories = set(categories)

	with open('data/compiled/categories.csv', 'w', newline='',encoding='utf-8') as f:
		writer = csv.writer(f)
		headers = ['id', 'name']
		counter = 0
		writer.writerow(headers)
		for i in unique_categories:
			writer.writerow([counter, i.replace(',','' )])
			counter += 1

def create_relationship_table():
	relationships = []
	categories = []

	with open('data/compiled/categories.csv', 'r', newline='') as csv_file:
		csv_reader = csv.reader(csv_file)
		skipped_header = False
		for row in csv_reader:
			if(skipped_header == False):
				skipped_header = True
			else:
				print(row[1])
				categories.append(row[1])

	relationship_id = 0

	print(categories.index('Sushi Bars'))
	print(categories[categories.index('Sushi Bars')])

	for i in range(0, 14):
		filename = f'data/food{i}.json'
		with open(filename, 'r') as json_file:
			data = json.load(json_file)

			for biz in data['businesses']:
				for cat in biz['categories']:
					# create array here
					# id, rest_id, cat_id
					relationships.append([relationship_id, biz['id'], categories.index(cat['title'].replace(',',''))])
					relationship_id += 1

	with open('data/compiled/relationships.csv', 'w', newline='', encoding='utf-8') as csv_file:
		writer = csv.writer(csv_file)
		headers = ['id', 'restaurant_id','category_id']
		writer.writerow(headers)
		for relationship in relationships:
			writer.writerow(relationship)

