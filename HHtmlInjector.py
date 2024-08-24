##############################################################################################
##                                                                                          ##
##  This Auxilary tool crawls given url pages and scans User Input fields ,                 ##
##   to detect HTML Injection Vulnerability                                                 ##
##                                                                                          ##
##   Author: Mahmut AY < mahmutayy@yahoo.com >                                              ##
##                                                                                          ##
##             USAGE:  HHtmlInjector.py  <url>                                              ##  
##                                                                                          ##
##             This is only for educational purposes usage                                  ##
##       !!  Do not attempt to violate the laws with anything contained here. !!!           ##
############################################################################################## 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def crawl_and_find_forms(url, visited, depth=0, max_depth=5):
    
    forms_found = []

    # Check if we've reached the maximum depth
    if depth > max_depth:
        return forms_found

    try:
        # Check if we've already visited this URL
        if url in visited:
            return forms_found

        # Mark this URL as visited
        visited.add(url)

        print(Fore.YELLOW + f"Crawling page: {url}")  # Print each page URL being crawled in yellow

        # Send a GET request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Check if the response is HTML before parsing
        if 'text/html' not in response.headers.get('Content-Type', ''):
            print(Fore.YELLOW + f"Skipping non-HTML content: {url}")
            return forms_found

        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all forms in the page
        forms = soup.find_all('form')
        for form in forms:
            forms_found.append((url, form))

        # Find all links on the page to continue crawling
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            next_url = urljoin(url, href)
            # Ensure we only crawl URLs on the same domain
            if is_same_domain(url, next_url):
                forms_found.extend(crawl_and_find_forms(next_url, visited, depth + 1, max_depth))

    except requests.RequestException as e:
        print(f"Error: Could not connect to {url}. Details: {e}")

    return forms_found

def scan_forms(forms, payloads):
    
    print("\nAll form field scan tests are being started...")  # Informational message before scanning

    for base_url, form in forms:
        form_action = form.get('action') or base_url  # Use the action or the base URL if no action is specified
        form_action = urljoin(base_url, form_action)  # Combine base URL with form action to handle relative URLs
        form_method = form.get('method', 'get').lower()  # Default to GET if no method is specified

        for input_tag in form.find_all('input'):
            input_name = input_tag.get('name')
            if input_name:
                for payload in payloads:
                    form_data = {input_name: payload}  #Her girdi alanını tek tek test edelim / Test each input field one at a time

                    try:
                        # Send a request based on the form method
                        if form_method == 'post':
                            test_response = requests.post(form_action, data=form_data)
                        else:
                            test_response = requests.get(form_action, params=form_data)

                        # Check if the payload appears in the response content
                        if payload in test_response.text:
                            print(Fore.RED + f"[+] Potential HTML injection vulnerability found in form with action '{form_action}' for input '{input_name}' using payload: {payload}")
                        else:
                            print(Fore.GREEN + f"[-] No HTML injection vulnerability found in form with action '{form_action}' for input '{input_name}' using payload: {payload}")

                    except requests.RequestException as e:
                        print(f"Error: Could not connect to {form_action}. Details: {e}")

def is_same_domain(base_url, new_url):
    
    base_domain = urlparse(base_url).netloc
    new_domain = urlparse(new_url).netloc
    return base_domain == new_domain

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Crawl a website and scan for HTML injection vulnerabilities in input fields using multiple payloads.')
    parser.add_argument('url', type=str, help='The base URL of the website to crawl and scan.')

    args = parser.parse_args()

    # Define a list of payloads to use for testing HTML injection
    payloads = [
        "<script>alert('HTML Injection 1');</script>",
        "<img src=x onerror=alert('HTML Injection 2')>",
        "<b>bold text</b>",
        "\"'><script>alert('HTML Injection 3');</script>"
    ]

    
    visited_urls = set()

    # Verilen URL'den başlayarak web sitesini tarayalım ve tüm formları bulalım.
    # Let's Crawl the website starting from the provided URL and find all the forms
    forms_to_scan = crawl_and_find_forms(args.url, visited_urls)

    # Bulınan tüm formları payloadlarımız ile tarayalım
    # Let's scan all found forms using defined Payloads
    scan_forms(forms_to_scan, payloads)
