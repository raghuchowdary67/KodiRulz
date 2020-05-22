"""
Deccandelight scraper plugin
Copyright (C) 2018 gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
from _base_ import Scraper
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib
import re
import requests
import HTMLParser
import json


class einthusan(Scraper):
    def __init__(self):
        Scraper.__init__(self)
        self.bu = 'https://einthusan.tv/'
        self.icon = self.ipath + 'einthusan.png'
        self.list = {'01Tamil': self.bu + 'launcher/?lang=tamil',
                     '02Telugu': self.bu + 'launcher/?lang=telugu',
                     '03Malayalam': self.bu + 'launcher/?lang=malayalam',
                     '04Kannada': self.bu + 'launcher/?lang=kannada',
                     '05Hindi': self.bu + 'launcher/?lang=hindi',
                     '06Bengali': self.bu + 'launcher/?lang=bengali',
                     '07Marathi': self.bu + 'launcher/?lang=marathi',
                     '08Punjabi': self.bu + 'launcher/?lang=punjabi'}
        self.hdr.update({'Referer': self.bu, 'Origin': self.bu[:-1]})

    def decrypt(self, e):
        t = 10
        i = e[0:t] + e[-1] + e[t + 2:-1]
        return json.loads(i.decode('base64'))

    def get_menu(self):
        return (self.list, 4, self.icon)

    def get_top(self, iurl):
        """
        Get the list of categories.
        """
        cats = []
        html = requests.get(iurl, headers=self.hdr).text
        mlink = SoupStrainer('section', {'id': 'UILaunchPad'})
        mdiv = BeautifulSoup(html, parseOnlyThese=mlink)
        items = mdiv.findAll('li')
        thumb = 'http://s3.amazonaws.com/einthusanthunderbolt/etc/img/{}.jpg'.format(iurl.split('=')[1])
        for item in items:
            if 'input' not in str(item) and 'data-disabled' not in str(item):
                title = item.p.text
                if title not in ['Feed', 'Contact', 'Go Premium']:
                    url = self.bu[:-1] + item.find('a')['href']
                    cats.append((title, thumb, url))
        surl = '{0}movie/results/?lang={1}&query=MMMM7'.format(self.bu, iurl.split('=')[1])
        cats.append(('[COLOR yellow]** Search Movies **[/COLOR]', thumb, surl))
        return cats, 5

    def get_second(self, iurl):
        """
        Get the list of types.
        """
        thumb = 'http://s3.amazonaws.com/einthusanthunderbolt/etc/img/{}.jpg'.format(iurl.split('=')[1])
        cats = [('Alphabets', thumb, iurl + 'MMMMAlphabets|Numbers'),
                ('Years', thumb, iurl + 'MMMMYear')]
        return cats, 6

    def get_third(self, iurl):
        """
        Get the list of types.
        """
        cats = []
        iurl, sterm = iurl.split('MMMM')
        html = requests.get(iurl, headers=self.hdr).text
        if sterm == 'Year':
            spat = 'href="([^"]+(?:{})[^"]+)">([^<]+)'.format(sterm)
        else:
            spat = r'href="([^"]+(?:{})[^"]+)"\s*data-disabled="">([^<]+)'.format(sterm)
        items = re.findall(spat, html)
        thumb = 'http://s3.amazonaws.com/einthusanthunderbolt/etc/img/{}.jpg'.format(iurl.split('=')[1])
        for url, title in items:
            url = self.bu[:-1] + url.replace('&amp;', '&')
            if '/playlist/' in url:
                title += '  [COLOR cyan][I]Playlists[/I][/COLOR]'
            cats.append((title, thumb, url))

        return cats, 7

    def get_items(self, iurl):
        clips = []
        h = HTMLParser.HTMLParser()
        if iurl.endswith('='):
            search_text = self.get_SearchQuery('Einthusan')
            search_text = urllib.quote_plus(search_text)
            iurl += search_text
        nextpg = True
        nmode = 9
        while nextpg and len(clips) < 18:
            html = requests.get(iurl, headers=self.hdr).text
            if '/movie-clip/' in iurl:
                items = re.findall(r'data-disabled="false"\s*href="([^"]+)">\s*<img\s*src="([^"]+).+?>([^<]+)</h3.+?info">(.+?)</div', html)
            else:
                items = re.findall(r'data-disabled="false"\s*href="([^"]+)"><img\s*src="([^"]+).+?h3>([^<]+).+?info">(.+?)</div', html)
            for url, thumb, title, info in items:
                title = h.unescape(title).encode('utf8')
                if 'Subtitle' in info:
                    title += '  [COLOR cyan][I]with subtitles[/I][/COLOR]'
                elif '/movie-clip/' in iurl and '/playlist/' not in url:
                    mtitle = h.unescape(re.findall('title="([^"]+)', info)[0]).encode('utf8')
                    title = '[COLOR cyan]{}[/COLOR] - [COLOR yellow]{}[/COLOR]'.format(mtitle, title)
                url = self.bu[:-1] + url
                if not thumb.startswith('http'):
                    thumb = 'http:' + thumb
                clips.append((title, thumb, url))
            if len(clips) > 0 and '/playlist/' in url:
                nmode = 7
            paginator = re.search(r'>(Page[^<]+).+?data-disabled=""\s*href="([^"]+)"><i>&#xe956;</i><p>Next<', html, re.DOTALL)

            if paginator:
                iurl = self.bu[:-1] + paginator.group(2).replace('&amp;', '&')
            else:
                nextpg = False

        if nextpg:
            title = 'Next Page.. (Currently in {})'.format(paginator.group(1))
            clips.append((title, self.nicon, iurl))

        return clips, nmode

    def get_video(self, iurl):
        h = HTMLParser.HTMLParser()
        headers = self.hdr
        r = requests.get(iurl, headers=headers)
        token = h.unescape(re.findall('data-pageid="([^"]+)', r.text)[0])
        ej = re.findall('data-ejpingables="([^"]+)', r.text)[0]
        xj = {"EJOutcomes": ej,
              "NativeHLS": False}
        pdata = {'xEvent': 'UIVideoPlayer.PingOutcome',
                 'xJson': json.dumps(xj).replace(' ', ''),
                 'gorilla.csrf.Token': token}
        headers.update({'X-Requested-With': 'XMLHttpRequest'})
        aurl = iurl.replace('/movie', '/ajax/movie')
        r2 = requests.post(aurl, data=pdata, headers=headers, cookies=r.cookies)
        stream_url = self.decrypt(r2.json()['Data']['EJLinks'])['MP4Link']
        # self.log(stream_url)
        return stream_url
