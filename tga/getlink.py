from bs4 import BeautifulSoup
import requests

data = requests.get('https://muhajeer.com/watch/ckv9Vi99YQd6cP5')

soup = BeautifulSoup(data.text, 'html.parser')
print(soup.find(attrs={"data-quality": "240p"})['src'])
print(soup.select('#my-video'))