import random
import requests
from fake_useragent import UserAgent
from app import config

def get_ip(proxies=None):
    if not proxies:
        return requests.get("http://httpbin.org/ip").text
    else:
        return requests.get("http://httpbin.org/ip", proxies=proxies).text
def get_new_proxies(): 
    host, port = config.get_tor_config()
    session = requests.session()
    creds = str(random.randint(10000,0x7fffffff)) + ":" + "foobar"
    # session.proxies = {'http': 'socks5h://{}@{}:{}'.format(creds, host, port), 'https': 'socks5h://{}@{}:{}'.format(creds, host, port)}
    host = "176.214.99.101:1256"
    port = "8080"
    session.proxies = {'http': host, 'https': host}
    # r = session.get('http://httpbin.org/ip')
    return session.proxies

def get_random_ua():
    return UserAgent().random