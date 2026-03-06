import ftplib
import threading
import time
import os

FTP_HOST = 'ftp.gnu.org'
REMOTE_DIR = '/video'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, 'webm_downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


# list all .webm files on the FTP server
def list_webm_files():
    try:
        ftp = ftplib.FTP(FTP_HOST)  #create FTP session and connect
        ftp.login()  #login with default anonymous credentials

        print(f'connected to {FTP_HOST}')
        print(ftp.getwelcome())  #welcome message from server

        ftp.cwd(REMOTE_DIR)  #change to /video directory
        print(f'current directory: {ftp.pwd()}')

        # get list of files and filter for .webm
        files = ftp.nlst()
        webm_files = [f for f in files if f.endswith('.webm')]

        print(f'\nfound {len(webm_files)} .webm files')

        ftp.quit()
        return webm_files

    except ftplib.all_errors as ftp_err:
        print(f'ftp error: {ftp_err}')
        return []
    except OSError as os_err:
        print(f'os error: {os_err}')
        return []


# download a single .webm file from the server
def download_file(filename):
    try:
        # need a new connection for each thread
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login()
        ftp.cwd(REMOTE_DIR)

        filepath = os.path.join(DOWNLOAD_DIR, filename)

        with open(filepath, 'wb') as file:
            ftp.retrbinary(f'RETR {filename}', file.write)  #download file in binary

        print(f'downloaded: {filename}')

        ftp.quit()

    except ftplib.all_errors as ftp_err:
        print(f'ftp error downloading {filename}: {ftp_err}')
    except OSError as os_err:
        print(f'os error downloading {filename}: {os_err}')


# download all .webm files using threads
def download_with_threads(files):
    start = time.perf_counter()  # start timer

    thread_list = []

    for filename in files:
        t = threading.Thread(target=download_file, args=(filename,))
        thread_list.append(t)
        t.start()

    print(f'active threads: {threading.active_count()}')
    print()

    # wait for all threads to finish
    for t in thread_list:
        t.join()

    end = time.perf_counter()  # end timer

    print(f'\ndownload completed in {round(end - start, 2)} seconds')


if __name__ == '__main__':

    print()

    # step 1: list .webm files available on the server
    print('listing .webm files from ftp.gnu.org/video')
    print()
    webm_files = list_webm_files()

    print()
    print()

    # step 2: download files using threads
    if webm_files:
        print('downloading files with threads')
        print()
        download_with_threads(webm_files)
    else:
        print('no .webm files found to download')

    print()
    print('Done!')
