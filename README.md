# Bing Image Search Client Utility
A client utility for scraping large sum of images using Bing Search.    
Simplys supply the search query and number of batches to download, let the program handles the rest.

## What does it do

* The porgram finds and downloads images based on your search query from Bing Search
* Access to some public images may be rejected by the hosting server. This program will skip downloading those images
* You can control number of image batches to download per query

![](screenshot.jpg)
## Instruction

1. Get Bing Search API (v7) here: https://www.microsoft.com/en-us/bing/apis/pricing
2. Set it up in the `config.py`
3. Run `python bing_image_search.py -q 'YOUR QUERY' -n NUM_OF_IMAGES` to scrape and download

