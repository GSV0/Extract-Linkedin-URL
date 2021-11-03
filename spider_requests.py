"""
Multi threaded requests spider for extracting linkedin urls from any website.
Developer: Ghanshyam S. Vachhani || Email: gsvachhani7@gmail.com
required "input.xlsx" file in same directory,
"input.xlsx" file need to have column of list of web site with header name "Website"
"""


import sys
import requests
import threading
import pandas as pd
from parsel import Selector
from datetime import datetime


def control(number):

    while True:
        if threading.active_count() <= number:
            break
        else:
            log_print()
    if number == 1:
        generate_files(result, 'output')
        generate_files(error, 'error')


def generate_files(data, name):

    # Generate CSV File
    pd.DataFrame(data).to_csv(f"{name}.csv", index=False)


def search(index, url):

    try:
        response = requests.get(url, timeout=20)
        response = Selector(text=response.text)
        linkedin = ' | '.join(set(response.xpath('//a[contains(@href, "linkedin")]/@href').extract()))
        result.append({'Index': index, 'Website': url, 'Linkedin': linkedin})
    except Exception as e:
        result.append({'Index': index, 'Website': url, 'Linkedin': 'error'})
        error.append(e)


def log_print():

    # This function print logs at run time. this is print run time (time), errors and extracted results
    text = f"\rresult : {len(result)} | error : {len(error)} | time : {(datetime.now()-start_time).total_seconds()}"
    sys.stdout.flush()
    sys.stdout.write(text)


if __name__ == '__main__':

    concurrent_thread, process_chunk = 120, 1000  # <<<<<<<<<< SET PARAMETERS

    result, error, start_time = list(), list(), datetime.now()
    df = pd.read_excel('input.xlsx', engine='openpyxl')
    websites = list(enumerate(df['Website']))

    for website in websites[:process_chunk]:
        threading.Thread(target=search, args=website).start()
        control(concurrent_thread)
        log_print()

    control(1)
