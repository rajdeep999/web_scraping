from bs4 import BeautifulSoup
import requests
import time

root = "https://subslikescript.com/"
letter = 'B'
url = root + 'movies_letter-'+letter
response = requests.get(url)

soup = BeautifulSoup(content, 'lxml')

pagination = soup.find('ul', class_='pagination')
page_count = pagination.find_all('li')
page_count = int(page_count[-2].text)

for page in range(1, page_count):
    time.sleep(5)
    url = root + 'movies_letter-' + letter + '?page=' + str(page)
    print(url)
    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='main-article')

    movies = box.find('ul', class_='scripts-list')
    movie_list = movies.find_all('a', href=True)
    for movie in movie_list:
        movie_url = root+movie['href']
        response = requests.get(movie_url)
        content = response.text
        soup = BeautifulSoup(content, 'lxml')

        box = soup.find('article', class_='main-article')
        title = box.find('h1').get_text()
        script = box.find('div', class_='full-script').get_text(strip=True, separator=' ')
        title = "".join(x for x in title if x.isalnum() or x == ' ')
        with open(r'data/{0}.txt'.format(title), 'w', encoding="utf-8") as file:
            file.write(script)

