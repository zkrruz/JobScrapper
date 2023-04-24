import requests
from bs4 import BeautifulSoup


def extract_max_page(url):
  request =  requests.get(url)
  soup = BeautifulSoup(request.text, 'html.parser')
  pages = soup.find("ul", {'class': 'styles-module-root-OK422'}).find_all('a')
  last_page=int(pages[-2].text)
  return last_page
  
def extract_job(html):
  title = html.find('a').text
  link_elem = html.find('a')
  if link_elem:
    link = link_elem['href']
  else:
    link = None
  location_elem = html.find('div', {'class': 'geo-root-zPwRk iva-item-geo-_Owyg'})
  location = location_elem.text if location_elem else 'Адрес не указан'
  return {'title': title, 'address': location, 'link': link}
  
  
def extract_jobs(last_page, url):
  jobs=[]
  for page in range(last_page):
    print(f'avito.ru: Парсинг страницы {page}')
    result = requests.get(f'{url}&p={page+1}')
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'iva-item-titleStep-pdebR'})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs(keyword):
  url = f'https://www.avito.ru/all/vakansii?cd=1&q={keyword}'
  max_page = extract_max_page(url)
  jobs=extract_jobs(max_page, url)
  return jobs