import requests
import bs4
import json
import fake_headers

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'

def get_headers():
    return fake_headers.Headers(browser='chrom', os='win').generate()


def get_text(url):
    res = requests.get(url, headers=get_headers())
    if res.status_code != 404:
        return res.text
    
def parse_tags():
    soup = bs4.BeautifulSoup(get_text(HOST), features="html.parser")
    vacancy_tags = soup.find_all('div', class_='serp-item')
    vacancies = []
    for vacancy in vacancy_tags:
        link = vacancy.find('a', class_='serp-item__title')['href']
        try:
            salary = vacancy.find('span', class_='bloko-header-section-3').text.replace(u'\u202F', ' ')
        except AttributeError:
            salary = 'Не указана'
        company = vacancy.find('div', class_='vacancy-serp-item__meta-info-company').text.replace('\xa0', ' ')
        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]
        res = get_text(link)
        description = bs4.BeautifulSoup(res, features="html.parser").find(class_='g-user-content').text
        if 'Django' in description or 'Flask' in description:
            vacancies.append({
                'link': link,
                'company': company,
                'city': city
            })

    return vacancies

def write_json(vacancy_list):
    with open('vacancies.json', 'w', encoding='utf-8') as data:
        json.dump(vacancy_list, data, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    result_list = parse_tags()
    write_json(result_list)







