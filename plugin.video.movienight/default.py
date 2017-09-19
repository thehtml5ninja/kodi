import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,base64
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.movienight'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
ADDON2=xbmcaddon.Addon(id='plugin.video.movienight')
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('New Releases','http://movienight.ws/',1,icon,'',fanart)
        addDir2('Drama','http://movienight.ws/category/drama/',4,icon,'',fanart)
        addDir2('Action','http://movienight.ws/category/Action/',4,icon,'',fanart)
        addDir2('Thriller','http://movienight.ws/category/Thriller/',4,icon,'',fanart)
        addDir2('Crime','http://movienight.ws/category/Crime/',4,icon,'',fanart)
        addDir2('Mystery','http://movienight.ws/category/Mystery/',4,icon,'',fanart)
        addDir2('Science Fiction','http://movienight.ws/category/science-fiction/',4,icon,'',fanart)
        addDir2('Fantasy','http://movienight.ws/category/Fantasy/',4,icon,'',fanart)
        addDir2('Comedy','http://movienight.ws/category/Comedy/',4,icon,'',fanart)
        addDir2('Horror','http://movienight.ws/category/Horror/',4,icon,'',fanart) 
        xbmc.executebuiltin('Container.SetViewMode(50)')
               
def GETMOVIES(url,name):
        metaset = selfAddon.getSetting('enable_meta')
        link = open_url(url)
        match=re.compile('<a href="(.+?)"><img width=".+?" height=".+?" src=".+?" class=" wp-post-image" alt="post image" title="&lt;div class=&quot;home_post_content&quot;&gt;&lt;div class=&quot;in_title&quot;&gt;(.+?)&lt').findall(link)
        for url,name in match:
            if 'Series' not in name:
                name=cleanHex(name)
                if metaset=='false':
                        addDir(name,url,100,icon,len(match),isFolder=False)
                else: addDir(name,url,100,'',len(match),isFolder=False)
        match=re.compile('<a href="(.+?)"><img src="http://movienight.ws/wp-content/themes/gridthemeresponsive/images/loading-button.png"/></a>').findall(link)
        for np in match:
                 addDir2('Next Page>>>',np,1,icon,'',fanart)       
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def GETGENRES(url,name):
        metaset = selfAddon.getSetting('enable_meta')
        link = open_url(url)
        match=re.compile('<a href="(.+?)"><img width=".+?" height=".+?" src=".+?" class=" wp-post-image" alt="post image" title="&lt;div class=&quot;home_post_content&quot;&gt;&lt;h4&gt;&lt;a href=&quot;.+?&quot;&gt;(.+?)&lt;/a&gt;&lt;/h4&gt;&lt;p&gt;').findall(link)
        for url,name in match:
            if 'Series' not in name:
                name=cleanHex(name)
                if metaset=='false':
                        addDir(name,url,100,icon,len(match),isFolder=False)
                else: addDir(name,url,100,'',len(match),isFolder=False)
        match=re.compile('<a href="(.+?)"><img src="http://movienight.ws/wp-content/themes/gridthemeresponsive/images/loading-button.png"/></a>').findall(link)
        for np in match:
                 addDir2('Next Page>>>',np,4,icon,'',fanart)
                 
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))


def PLAYLINK(name,url,iconimage):
        link = open_url(url)
        try:    
                codedlink=re.compile("onClick=\"javascript:replaceb64Text\('b64block-.+?-1', '(.+?)'").findall(link)[0]
                decodedlink = base64.b64decode(codedlink)
                url=re.compile('src=\&quot\;(.+?)\&quot').findall(decodedlink)[0]
        except:
                url=re.compile('<iframe src="(.+?)" frameborder').findall(link)[0]
        link = open_url(url)
        stream_url=re.compile('<source src="(.+?)"').findall(link)[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
        return param

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

def addDir2(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true':
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            meta = metaget.get_meta('movie', simplename ,simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels= meta )
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON2.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON2.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GENRES(url)
elif mode==4: GETGENRES(url,name)
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

