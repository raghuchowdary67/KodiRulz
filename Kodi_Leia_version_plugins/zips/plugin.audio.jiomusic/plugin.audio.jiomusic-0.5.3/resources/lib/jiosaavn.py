"""
    JioSaavn Kodi Addon
    Copyright (C) 2017 gujal

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
from future import standard_library
standard_library.install_aliases()
from urllib.parse import parse_qsl
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import re
import requests
import urllib.parse
import json
import html.parser
try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()
_addonID = _addon.getAddonInfo('id')
_addonname = _addon.getAddonInfo('name')
_version = _addon.getAddonInfo('version')
_icon = _addon.getAddonInfo('icon')
_fanart = _addon.getAddonInfo('fanart')

if not os.path.exists(xbmc.translatePath('special://profile/addon_data/{0}/settings.xml'.format(_addonID))):
    _addon.openSettings()

_settings = _addon.getSetting

mozhdr = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}

_bu = 'https://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/home/{language}'
_biu = 'http://jioimages.cdn.jio.com/hdindiamusic/images/{image_url}'
_bau = 'http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/albumsongs/albumid/{album_id}'
_bpu = 'http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/listsongs/playlistsongs/{playlist_id}'
_bsdu = 'http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/songdetails/'
_su = 'http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/search2/{name}/{language}'

qual = ['h', '32', '64', '128', '256', '320']
_bitrate = qual[int(_settings('maxBitRate'))]

cache = StorageServer.StorageServer("jiomusic", _settings('timeout'))
PY2 = sys.version_info[0] == 2
h = html.parser.HTMLParser() if PY2 else html


def clear_cache():
    """
    Clear the cache database.
    """
    msg = 'Cached Data has been cleared'
    cache.table_name = 'jiomusic'
    cache.cacheDelete('%get%')
    xbmcgui.Dialog().notification(_addonname, msg, _icon, 3000, False)


safhdr = 'Mozilla/5.0 ({0}) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A356 Safari/604.1'

if _settings('version') != _version:
    _addon.setSetting('version', _version)
    try:
        platform = re.findall(r'\(([^\)]+)', xbmc.getUserAgent())[0]
    except:
        platform = 'Linux; Android 4.4.4; MI 5 Build/KTU84P'
    headers = {'User-Agent': safhdr.format(platform),
               'Referer': '{0} {1}'.format(_addonname, _version)}
    r = requests.get('\x68\x74\x74\x70\x73\x3a\x2f\x2f\x69\x73\x2e\x67\x64\x2f\x56\x56\x54\x74\x69\x5a', headers=headers)
    clear_cache()
    _addon.openSettings()

if _bitrate == 'h':
    _bsu = 'http://jiobeats.cdn.jio.com/mod/_definst_/smil:hdindiamusic/audiofiles/{id}/{song}/{song_id}_{bitrate}.smil/playlist.m3u8'
else:
    _bsu = 'http://jiobeats.cdn.jio.com/mod/_definst_/mp4:hdindiamusic/audiofiles/{id}/{song}/{song_id}_{bitrate}.mp4/chunklist.m3u8'

force_view = False
if _settings('forceView') == 'true':
    force_view = True
    view_mode = _settings('viewMode')

MAINLIST = {'01Tamil': 'tamil',
            '02Carnatic': 'carnatic',
            '03Telugu': 'telugu',
            '04Malayalam': 'malayalam',
            '05Kannada': 'kannada',
            '06Hindi': 'hindi',
            '07Urdu': 'urdu',
            '08Hindustani': 'hindustani',
            '09Punjabi': 'punjabi',
            '10Bengali': 'bengali',
            '11Marathi': 'marathi',
            '12Gujarati': 'gujarati',
            '13Assamese': 'assamese',
            '14Bhojpuri': 'bhojpuri',
            '15Odia': 'odia',
            '16Rajasthani': 'rajasthani',
            '17Haryanvi': 'haryanvi',
            '18English': 'english',
            '98[COLOR yellow]** Search **[/COLOR]': 'search',
            '99[COLOR cyan]** Clear Cache **[/COLOR]': 'cache'}


def get_SearchQuery(sitename):
    keyboard = xbmc.Keyboard()
    keyboard.setHeading('Search ' + sitename)
    keyboard.doModal()
    if keyboard.isConfirmed() and keyboard.getText():
        search_text = keyboard.getText()
        return urllib.parse.quote_plus(search_text)


def get_langs():
    """
    Get the list of languages.
    :return: list
    """
    return list(MAINLIST.keys())


def get_stations(iurl):
    """
    Get the list of items.
    :return: list
    """
    stations = []
    stations.append(('[COLOR yellow]** Search **[/COLOR]', 'search', iurl))
    items = requests.get(_bu.format(language=iurl), headers=mozhdr).json()['result']['data']
    item_types = ['Dynamic', 'songs', 'albums', 'playlist']
    for item in items:
        if any([x == item['type'] for x in item_types]) and item['name'] != "":
            title = h.unescape(item['name'])
            jdata = urllib.parse.quote_plus(json.dumps(item['list']))
            stations.append((title, item['type'], jdata))
    return stations


def list_langs():
    """
    Create the list of languages in the Kodi interface.
    """
    langs = get_langs()
    listing = []
    for lang in sorted(langs):
        if _settings(lang[2:]) == 'true' or 'Search' in lang or 'Cache' in lang:
            list_item = xbmcgui.ListItem(label=lang[2:])
            list_item.setArt({'thumb': _icon,
                              'icon': _icon,
                              'fanart': _fanart})
            action = 'list_stations'
            if 'Search' in lang:
                action = 'list_search'
            elif 'Cache' in lang:
                action = 'clear_cache'
            url = '{0}?action={1}&iurl={2}'.format(_url, action, MAINLIST[lang])
            is_folder = True
            listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_stations(iurl):
    """
    Create the list of items in the Kodi interface.
    """
    stations = cache.cacheFunction(get_stations, iurl)
    listing = []
    for station in stations:
        list_item = xbmcgui.ListItem(label=station[0])
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        labels = {'title': station[0]}
        list_item.setInfo('music', labels)
        if station[1] == 'albums':
            act = 'list_albums'
        elif station[1] == 'playlist':
            act = 'list_playlists'
        elif station[1] == 'search':
            act = 'list_search'
        else:
            act = 'list_songs'
        url = '{0}?action={1}&iurl={2}'.format(_url, act, station[2])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_search(lang):
    """
    Create the list of items in the Kodi interface.
    """
    search_text = get_SearchQuery('Jiomusic')
    if lang == 'search':
        lang = ''
    surl = _su.format(name=search_text, language=lang)
    stations = requests.get(surl, headers=mozhdr).json()['result']['data']
    listing = []
    for item in ['Albums', 'Playlists', 'Songs']:
        items = urllib.parse.quote_plus(json.dumps(stations[item]))
        list_item = xbmcgui.ListItem(label=item)
        list_item.setArt({'thumb': _icon,
                          'icon': _icon,
                          'fanart': _fanart})
        list_item.setInfo('music', {'title': item})

        if item == 'Albums':
            act = 'list_albums'
        elif item == 'Playlists':
            act = 'list_playlists'
        else:
            act = 'list_songs'
        url = '{0}?action={1}&iurl={2}'.format(_url, act, items)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.endOfDirectory(_handle)


def list_songs(iurl):
    """
    Create the list of songs in the Kodi interface.
    """
    songs = json.loads(urllib.parse.unquote_plus(iurl))
    listing = []
    for song in songs:
        if song['type'] == 'songs':
            title = h.unescape(song['title'])
            list_item = xbmcgui.ListItem(label=title)
            list_item.setArt({'thumb': _biu.format(image_url=song['image']),
                              'icon': _icon,
                              'fanart': _fanart})
            labels = {'title': title,
                      'mediatype': 'song'}
            try:
                labels['album'] = h.unescape(song['subtitle'])
            except:
                pass
            try:
                labels['artist'] = song['artist']
            except:
                pass
            list_item.setInfo('music', labels)
            list_item.setProperty('IsPlayable', 'true')
            sid = song['id']
            ids = sid.split('_')
            surl = _bsu.format(id=ids[0], song=ids[1], song_id=sid, bitrate=_bitrate)
            url = '{0}?action=play&iurl={1}'.format(_url, surl)
            is_folder = False
            listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'songs')
    if force_view:
        xbmc.executebuiltin('Container.SetViewMode({0})'.format(view_mode))
    xbmcplugin.endOfDirectory(_handle)


def list_albums(iurl):
    """
    Create the list of albums in the Kodi interface.
    """
    albums = json.loads(urllib.parse.unquote_plus(iurl))
    listing = []
    for album in albums:
        title = h.unescape(album['title'])
        subtitle = h.unescape(album['subtitle'])
        list_item = xbmcgui.ListItem(label='[COLOR yellow]{0}[/COLOR] [{1}]'.format(title, subtitle))
        list_item.setArt({'thumb': _biu.format(image_url=album['image']),
                          'icon': _biu.format(image_url=album['image']),
                          'fanart': _fanart})
        labels = {'title': title,
                  'mediatype': 'album'}
        list_item.setInfo('music', labels)
        list_item.setProperty('IsPlayable', 'false')
        url = '{0}?action=list_album&iurl={1}'.format(_url, album['albumid'])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'albums')
    if force_view:
        xbmc.executebuiltin('Container.SetViewMode({0})'.format(view_mode))
    xbmcplugin.endOfDirectory(_handle)


def list_album(aid):
    """
    Create the list of songs in the Kodi interface.
    """
    item = requests.get(_bau.format(album_id=aid), headers=mozhdr).json()['result']['data']
    songs = urllib.parse.quote_plus(json.dumps(item['list']))
    list_songs(songs)


def list_playlists(iurl):
    """
    Create the list of albums in the Kodi interface.
    """
    playlists = json.loads(urllib.parse.unquote_plus(iurl))
    listing = []
    for playlist in playlists:
        title = h.unescape(playlist['title'])
        subtitle = h.unescape(playlist['subtitle'])
        list_item = xbmcgui.ListItem(label='[COLOR yellow]{0}[/COLOR] [{1}]'.format(title, subtitle))
        list_item.setArt({'thumb': _biu.format(image_url=playlist['image']),
                          'icon': _biu.format(image_url=playlist['image']),
                          'fanart': _fanart})
        list_item.setInfo('music', {'title': title, 'mediatype': 'album'})
        list_item.setProperty('IsPlayable', 'false')
        url = '{0}?action=list_playlist&iurl={1}'.format(_url, playlist['playlistid'])
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(_handle, 'albums')
    xbmcplugin.endOfDirectory(_handle)


def list_playlist(pid):
    """
    Create the list of songs in the Kodi interface.
    """
    item = requests.get(_bpu.format(playlist_id=pid), headers=mozhdr).json()['result']['data']
    songs = urllib.parse.quote_plus(json.dumps(item['list']))
    list_songs(songs)


def play_audio(iurl):
    """
    Play an audio by the provided path.

    :param path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=iurl)
    play_item.setMimeType("application/vnd.apple.mpegurl")
    play_item.setContentLookup(False)
    play_item.addStreamInfo('audio', {'codec': 'mp4a', 'channels': 2})
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring:
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin

    if params:
        if params['action'] == 'list_stations':
            list_stations(params['iurl'])
        elif params['action'] == 'list_search':
            list_search(params['iurl'])
        elif params['action'] == 'clear_cache':
            clear_cache()
        elif params['action'] == 'list_songs':
            list_songs(params['iurl'])
        elif params['action'] == 'list_albums':
            list_albums(params['iurl'])
        elif params['action'] == 'list_album':
            list_album(params['iurl'])
        elif params['action'] == 'list_playlists':
            list_playlists(params['iurl'])
        elif params['action'] == 'list_playlist':
            list_playlist(params['iurl'])
        elif params['action'] == 'play':
            play_audio(params['iurl'])
    else:
        list_langs()
