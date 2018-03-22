import urlparse
import sys,urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import resolveurl as urlresolver

#from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 

#import web_pdb; web_pdb.set_trace()
 
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

_addon = xbmcaddon.Addon()
_icon = _addon.getAddonInfo('icon')

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def resolve_url(url):
    duration=7500   #in milliseconds
    message = "Cannot Play URL"
    stream_url = urlresolver.HostedMediaFile(url=url).resolve()
    # If urlresolver returns false then the video url was not resolved.
    if not stream_url:
        dialog = xbmcgui.Dialog()
        dialog.notification("URL Resolver Error", message, xbmcgui.NOTIFICATION_INFO, duration)
        return False
    else:        
        return stream_url    

def play_video(path):
    """
    Play a video by the provided path.
    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    vid_url = play_item.getfilename()
    stream_url = resolve_url(vid_url)
    if stream_url:
        play_item.setPath(stream_url)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)

# addon kicks in

mode = args.get('mode', None)


if mode is None:
    
    links = []
    
    class item:  
        name = ''
        videoLink = ''
        imgLink = ''

        def __init__(self,name,videoLink,imgLink):
            self.name = name
            self.videoLink = videoLink
            self.imgLink = imgLink  

    html = urllib.urlopen('https://meczreplay.blogspot.com/search?max-results=50')
    soup = BeautifulSoup(html)
    letters = soup.find_all('a', href=True)

    linksContainer = soup.find_all('div', attrs={'class' : 'container post-body entry-content'})
    lin = soup.find_all('img', attrs = {'alt' : 'Obraz'})

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
                links.append(item(title + ' - ' + name ,link ,i.img['src']))


    for i in links: 
        video_play_url = i.videoLink
        url = build_url({'mode' :'play', 'playlink' : video_play_url})
        li = xbmcgui.ListItem(i.name, iconImage=i.imgLink)
        li.setProperty('IsPlayable' , 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'play':
    final_link = args['playlink'][0]
    play_video(final_link)