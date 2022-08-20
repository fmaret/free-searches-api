import requests 
from bs4 import BeautifulSoup

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
}


def google(q):
    response = requests.get(f'https://www.google.com/search?q={q}', headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    return soup

result = google('"apple"')
print(result.find("h3"))
