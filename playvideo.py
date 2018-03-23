import urlparse
import sys,urllib
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import resolveurl as urlresolver
from bs4 import BeautifulSoup
import re 

import resources.lib.mr_parser
import resources.lib.meczreplay

import web_pdb; web_pdb.set_trace()
 
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
    
    data = resources.lib.mr_parser.meczreplay()
    
    parser = resources.lib.meczreplay.webParser()
    data2 = parser.getData()

    for i in data2: 
        video_play_url = i.videoLink
        url = build_url({'mode' :'play', 'playlink' : video_play_url})
        li = xbmcgui.ListItem(i.name, iconImage=i.imgLink)
        li.setProperty('IsPlayable' , 'true')
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

    xbmcplugin.endOfDirectory(addon_handle)


elif mode[0] == 'play':
    final_link = args['playlink'][0]
    play_video(final_link)