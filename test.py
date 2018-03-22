from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 

links = []

class item:
    
    name = ''
    videoLink = ''
    imgLink = ''

    def __init__(self,name,videoLink,imgLink):
        self.name = name
        self.videoLink = videoLink
        self.imgLink = imgLink  



html = urlopen('https://meczreplay.blogspot.com/search?max-results=10')
soup = BeautifulSoup(html,'lxml')
letters = soup.find_all('a', href=True)

linksContainer = soup.find_all('div', attrs={'class' : 'container post-body entry-content'})
#imgLinks = soup.find_all('img', attrs = {'alt' : 'Obraz'})

for i in linksContainer:
    dataContainer = i.find('div', attrs={'class' : 'snippet-item r-snippetized'})
    data = str(dataContainer).replace('<div class=\"snippet-item r-snippetized\">','').replace('</div>','').replace('\n','')
    table = filter(None, re.split('<br/>|<b>|</b>|<br>|\n',str(data)))
    
    for line in table:
        indexHttp = line.find('http')
        if (indexHttp == -1):
            title = line.replace('</strong>','').replace('<strong>','')
        else: 
            name = line.split('<a href="')[0].replace(':','')
            link = line.split('<a href="')[1].split('"')[0]
            links.append ( item ( title + ' - ' + name,link , i.img['src'] ) ) 
            print(title)


            
