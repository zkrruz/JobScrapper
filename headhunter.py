import requests
from bs4 import BeautifulSoup

ITEMS = 100


headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept_Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
  }

def extract_max_page(url):
  request = requests.get(url, headers = headers)
  soup = BeautifulSoup(request.text, 'html.parser')
  pages = []
  paginator = soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
  for page in paginator:
    pages.append(int(page.find('a').text))
  return pages[-1]

def extract_job(html):
  title=html.text
  link_elem = html.find('a')
  if link_elem:
    link = link_elem['href']
  else:
    link = None
  location_elem = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
  location = location_elem.text if location_elem else 'Адрес не указан'
  return {'title': title, 'location': location, 'link': link}
  
def extract_jobs(last_page, url):
  jobs=[]
  for page in range(last_page):
    print(f'hh.ru: Парсинг страницы {page}')
    result = requests.get(f'{url}&page={page}', headers=headers)
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('a', {'class': 'serp-item__title'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(keyword):
  url = f'https://hh.ru/search/vacancy?text={keyword}&items_on_page={ITEMS}'
  max_page = extract_max_page(url)
  jobs = extract_jobs(max_page, url)
  return jobs