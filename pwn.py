#!/usr/bin/env python 

import sys
from bs4 import BeautifulSoup
import argparse
import cfscrape
from requests.exceptions import HTTPError
import lxml
from random import choice
from time import sleep

breach_index = {}
version = "1.1.1"

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--email", help="Email to search haveibeenpwned")
parser.add_argument("-l", "--list", help="file with emails to search haveibeenpwned, RATE LIMITED!")
parser.add_argument("-p", "--proxy", help="HTTP/HTTPS Proxy to use")
parser.add_argument("-v", "--version", help="Printse the version")
parser.add_argument("-d", "--delay", default=10)
args = parser.parse_args()
email = args.email
int(args.delay)

ua = {
  "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
}


def filter():
    pass

def get_page(input_email):
    breach_list = []
    try:
        url = f"https://haveibeenpwned.com/account/{input_email}"
        scraper = cfscrape.create_scraper()
        r = scraper.get(url, headers=ua).content
        soup = BeautifulSoup(r, "lxml")
        results = soup.find_all('span', {'class' : 'pwnedCompanyTitle'})
        for breach in results:
            if breach is not None:
                line = breach.text.replace(":", "")
                breach_list.append(line)
                breach_index[input_email] = breach_list
            else:
                info = f"{input_email} is not pwned"
                print(info)
                breach_index[input_email] = "Not pwned"
            if args.email != None:
                print(f"{input_email}:{line}")

    except HTTPError as http_error:
        print(http_error)
def output():
    for email, breach in dict.items(breach_index):
        print(f"________________\n\n{email.rstrip()}:\n________________\n")
        for breach in breach_index.get(email):
            print(breach)

def main():
    if args.email != None:
        get_page(args.email.rstrip())
    if args.list != None:
        with open(args.list) as email_list:
            for line in email_list:
                if len(line.strip()) == 0 :
                    print('empty line, skipping')
                    break
                else:
                    get_page(line.rstrip())
                    output()
                    sleep(3)

main()
