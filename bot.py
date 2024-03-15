#!/usr/bin/python3
########################################
# imports
########################################
import datetime
import json
import time
import random
import re
import requests

########################################
# variables
########################################
user_agent = "Mozilla/5.0 (Windows NT 10.0; rv:123.0) Gecko/20100101 Firefox/123."

########################################
# functions
########################################
def log_message(message: str) -> str:
    """
    prints log messages in a standardized format
 
    args:
        messsage (str): the message to print
 
    returns:
        str: the timestamp then message
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - {message}")


def generate_random_delay():
    """
    generate a random delay between X and X seconds
    """
    delay = random.randint(10, 30)
    log_message(f"STATE: Waiting for {delay} seconds...")
    time.sleep(delay)


def get_page(url: str) -> tuple[int, bytes]:
    """
    gets the content of a page using the requests module
 
    args:
        url (str): the url to get
 
    returns:
        tuple[int, bytes]: a tuple containing the HTTP status code and the content of the web page
    """
    headers = {
        "User-Agent": user_agent,
    }

    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            log_message(f"STATE: HTTP status code is {page.status_code}")
            return page.status_code, page.content
        else:
            log_message(f"ERROR: HTTP status code is {page_status_code} for {url}")
            exit(1)
    except requests.RequestException as e:
        log_message(f"ERROR: Failed to fetch page content for URL '{url}': {e}")
        exit(1)


def get_item_json(html_content: bytes) -> list:
    """
    extracts JSON-like content from HTML content and parses it into a list of dictionaries

    args:
        html_content (bytes): the HTML content containing the JSON-like data

    returns:
        list: a list of dictionaries representing the parsed JSON data
    """
    # find the start and end index of the JSON-like content within <script> tags
    start_index = html_content.find(b'var products =') + len(b'var products =')
    end_index = html_content.find(b'];', start_index) + 1

    # extract the JSON-like content
    json_content = html_content[start_index:end_index]

    # remove the first and last square brackets
    json_content = json_content.strip()[1:-1]

    # remove any invalid characters before parsing as JSON
    json_content = json_content.replace(b'\n', b'').replace(b'\t', b'').replace(b'\r', b'')

    # parse the JSON-like content
    try:
        products = json.loads(json_content)
        return products
    except json.JSONDecodeError:
        log_message("ERROR: Failed to parse JSON content")
        exit(1)


def ajax_request(itemId: str, productId: str, catalogId: str) -> tuple[int, bytes]:
    headers = {
        "User-Agent": user_agent,
    }

    url = f"https://www.costco.com/AjaxGetInventoryDetail?itemId={itemId}&catalogId={catalogId}&productId={productId}&WH=any"

    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 200:
            log_message(f"STATE: HTTP status code is {page.status_code}")
            return page.status_code, page.content
        else:
            log_message(f"ERROR: HTTP status code is {page_status_code} for {url}")
            exit(1)
    except requests.RequestException as e:
        log_message(f"ERROR: Failed to fetch page content for URL '{url}': {e}")
        exit(1)


########################################
# script starts here
########################################
log_message("STATE: Starting script...")
try:
    # open the file in read mode
    with open('URLs.txt', 'r') as file:
        for line in file:
            # check if the line starts with "https://" so that we can ignore other lines with comments
            if line.startswith('https://'):
                # strip the blank characters at the beginning and end of each line
                line = line.strip()
                # to simulate not being a bot, wait a random amount of time
                generate_random_delay()
                # get the content of the page
                page_status_code, page_content = get_page(line)
                # from here, we need four things to make the API call to https://www.costco.com/AjaxGetInventoryDetail
                #   itemId
                #   productId
                #   catalogId
                #   WH (warehouse)

                # find the catalogId in a different part of the page
                page_content_str = page_content.decode('utf-8')
                pattern = r"wcs\.catalogId\s*=\s*'(\d+)'"
                match = re.search(pattern, page_content_str)
                if match:
                    catalogId = match.group(1)
                else:
                    log_message("ERROR: Catalog ID not found...")
                    exit(1)

                # get the JSON data and parse it
                json_data = get_item_json(page_content)
                for item in json_data:
                    partNumber = item.get("partNumber")
                    productName = item.get("productName")
                    itemId = item.get("catentry")
                    # the productId appears to always be the ItemId minus one
                    productId = int(itemId) - 1

                # finally, make the request to check stock
                ajax_status_code, ajax_content = ajax_request(itemId, productId, catalogId)
                print(ajax_content)
                

except FileNotFoundError:
    log_message("ERROR: File not found, exiting...")
    exit(1)
