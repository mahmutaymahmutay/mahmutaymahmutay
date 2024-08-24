##############################################################################################
##                                                                                          ##
##  This Auxilary tool crawls given url pages and scans User Input fields ,                 ##
##   to detect HTML Injection Vulnerability                                                 ##
##                                                                                          ##
##           Author: Mahmut AY < mahmutayy@yahoo.com >                                      ##
##                                                                                          ##
##        Please run equirements_HtmlInjector.py  file first !!                             ##
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

    # The list of payloads ,we  use for testing HTML injection
  
    payloads = [
    "<h1>HTML</h1>",
    "<h1>html</h1>",
    "<h2>HTML</h2>",
    "<h3>HTML</h3>",
    "<h4>HTML</h4>",
    "<h5>HTML</h5>",
    "<h6>HTML</h6>",
    "<pre>HTML</pre>",
    "<p>HTML</p>",
    "<i>HTML</i>",
    '<a href="https://www.google.com">HTML</a>',
    '<abbr title="HTML">HTML</abbr>',
    '<acronym title="HtmlInjetionDetetor ">AI</acronym>',
    "<address>address,address</address>",
    "<article><h2>HtmlInjectionDetector </h2></article>",
    '<audio controls><source src="demo.ogg" type="audio/ogg"><source src="demo.mp3" type="audio/mpeg"></audio>',
    "<b>HTML</b>",
    "<h1>HTML</h1><!--",
    "qq<h1>HTML</h1>",
    "qq<h1>HTML</h1>qq",
    "$$\\<u>HTML</u>{}$$",
    "%3Ch1%3EHTML%3C%2Fh1%3E",
    "&lt;h1&gt;HTML&lt;/h1&gt;",
    "&#60;h1&#62;HTML&#60;/h1&#62;",
    '<iframe src="https://www.google.com" title="test"></iframe>',
    "123<h1>HTML</h1>",
    "<h1>HTML</h1>123",
    "123<h1>HTML</h1>123",
    "%253Ch1%253EHTML%253C%252Fh1%253E",
    '<iframe id="if1" src="https://www.google.com"></iframe>',
    '<iframe id="if2" src="https://www.google.com"></iframe>',
    "PGgxPkhUTUw8L2gxPg==",
    "UEdneFBraFVUVXc4TDJneFBnPT0=",
    "<<h1>HTML</h1>",
    "<<h1>HTML</h1>>",
    "<<h1>html</h1>>",
    "%253Ch1%253EHTML%253C%252Fh1%253E<h1>Html</h1>",
    "<pre>HTML</pre>",
    "<p>HTMLinjection here</p>",
    "<i>HTML</i>",
    "<u>Html</u>",
    "<mark>Html</mark>",
    '<a href="https://www.google.com">HTML</a>',
    "<b>HTML</b>",
    "<h1>HTML</h1><!--",
    "qq<h1>HTML</h1>",
    "qq<h1>HTML</h1>qq",
    "%3Ch1%3EHTML%3C%2Fh1%3E",
    "%253Ch1%253EHTML%253C%252Fh1%253E",
    "&lt;h1&gt;HTML&lt;/h1&gt;",
    "&amp;lt;h1&amp;gt;HTML&amp;lt;/h1&amp;gt;",
    "&#60;h1&#62;HTML&#60;/h1&#62;",
    '<iframe src="https://www.google.com" title="test"></iframe>',
    "123<h1>HTML</h1>",
    "<h1>HTML</h1>123",
    "123<h1>HTML</h1>123",
    "%253Ch1%253EHTML%253C%252Fh1%253E",
    '<iframe id="if1" src="https://www.google.com"></iframe>',
    '<iframe id="if2" src="https://www.google.com"></iframe>',
    "<<h1>HTML</h1>",
    "<<h1>HTML</h1>>",
    "<<h1>html</h1>>",
    "%253Ch1%253EHTML%253C%252Fh1%253E",
    "<div>HTML</div>",
    "%3Ci%3Ehtml%3C%2Fi%3E",
    "%253Ci%253Ehtml%253C%252Fi%253E",
    '<style>h1 {color:red;}</style><h1>This is a heading</h1>',
    '<textarea id="HTML" name="HTML" rows="4" cols="50">Html injected</textarea>',
    '<head><base href="https://www.google.com" target="_blank"></head>',
    '<span style="color:blue;font-weight:bold">html</span>',
    '<abbr title="HTML">HTML</abbr>',
    '<acronym title="HtmlInjetionDetetor ">AI</acronym>',
    "<address>address,address</address>",
    "<article><h2>HtmlInjetionDetetor </h2></article>",
    '<audio controls><source src="demo.ogg" type="audio/ogg"><source src="demo.mp3" type="audio/mpeg"></audio>',
    "<bdi>Html</bdi>injection",
    "<bdo dir=\"rtl\">HTML html</bdo>",
    '<blockquote cite="http://google.com">HTML Injection</blockquote>',
    "<body><h1>HTML html</h1></body>",
    "Html<br>line breaks<br>injection",
    "<button type=\"button\">Click Me!</button>",
    "<canvas id=\"myCanvas\">draw htmli</canvas>",
    "<caption>Html</caption>",
    "<cite>Html Html</cite>",
    "<code>Html</code>",
    "<colgroup><col span=\"2\" style=\"background-color:red\"></colgroup>",
    "<data value=\"21053\">test html</data>",
    '<datalist id="html"><option value="html"></datalist>',
    "<dl><dt>Html</dt></dl>",
    "<dt>Html</dt>",
    "<dd>Html</dd>",
    "<del>Html</del>",
    "<ins>Html</ins>",
    "<details><summary>HTML</summary><p>html html</p></details>",
    "<dfn>HTML</dfn>",
    "<dialog open>Html</dialog>",
    "<dialog close></dialog>",
    "<em>Html</em>",
    '<embed type="text/html" src="index.html" width="500" height="200">',
    '<fieldset><legend>hello:</legend><label for="fname">First name:</label><input type="text" id="fname" name="fname"><br><br><inputtype="submit" value="Submit"></fieldset>',
    "<figure>Html</figure>",
    "<figcaption>Html Html</figcaption>",
    "<footer>HTML html</footer>",
    '<form method="GET">Username: <input type="text" name="username" value="" /> <br />Password: <input type="password" name="passwd" value="" /> <br /><input type="submit" name="submit" value="login" /></form>',
    '<form method="POST">Username: <input type="text" name="username" value="" /> <br />Password: <input type="password" name="passwd" value="" /> <br /><input type="submit" name="submit" value="login" /></form>',
    "<head><title>html</title></head>",
    "<header>HTML html</header>",
    "<hr>html<hr>",
    '<img src="index.jpg" alt="Girl in a jacket" width="500" height="600">',
    '<input type="text" id="name" name="name">',
    "<ins>red</ins>",
    "<kbd>Ctrl</kbd>",
    'label for="html">HTML</label><br>',
    "<legend>Html</legend>",
    "<li>Html</li>",
    "<main>Html</main>",
    '<map name="workmap">Html</map>',
    '<meter id="html" value="2" min="0" max="10">2 out of 10</meter>',
    "<nav>Html</nav>",
    "<noscript>Sorry, your browser does not support Html</noscript>",
    "<ol>Html</ol>",
    '<optgroup label="Html"></optgroup>',
    '<option value="Html">Html</option>',
    "<pre>Html</pre>",
    '<progress id="html" value="32" max="100"> 32% </progress>',
    "<q>Html Html</q>",
    "<s>Only 50 tickets left</s>",
    "<samp>File not found</samp>",
    "<section>HTML</section>",
    '<select name="cars" id="cars"></select>',
    "<small>HTML rocks</small>",
    "<strong>Html</strong>",
    "<sub>Html</sub>",
    "<summary>Html</summary>",
    "<sup>Html</sup>",
    '<svg width="100" height="100"><circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" /></svg>',
    "<table><th>HTML</th><th>HTML</th></table>",
    "<time>10:10</time>",
    '<time datetime="2008-02-14 20:00">HTML</time>',
    "<ul>html</ul>",
    "<var>Html</var>"
        ]
    
    visited_urls = set()

    # Verilen URL'den başlayarak web sitesini tarayalım ve tüm formları bulalım.
    # Let's Crawl the website starting from the provided URL and find all the forms
    forms_to_scan = crawl_and_find_forms(args.url, visited_urls)

    # Bulınan tüm formları payloadlarımız ile tarayalım
    # Let's scan all found forms using defined Payloads
    scan_forms(forms_to_scan, payloads)
