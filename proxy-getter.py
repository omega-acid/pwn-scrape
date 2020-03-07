#!/usr/bin/env python 

import requests
from itertools import cycle
from random import choice
from requests import HTTPError
import warnings
from urllib3.exceptions import InsecureRequestWarning

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import asyncio
    from proxybroker import Broker

proxy_list = []
test = "test"
def read_proxy(in_file, proxy_type):
    with open(in_file) as file:
        for ip in file:
            print(f"Adding {ip} to the list of proxies to check")
            proxy_list.append(ip)
        set(proxy_list)
        print(proxy_list)

    

def check_proxy():
    proxy_pool = cycle(proxy_list)
    url = 'https://httpbin.org/ip'
    proxy = next(proxy_pool)  
    rotate = len(proxy_list)
    for i in range(rotate):
        proxy = next(proxy_pool)
        print("Request #%d"%i)
        try:
            response = requests.get(url, verify=False, proxies={"http": f"socks5://{proxy}", "https://": f"socks://104.236.62.242:1080"})
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

            print(response.text)
        except HTTPError as http_err:
            print(f"HTTP ERRROR {http_err}")

        #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
        #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
            print("Skipping. Connnection error")
read_proxy(test, "HTTPS")
check_proxy()
