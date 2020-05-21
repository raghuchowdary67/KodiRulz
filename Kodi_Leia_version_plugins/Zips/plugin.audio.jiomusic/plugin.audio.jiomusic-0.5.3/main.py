"""
    JioSaavn Kodi Addon
    Copyright (C) 2020 Raghu

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


    API Endpoint URLs
    Big Thanks to Vikas Kapadiya
    https://github.com/vikas5914

    Base Url - https://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/home/{language}
    Image Url -  https://jioimages.cdn.jio.com/hdindiamusic/images/{image_url}
    Album url - http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/albumsongs/albumid/{album_id}
    Playlist Url - http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/listsongs/playlistsongs/{playlist_id}
    Seacrh Url - http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/search2/{name}/{language (optional)}
    Search autocomplete Url - http://beatsapi.media.jio.com/v2_1/beats-api/jio/src/response/autocomplete/{name}
    Song Url - http://jiobeats.cdn.jio.com/mod/_definst_/mp4:hdindiamusic/audiofiles/{id}/(song}/{song_id}_{bitrate}.mp4/chunklist.m3u8
               http://jiobeats.cdn.jio.com/mod/_definst_/smil:hdindiamusic/audiofiles/{id}/{song}/{song_id}_h.smil/playlist.m3u8
"""

import sys
from resources.lib import jiosaavn

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    jiosaavn.router(sys.argv[2][1:])
