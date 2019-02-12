#import urlparse
import sys,urllib
#import sys,urllib.request
#import xbmc, xbmcgui, xbmcaddon, xbmcplugin
#import resolveurl as urlresolver
from bs4 import BeautifulSoup
#import BeautifulSoup
import re 


class item:  
    name = ''
    videoLink = ''
    imgLink = ''

    def __init__(self,name,videoLink,imgLink):
        self.name = name
        self.videoLink = videoLink
        self.imgLink = imgLink  

class webParser:   
    def getData(self):
        #html = urllib.request.urlopen('https://meczreplay.blogspot.com/search?max-results=50')
        html = urllib.urlopen('https://meczreplay.blogspot.com/search?max-results=50')
        soup = BeautifulSoup(html) 
        #soup = BeautifulSoup(html,"lxml") 

        linksContainer = soup.find_all('div', attrs={'class' : 'container post-body entry-content'}) 
        
        self.links = []
        for i in linksContainer:
            dataContainer = i.find('div', attrs={'class' : 'snippet-item r-snippetized'})
            data = str(dataContainer).replace('<div class=\"snippet-item r-snippetized\">','').replace('</div>','').replace('\n','')
            table = filter(None, re.split('<br/>|<b>|</b>|<br>|\n',str(data)))
    
            for line in table:
                indexHttp = line.find('http')
                if (indexHttp == -1):
                    title = line.replace('</strong>','').replace('<strong>','')
                else:
                    try:
                        name = line.split('<a href="')[0].replace(':','')
                        link = line.split('<a href="')[1].split('"')[0]
                        self.links.append(item(title + ' - ' + name ,link ,i.img['src']))
                    except:
                        pass 
        return self.links
