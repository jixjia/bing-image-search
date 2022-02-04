# USAGE
# python bing_image_scrape.py -q doraemon -n 500

# import the necessary packages
from requests import exceptions
import config
import argparse
import requests
import os

ap = argparse.ArgumentParser()
ap.add_argument('-q', '--query', required=True, help='search query to search Bing Image API for')
ap.add_argument('-n', '--max_items', default=20, type=int, help='maximum returned results')
args = vars(ap.parse_args())

# Exception handling
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])

# Bing Image Search API call
term = args['query']
headers = {'Ocp-Apim-Subscription-Key': config.API_KEY}
params = {'q': term, 'offset': 0, 'count': config.ITEMS_PER_PAGE}

print('[INFO] Searching Bing Image API for "{}"...'.format(term), end='')

# make the search
search = requests.get(config.ENDPOINT, headers=headers, params=params)
search.raise_for_status()

# grab results from the search, including the total number of
# estimated results returned by the Bing API
results = search.json()
totalNumItems = min(results['totalEstimatedMatches'], args['max_items'])

print(f'Found {results["totalEstimatedMatches"]} items, capped at {totalNumItems}')
if totalNumItems > 0:
	
	# initialize counter
	total = 0
	
	# initialize download container
	output_path = os.path.join('dataset', term.replace(' ','-'))

	if not os.path.exists(output_path):
		os.mkdir(output_path)

	# loop over the downloadable items paged by ITEMS_PER_PAGE
	for offset in range(0, totalNumItems, config.ITEMS_PER_PAGE):
		# update the search parameters using the current offset, then
		# make the request to fetch the results
		if totalNumItems < config.ITEMS_PER_PAGE:
			print(f'[INFO] Batch {offset}~{offset + totalNumItems} items')
		else:
			print(f'[INFO] Batch {offset}~{offset + config.ITEMS_PER_PAGE} items')
		
		params['offset'] = offset
		search = requests.get(config.ENDPOINT, headers=headers, params=params)
		search.raise_for_status()
		results = search.json()
		
		# loop over the results
		for idx, v in enumerate(results['value']):
			# try to download the image
			try:
				# make a request to download (it could be rejected by destination server)
				print('({}) Fetching: {}'.format(idx, v['contentUrl'][:80]))
				r = requests.get(v['contentUrl'], timeout=10)

				# build the path to the output image
				ext = v['contentUrl'][v['contentUrl'].rfind('.'):]
				p = os.path.sep.join([output_path, '{}{}'.format(str(total).zfill(8), ext)])

				# write the image to disk
				f = open(p, 'wb')
				f.write(r.content)
				f.close()

			# catch errors during download
			except Exception as e:
				if type(e) in EXCEPTIONS:
					print('>>> Skipping. Unable to download {}'.format(v['contentUrl'][:80]))
					continue
				
			# update the counter
			total += 1

			if total > args['max_items']:
				break

	print(f'[INFO] Downloaded {total} items in total')