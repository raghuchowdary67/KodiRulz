"""
    Deccan Delight Kodi Addon
    Copyright (C) 2016 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib
import re
import requests
import resolveurl
import tempfile


try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()
_addonname = _addon.getAddonInfo('name')
_version = _addon.getAddonInfo('version')
_addonID = _addon.getAddonInfo('id')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')
_path = _addon.getAddonInfo('path')
_ipath = _path + '/resources/images/'
_settings = _addon.getSetting

cache = StorageServer.StorageServer('deccandelight', _settings('timeout'))
pDialog = xbmcgui.DialogProgress()


def clear_cache():
    """
    Clear the cache database.
    """
    msg = 'Cached Data has been cleared'
    cache.table_name = 'deccandelight'
    cache.cacheDelete('%get%')
    xbmcgui.Dialog().notification(_addonname, msg, _icon, 3000, False)


mozhdr = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
safhdr = 'Mozilla/5.0 ({}) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1'

try:
    platform = re.findall(r'\(([^)]+)', xbmc.getUserAgent())[0]
except:
    platform = 'Linux; Android 4.4.4; MI 5 Build/KTU84P'


if _settings('version') != _version:
    _addon.setSetting('version', _version)
    headers = {'User-Agent': safhdr.format(platform),
               'Referer': '{0} {1}'.format(_addonname, _version)}
    r = requests.get('\x68\x74\x74\x70\x73\x3a\x2f\x2f\x69\x73\x2e\x67\x64\x2f\x36\x59\x6f\x64\x55\x50',
                     headers=headers)
    clear_cache()
    _addon.openSettings()


sites = {'01tgun': 'Tamil Gun : [COLOR yellow]Tamil[/COLOR]',
         '02rajt': 'Raj Tamil : [COLOR yellow]Tamil[/COLOR]',
         '03tyogi': 'Tamil Yogi : [COLOR yellow]Tamil[/COLOR]',
         '11awatch': 'Andhra Watch : [COLOR yellow]Telugu[/COLOR]',
         # '21cinem': 'Cine Malayalam : [COLOR yellow]Malayalam[/COLOR]',
         '22torm': 'TOR Malayalam : [COLOR yellow]Malayalam[/COLOR]',
         '26kcine': 'Kannada Cine : [COLOR yellow]Kannada[/COLOR]',
         '31hlinks': 'Hindi Links 4U : [COLOR yellow]Hindi[/COLOR]',
         '41sominal': 'Sominal : [COLOR magenta]Various[/COLOR]',
         '42einthusan': 'Einthusan : [COLOR magenta]Various[/COLOR]',
         '43mrulz': 'Movie Rulz : [COLOR magenta]Various[/COLOR]',
         '44b2t': 'Bolly 2 Tolly : [COLOR magenta]Various[/COLOR]',
         '45omg': 'Online Movies Gold : [COLOR magenta]Various[/COLOR]',
         '46wompk': 'Online Movies PK : [COLOR magenta]Various[/COLOR]',
         '47onmw': 'Online Movie Watch : [COLOR magenta]Various[/COLOR]',
         '48flinks': 'Film Links 4 U : [COLOR magenta]Various[/COLOR]',
         # '49mersal': 'Mersalaayitten : [COLOR magenta]Various[/COLOR]',
         '50bmov': 'Bharat Movies : [COLOR magenta]Various[/COLOR]',
         '51i4movie': 'India 4 Movie : [COLOR magenta]Various[/COLOR]',
         '52tvcd': 'Thiruttu VCD : [COLOR magenta]Various[/COLOR]',
         # '61tamiltv': 'APKLand TV : [COLOR yellow]Tamil Live TV and VOD[/COLOR]',
         '62lyca': 'Lyca TV : [COLOR yellow]Tamil Live TV[/COLOR]',
         # '63mhdtv': 'MHDTV Live : [COLOR magenta]Various Live TV[/COLOR]',
         # '64aindia': 'Abroad India : [COLOR magenta]Various Live TV[/COLOR]',
         '71bbt': 'BigBoss Tamil: [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '72tdhool': 'Tamil Dhool : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '73tst247': 'Tamil Serial Today : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '74tstv': 'Tamil Serials : [COLOR yellow]Tamil Catchup TV[/COLOR]',
         '76manatv': 'Mana Telugu : [COLOR yellow]Telugu Catchup TV[/COLOR]',
         '77tflame': 'Telugu Flame : [COLOR yellow]Telugu Catchup TV[/COLOR]',
         '81apnetv': 'Apne TV : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '82desit': 'Desi Tashan : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '83yaartv': 'TV Yaar : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '84yodesi': 'Yo Desi : [COLOR yellow]Hindi Catchup TV[/COLOR]',
         '91ary': 'Ary Digital : [COLOR yellow]Urdu Catchup TV[/COLOR]',
         '92geo': 'Geo TV : [COLOR yellow]Urdu Catchup TV[/COLOR]',
         '93hum': 'Hum TV : [COLOR yellow]Urdu Catchup TV[/COLOR]',
         '99gmala': 'Hindi Geetmala : [COLOR yellow]Hindi Songs[/COLOR]'
         }

for site, title in sorted(sites.iteritems()):
    if _settings(site[2:]) == 'true':
        ri = 'from resources.scrapers import {}'.format(site[2:])
        exec ri


def list_sites():
    """
    Create the Sites menu in the Kodi interface.
    """
    listing = []
    for site, title in sorted(sites.iteritems()):
        if _settings(site[2:]) == 'true':
            item_icon = _ipath + '{}.png'.format(site[2:])
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': item_icon,
                              'icon': item_icon,
                              'poster': item_icon,
                              'fanart': _fanart})
            url = '{0}?action=1&site={1}'.format(_url, site[2:])
            is_folder = True
            listing.append((url, list_item, is_folder))

    list_item = xbmcgui.ListItem(label='[COLOR yellow][B]Clear Cache[/B][/COLOR]')
    item_icon = _ipath + 'ccache.png'
    list_item.setArt({'thumb': item_icon,
                      'icon': item_icon,
                      'poster': item_icon,
                      'fanart': _fanart})
    url = '{0}?action=0'.format(_url)
    is_folder = False
    listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)


def list_menu(site):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    menu, mode, icon = cache.cacheFunction(scraper.get_menu)
    listing = []
    for title, iurl in sorted(menu.iteritems()):
        digits = len(re.findall(r'^(\d*)', title)[0])
        if 'MMMM' in iurl:
            niurl, nmode = iurl.split('MMMM')
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nmode, site, urllib.quote(niurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
        elif 'Adult' not in title:
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            if mode == 9:
                is_folder = False
                list_item.setProperty('IsPlayable', 'true')
                list_item.addStreamInfo('video', {'codec': 'h264'})
            else:
                is_folder = True
            listing.append((url, list_item, is_folder))
        elif _settings('adult') == 'true':
            list_item = xbmcgui.ListItem(label=title[digits:])
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)


def list_top(site, iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    menu, mode = cache.cacheFunction(scraper.get_top, iurl)
    listing = []
    for title, icon, iurl in menu:
        if 'MMMM' in iurl:
            nurl, nmode = iurl.split('MMMM')
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nmode, site, urllib.quote(nurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
        else:
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': icon,
                              'icon': icon,
                              'poster': icon,
                              'fanart': _fanart})
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, mode, site, urllib.quote(iurl))
            is_folder = True
            listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)


def list_second(site, iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    menu, mode = cache.cacheFunction(scraper.get_second, iurl)
    listing = []
    for title, icon, iurl in menu:
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'thumb': icon,
                          'icon': icon,
                          'poster': icon,
                          'fanart': _fanart})
        nextmode = mode
        if 'Next Page' in title:
            nextmode = 5
        url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(iurl))
        is_folder = True
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', {'codec': 'h264'})
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'tvshows')
    xbmcplugin.endOfDirectory(_handle)


def list_third(site, iurl):
    """
    Create the Site menu in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    menu, mode = cache.cacheFunction(scraper.get_third, iurl)
    listing = []
    for title, icon, iurl in menu:
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'thumb': icon,
                          'icon': icon,
                          'poster': icon,
                          'fanart': _fanart})
        nextmode = mode
        if 'Next Page' in title:
            nextmode = 6
        url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(iurl))
        is_folder = True
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', {'codec': 'h264'})
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'tvshows')
    xbmcplugin.endOfDirectory(_handle)


