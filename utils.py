#-*- coding: UTF-8 -*-

import os
import mimetypes

mimetypes.init()


def get_size(path):
    """
    @param path: Normalized path
    @return: Human readable file size
    @rtype: str
    """
    power = 0
    power_map = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    try:
        siz = os.path.getsize(path)

        while siz > 1024:
            siz /= 1024
            power += 1

    except OSError as e:
        return 'Error {}: {}'.format(e.errno, e.strerror)

    else:
        return '{} {}'.format(round(siz, 2), power_map[power])


def get_mime(path):
    """
    @param path: Normalized file path
    @return: Guessed mime type
    @rtype : str
    """
    mime = mimetypes.guess_type(path)[0]
    if not mime:
        mime = 'application/octet-stream'

    return mime


def populate_navbar(path):
    """
    @param path: Normalized file path
    @return: List of relative path and entry name pairs
    @rtype: list
    """
    entries = []

    while not path in ('', '.'):
        temp = os.path.split(path)
        entries.insert(0, [path, temp[1]])
        path = temp[0]
    return entries
