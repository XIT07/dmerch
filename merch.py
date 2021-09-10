import re, urllib.parse,csv ,datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup
headers = {
    'Access-Control-Allow-Origin': '*',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}
s = HTMLSession()
keyword = input("\nEnter keyword or search term :").replace(' ', '+')
NPAGE = input("\nEnter Last Number of Page :")
URLS = [f'https://www.amazon.com/s?k={el}&i=fashion-novelty&rh=p_6:ATVPDKIKX0DER&page={page}&hidden-keywords=ORCA&qid=1621510987&ref=sr_pg_{page}' for el in (keyword,) for page in (1, NPAGE)]

def geturl(url):
    r = s.get(url)
    r.html.render(timeout=8000)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return ["https://amazon.com"+p.a['href'] for p in soup.find_all('div', {'data-component-type':'s-search-result'})]
    
def getdata(url):
    r = s.get(url)
    r.html.render(timeout=8000)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    imgs = soup.find('div',{'class':'imgTagWrapper'}).find('img')['src']
    val =  re.match(r"(https:\/\/m\.\w+.*I\/)(.*\._CLa)(\|)(\\|)(\d+.*?\d+.*?)(\w+.*)(\|)",urllib.parse.unquote(imgs))
    #link,ids,dsgn = val.group(1),val.group(2),val.group(6)
    try:
        link = val.group(1)
        ids = val.group(2)
        dsgn = val.group(6)
    except:
        link = ""
        ids = ""
        dsgn = ""
    return {'title': soup.title.text.replace('Amazon.com:', '').replace(': Clothing', ''), "T-Shirt" : link+ids if link+ids+".png" else None , 'Design': link+dsgn}

urls = []
for url in URLS:
    urls.extend(geturl(url))
    
with open(""+keyword+".csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'T-Shirt', 'Design'])    
    for url in urls:
        print(f'parsing {url}')
        info = getdata(url)
        print(info)
        writer.writerow(list(info.values()))
