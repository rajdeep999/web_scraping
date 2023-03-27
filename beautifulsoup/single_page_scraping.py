from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = 'https://subslikescript.com/movie/Firefly-3582840'
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, 'lxml')
    box = soup.find('article', class_='main-article')
    title = box.find('h1').get_text()
    script = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

    with open(f'data/{title}.txt', 'w', encoding="utf-8") as file:
        file.write(script)
