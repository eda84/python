#!python3
# multidownloadXkcd.py - Download XKCD comic in multi thread

import requests
import os
import threading
import bs4

os.makedirs('xkcd', exist_ok=True)  # Save comic in ./xkcd


def download_xkcd(start_comic, end_comic):
    for url_number in range(start_comic, end_comic):
        # Download the page

        print('Dwonloading page http://xkcd.com/{}...'.format(url_number))
        res = requests.get('http://xkcd.com/{}'.format(url_number))
        res.raise_for_status

        soup = bs4.BeautifulSoup(res.text)

        # Find the URL the comic image
        comic_elem = soup.select('#comic img')
        if comic_elem == []:
            print('Comic image not found')
        else:
            comic_url = 'http:' + comic_elem[0].get('src')
            # Download the image
            print('Downloading image {}...'.format(comic_url))
            res = requests.get(comic_url)
            res.raise_for_status

            # Save the image in ./xkcd
            image_file = open(os.path.join('xkcd', os.path.basename(comic_url)), 'wb')
            for chunk in res.iter_content(100000):
                image_file.write(chunk)
            image_file.close()

# Generate and start Thread object
download_threads = []

download_xkcd(1, 2)

for i in range(1, 1400, 100):
    download_thread = threading.Thread(target=download_xkcd, args=(i, i + 100))
    download_threads.append(download_thread)
    download_thread.start()

# Wait for all threads to finish
for download_thread in download_threads:
    download_thread.join()

print('Finish')