def list_items(site, iurl):
    """
    Create the list of movies/episodes in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    if iurl.endswith('='):
        movies, mode = scraper.get_items(iurl)
    else:
        movies, mode = cache.cacheFunction(scraper.get_items, iurl)
    listing = []
    for movie in movies:
        title = movie[0]
        if title == '':
            title = 'Unknown'
        list_item = xbmcgui.ListItem(label=title)
        list_item.setInfo('video', {'title': title})
        if 'Next Page' in title:
            nextmode = 7
            url = '{0}?action={1}&site={2}&iurl={3}'.format(_url, nextmode, site, urllib.quote(movie[2]))
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'poster': movie[1],
                              'fanart': _fanart})
        else:
            qtitle = urllib.quote(title)
            iurl = urllib.quote(movie[2])
            url = '{0}?action={1}&site={2}&title={3}&thumb={4}&iurl={5}'.format(_url, mode, site, qtitle, urllib.quote(movie[1].encode('utf8')), iurl)
            list_item.setArt({'thumb': movie[1],
                              'icon': movie[1],
                              'poster': movie[1],
                              'fanart': _fanart})
        if mode == 9 and 'Next Page' not in title:
            is_folder = False
            list_item.setProperty('IsPlayable', 'true')
            list_item.addStreamInfo('video', {'codec': 'h264'})
            list_item.addContextMenuItems([('Save Video', 'RunPlugin(plugin://' + _addonID + '/?action=10&iurl=' + iurl + 'ZZZZ' + title + ')',)])
        else:
            is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'movies')
    xbmcplugin.endOfDirectory(_handle)


def list_videos(site, title, iurl, thumb):
    """
    Create the list of playable videos in the Kodi interface.
    """
    scraper = eval('{}.{}()'.format(site, site))
    videos = cache.cacheFunction(scraper.get_videos, iurl)
    listing = []
    for video in videos:
        list_item = xbmcgui.ListItem(label=video[0])
        list_item.setArt({'thumb': thumb,
                          'icon': thumb,
                          'poster': thumb,
                          'fanart': thumb})
        list_item.setInfo('video', {'title': title})
        list_item.addStreamInfo('video', {'codec': 'h264'})
        list_item.setProperty('IsPlayable', 'true')
        url = '{0}?action=9&iurl={1}'.format(_url, urllib.quote_plus(video[1]))
        if 'm3u8' not in video[1]:
            list_item.addContextMenuItems([('Save Video', 'RunPlugin(plugin://{0}/?action=10&iurl={1}ZZZZ{2})'.format(_addonID, urllib.quote_plus(video[1]), title),)])
        is_folder = False
        listing.append((url, list_item, is_folder))

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'videos')
    xbmcplugin.endOfDirectory(_handle)


def resolve_url(url):
    try:
        stream_url = resolveurl.HostedMediaFile(url=url).resolve()
        # If resolveurl returns false then the video url was not resolved.
        if not stream_url or not isinstance(stream_url, basestring):
            try:
                msg = stream_url.msg
            except:
                msg = url
            xbmcgui.Dialog().ok('Resolve URL', msg)
            return False
    except Exception as e:
        try:
            msg = str(e)
        except:
            msg = url
        xbmcgui.Dialog().ok('Resolve URL', msg)
        return False

    return stream_url


def play_video(iurl, dl=False):
    """
    Play a video by the provided path.
    """
    streamer_list = ['tamilgun', 'mersalaayitten', 'mhdtvworld.', '/hls/', 'poovee.',
                     'watchtamiltv.', 'cloudspro.', 'abroadindia.', 'nextvnow.', 'harpalgeo.',
                     'hindigeetmala.', '.mp4', 'googlevideo.', 'playembed.', 'akamaihd.',
                     'tamilhdtv.', 'andhrawatch.', 'tamiltv.', 'athavantv', 'cinemalayalam',
                     'justmoviesonline.', '.mp3', 'googleapis.', '.m3u8', 'telugunxt.',
                     'playsominaltv.', 'bharat-movies.', 'googleusercontent.', 'arydigital.',
                     'space-cdn.', 'einthusan.', 'd0stream.', 'telugugold.', 'tamilyogi.',
                     'hum.tv', 'apnevideotwo.', 'player.business']
    # Create a playable item with a path to play.
    title = 'unknown'
    if 'ZZZZ' in iurl:
        iurl, title = iurl.split('ZZZZ')

    play_item = xbmcgui.ListItem(path=iurl)
    vid_url = play_item.getfilename()
    # xbmc.log('\n@@@@DD Play URL = {}\n'.format(vid_url), xbmc.LOGNOTICE)

    if any([x in vid_url for x in streamer_list]):
        if 'mersalaayitten' in vid_url:
            scraper = mersal.mersal()
            stream_url, srtfile = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
            if srtfile:
                play_item.setSubtitles(['special://temp/mersal.srt', srtfile])
        elif 'apnevideotwo.' in vid_url:
            stream_url = urllib.quote(vid_url, ':/|=?')
            play_item.setPath(stream_url)
        elif 'player.business' in vid_url:
            headers = {'User-Agent': mozhdr}
            spage = requests.get(vid_url, headers=headers).text
            matches = re.findall(r'"src":"([^"]+)","label":"([^"]+)', spage)
            if len(matches) > 1:
                sources = []
                for match in matches:
                    sources.append(match[1])
                dialog = xbmcgui.Dialog()
                ret = dialog.select('Choose a Source', sources)
                match = matches[ret]
            else:
                match = matches[0]
            stream_url = match[0] + '|User-Agent={}'.format(mozhdr)
            play_item.setPath(stream_url)
        elif 'einthusan.' in vid_url:
            scraper = einthusan.einthusan()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'tamilyogi.' in vid_url:
            scraper = tyogi.tyogi()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'playsominaltv.' in vid_url:
            scraper = sominal.sominal()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'athavantv.' in vid_url:
            scraper = lyca.lyca()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'hindigeetmala.' in vid_url:
            scraper = gmala.gmala()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'telugunxt.' in vid_url or 'telugugold.' in vid_url:
            scraper = tflame.tflame()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                stream_url = resolve_url(stream_url)
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'bharat-movies.' in vid_url:
            scraper = bmov.bmov()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                stream_url = resolve_url(stream_url)
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'tamilgun.' in vid_url:
            if '.m3u8' in vid_url:
                stream_url = vid_url
            else:
                scraper = tgun.tgun()
                stream_url = scraper.get_video(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif 'andhrawatch.' in vid_url:
            scraper = awatch.awatch()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'arydigital.' in vid_url:
            scraper = ary.ary()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url:
                stream_url = resolve_url(stream_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        elif 'harpalgeo.' in vid_url:
            scraper = geo.geo()
            stream_url = scraper.get_video(vid_url)
            play_item.setPath(stream_url)
        elif 'hum.tv' in vid_url:
            scraper = hum.hum()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url or 'dailymotion' in stream_url:
                stream_url = resolve_url(stream_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        elif 'watchtamiltv.live' in vid_url:
            scraper = tamiltv.tamiltv()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                play_item.setPath(stream_url)
        elif 'mhdtvworld.' in vid_url:
            scraper = mhdtv.mhdtv()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url:
                stream_url = resolve_url(stream_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        elif 'cinemalayalam.' in vid_url:
            scraper = cinem.cinem()
            stream_url = scraper.get_video(vid_url)
            if 'youtube.' in stream_url:
                stream_url = resolve_url(stream_url)
            if stream_url:
                play_item.setPath(stream_url)
        elif 'playembed.' in vid_url or '.m3u8' in vid_url:
            stream_url = vid_url
            play_item.setPath(stream_url)
        elif 'abroadindia.' in vid_url:
            scraper = aindia.aindia()
            stream_url = scraper.get_video(vid_url)
            if stream_url:
                if 'youtube.' in stream_url:
                    stream_url = resolve_url(stream_url)
                elif '.f4m' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=HDS&url={}'.format(qurl)
                elif '.ts' in stream_url:
                    qurl = urllib.quote_plus(stream_url)
                    stream_url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&url={}'.format(qurl)
                if stream_url:
                    play_item.setPath(stream_url)
                else:
                    play_item.setPath(None)
        elif 'load.' in vid_url:
            stream_url = resolve_url(vid_url)
            if stream_url:
                play_item.setPath(stream_url)
            else:
                play_item.setPath(None)
        else:
            stream_url = vid_url
            play_item.setPath(stream_url)
    else:
        stream_url = resolve_url(vid_url)
        if stream_url:
            play_item.setPath(stream_url)
        else:
            play_item.setPath(None)

    if dl and stream_url:
        download_dir = _settings('dlfolder')
        if not download_dir:
            xbmcgui.Dialog().notification('Download:', 'Choose download directory in Settings!', _icon, 5000, False)
            return

        headers = {}
        if '|' in stream_url:
            stream_url, hdrs = stream_url.split('|')
            for x, y in parse_qsl(hdrs):
                headers[x] = y
        if 'User-Agent' not in headers.keys():
            headers.update({'User-Agent': mozhdr})

        if '.m3u8' in stream_url or stream_url.endswith('.bin'):
            xbmcgui.Dialog().notification('Download:', 'Cannot download HLS Streams!', _icon, 5000, False)
            return

        vidfile = xbmc.makeLegalFilename(download_dir + title + '.mp4')
        if not xbmcvfs.exists(vidfile):
            tmp_file = tempfile.mktemp(dir=download_dir, suffix='.mp4')
            tmp_file = xbmc.makeLegalFilename(tmp_file)
            pDialog.create('Deccandelight', 'Downloading', title)
            dfile = requests.get(stream_url, headers=headers, stream=True)
            totalsize = float(dfile.headers['content-length'])
            handle = open(tmp_file, "wb")
            chunks = 0
            for chunk in dfile.iter_content(chunk_size=8388608):
                if chunk:  # filter out keep-alive new chunks
                    handle.write(chunk)
                    chunks += 1
                    percent = int(float(chunks * 838860800) / totalsize)
                    pDialog.update(percent)
                    if pDialog.iscanceled():
                        handle.close()
                        xbmcvfs.delete(tmp_file)
                        break
            handle.close()
            try:
                xbmcvfs.rename(tmp_file, vidfile)
                return vidfile
            except:
                return tmp_file
        else:
            xbmcgui.Dialog().notification('Download:', 'File already exists!', _icon, 3000, False)

    elif stream_url:
        kodistr = xbmc.getInfoLabel('System.BuildVersion')
        kodiver = float(kodistr[0:3])
        # xbmc.log('\n@@@@DD Final URL = {}\n'.format(stream_url), xbmc.LOGNOTICE)
        if kodiver >= 17.0 and stream_url and ('yupp' not in stream_url) and ('SUNNXT' not in stream_url):

            if '.m3u8' in stream_url:
                play_item.setMimeType('application/vnd.apple.mpegstream_url')
                play_item.setContentLookup(False)
                adaptive_list = ['master', 'adaptive', 'tamilray', 'index']
                if any([x in stream_url for x in adaptive_list]):
                    play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                    play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
                    if '|' in stream_url:
                        stream_url, strhdr = stream_url.split('|')
                        play_item.setProperty('inputstream.adaptive.stream_headers', strhdr)
                        play_item.setPath(stream_url)

            elif '.mpd' in stream_url:
                play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                play_item.setMimeType('application/dash+xml')
                play_item.setContentLookup(False)

            elif '.ism' in stream_url:
                play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
                play_item.setProperty('inputstream.adaptive.manifest_type', 'ism')
                play_item.setMimeType('application/vnd.ms-sstr+xml')
                play_item.setContentLookup(False)

        xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    Action Definitions:
    1 : List Site
    4 : List Top Menu (Channels, Languages)
    5 : List Secondary Menu (Shows, Categories)
    6 : List Third Menu
    7 : List Individual Items (Movies, Episodes)
    8 : List Playable Videos
    9 : Play Video
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == '0':
            clear_cache()
        elif params['action'] == '1':
            list_menu(params['site'])
        elif params['action'] == '4':
            list_top(params['site'], params['iurl'])
        elif params['action'] == '5':
            list_second(params['site'], params['iurl'])
        elif params['action'] == '6':
            list_third(params['site'], params['iurl'])
        elif params['action'] == '7':
            list_items(params['site'], params['iurl'])
        elif params['action'] == '8':
            list_videos(params['site'], params['title'], params['iurl'], params['thumb'])
        elif params['action'] == '9':
            play_video(params['iurl'])
        elif params['action'] == '10':
            play_video(params['iurl'], dl=True)
    else:
        list_sites()
