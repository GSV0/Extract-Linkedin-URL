"""
Selenium spider for extracting linkedin urls links from any website.
Developer: Ghanshyam S. Vachhani || Email: gsvachhani7@gmail.com
required "input.xlsx" file in same directory,
"input.xlsx" file need to have column of list of web site with header name "Website"
"""


import pandas as pd
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def generate_files(data, name):

    # Generate CSV File
    pd.DataFrame(data).to_csv(f"{name}.csv", index=False)


def chrome_search(index, url):

    try:
        driver.get(url)
        response = Selector(text=driver.page_source)
        linkedin = ' | '.join(set(response.xpath('//a[contains(@href, "linkedin")]/@href').extract()))
        results = {'index': index, 'Website': url, 'Linkedin': linkedin}
    except Exception as e:
        results = {'index': index, 'Website': url, 'Linkedin': 'error'}
        error.append(e)
    return results


if __name__ == '__main__':

    df = pd.read_excel('input.xlsx', engine='openpyxl')
    website_urls = list(df['Website'])

    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)

    result, error = list(), list()
    df = pd.read_excel('input.xlsx', engine='openpyxl')
    websites = list(enumerate(df['Website']))

    for website in websites[:10]:
        result.append(chrome_search(website[0], website[1]))
    generate_files(result, 'output')