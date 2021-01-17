import requests
from urllib.request import urlparse, urljoin
import urllib3
from bs4 import BeautifulSoup
import colorama
import socket
import sys
import signal
import pyfiglet

# define proxies
proxies = {
  'http': 'http://127.0.0.1:8080',
  'https': 'http://127.0.0.1:8080',
}

# headers for http get requests
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

colorama.init()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(pyfiglet.figlet_format("Makdi",font='whimsy'))
print("The program is configured to send the discovered links to the proxy, posting minimal output to stdout \n\n")

get_domain = str(input("Input a URL with http/https prepended: "))

domain = urlparse(get_domain).netloc #extract domain

# variables that store final and buffer values
ilink = []
elink = []
in_links = set() #stores internal links
ex_links = set() #stores externanl links through passive discovery

def valid_url():
# url validation
    try:
        global ip
        initial = requests.get(get_domain,headers=headers,verify=False)
        print("Connected. Proceeding further \n\n")
        crawl(get_domain)
    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED, "URL not acccessible with the following error: \n\n" + str(e))
        sys.exit(0)


def crawl(url):
# converts url to parsable text and extract urls
    try:
        response = requests.get(url,headers=headers,verify=False)
        parse = BeautifulSoup(response.text , "html.parser")
        for i in parse.find_all('a'):
            link = i.get('href')
            if link.startswith(urlparse(get_domain).scheme):
                int_or_ext(link)
            elif link.startswith("https" or "http"):
                int_or_ext(link)
            else:
                link = urljoin(get_domain,link)
                int_or_ext(link)
    except:
        pass

def int_or_ext(link):
# catalogs urls as internal or external
        if domain in link:
            ilink.append(link)
            in_links.add(link)
        else:
            elink.append(link)

def consolidate():
# runs crawl on internal urls
    init = 0
    len_init = 0
    for i in ilink:
        crawl(i)
        init += 1
        if init == 120:
            len_init = len(in_links)
        elif init in range(60,360,60) and len(in_links) == len_init:
            break
        elif init in range (60,360,60) and len(in_links) > len_init:
            len_init = len(in_links)
        elif init == 5: #intentional for testing
            break
    for i in elink:
        ex_links.add(i)
    print(str(len(in_links)) + " internal links discovered. Queued to be sent to the proxy")
    print(str(len(ex_links)) + " external links passively discovered \n\n")

valid_url()

consolidate()

def export():
# provides export option in set structure for internal and external links
    print(colorama.Fore.GREEN, "Internal links discovered: \n", in_links, "\n\nExternal links passively discovered: \n", ex_links, "\n\n")

def send_to_proxy():
# send get requests through proxy
    try:
        for i in  in_links:
            requests.get(i,headers=headers,proxies=proxies,verify=False)
        print("Links succesfully sent to the proxy\n\n")
    except requests.exceptions.RequestException as e:
        export()
        print(colorama.Fore.RED, "Proxy not acccessible with the following error: \n\n" + str(e) + '\n')
        exit(0)

send_to_proxy()


if str((input("print discovered links to stdout: y/n"))) == 'y' or 'yes':
    export()
else:
    pass

