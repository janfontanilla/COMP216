# pip install requests
import requests
import time
import threading
import os
from requests.exceptions import HTTPError

IMAGE_URLS = [
    'https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0',
    'https://images.unsplash.com/photo-1485833077593-4278bba3f11f',
    'https://images.unsplash.com/photo-1593179357196-ea11a2e7c119',
    'https://images.unsplash.com/photo-1526515579900-98518e7862cc',
    'https://images.unsplash.com/photo-1582376432754-b63cc6a9b8c3',
    'https://images.unsplash.com/photo-1567608198472-6796ad9466a2',
    'https://images.unsplash.com/photo-1487213802982-74d73802997c',
    'https://images.unsplash.com/photo-1552762578-220c07490ea1',
    'https://images.unsplash.com/photo-1569691105751-88df003de7a4',
    'https://images.unsplash.com/photo-1590691566903-692bf5ca7493',
    'https://images.unsplash.com/photo-1497206365907-f5e630693df0',
    'https://images.unsplash.com/photo-1469765904976-5f3afbf59dfb',
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "images")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# part A: download a single file from a given URL
def download_file(url):
    try:
        response = requests.get(url)  #send a GET request to the url
        response.raise_for_status()  #raise an exception if returned an error status code
    except HTTPError as http_error:
        print(f'http error occurred: {http_error}')
    except Exception as e:
        print(f'other error occurred: {e}')
    else:
        filename = url.split('/')[-1] + '.jpg'  #extract the last part of the url to use as the filename
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)

        print(f'downloaded: {filename} to: {filepath}')


# part B: download all images sequentially and time the operation
def download_sequentially(urls):
    start = time.perf_counter()  #start the timer before downloading

    for url in urls:
        download_file(url)

    end = time.perf_counter()
    print(f'\nsequential download time: {round(end - start, 2)} seconds')


# part C: download all images using threads and time the operation
def download_with_threads(urls):
    start = time.perf_counter()  #start the timer before downloading

    thread_list = []

    for url in urls:
        t = threading.Thread(target=download_file, args=(url,))  #assign download_file as the task for each thread
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()  #wait for all threads to finish before stopping the timer

    end = time.perf_counter()
    print(f'\nthreaded download time: {round(end - start, 2)} seconds')


if __name__ == '__main__':

    print('downloading images sequentially')
    print()
    download_sequentially(IMAGE_URLS)

    print()

    print('downloading images with threads')
    print()
    download_with_threads(IMAGE_URLS)

    print()
    print('Completed')
