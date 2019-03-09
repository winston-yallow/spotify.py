import inspect
import functools

import spotify
from spotify import _types, models
from spotify.sync import _thread


class SyncMeta:
    def __getattribute__(self, key):
        attr = object.__getattribute__(self, key)

        if inspect.iscoroutinefunction(attr):
            @functools.wraps(attr)
            def decorator(*args, **kwargs):
                return _thread.run_coro(attr(*args, **kwargs))
            setattr(self, key, decorator)
            return decorator
        return attr


class HTTPClient(spotify.HTTPClient, SyncMeta):
    pass


class HTTPUserClient(spotify.HTTPUserClient, SyncMeta):
    pass


class Client(spotify.Client, SyncMeta):
    _default_http_client = HTTPClient

    def __init__(self, *args, **kwargs):
        kwargs['loop'] = _thread._loop
        super().__init__(*args, **kwargs)


class Track(models.Track, SyncMeta):
    pass


class User(models.User, SyncMeta):
    pass


class PlaylistTrack(models.PlaylistTrack, SyncMeta):
    pass


class Artist(models.Artist, SyncMeta):
    pass


class Album(models.Album, SyncMeta):
    pass


class Playlist(models.Playlist, SyncMeta):
    pass


class Library(models.Library, SyncMeta):
    pass


_types.update({
    'artist': Artist,
    'track': Track,
    'user': User,
    'playlist': Playlist,
    'album': Album,
    'library': Library,
    'playlist_track': PlaylistTrack
})

for klass in _types.values():
    setattr(spotify.client, klass.__name__, klass)
