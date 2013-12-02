#-*- coding: UTF-8 -*-

import os
import mimetypes

mimetypes.init()


def fill_path(path):
    if path[:1] != '/':
        path = '/' + path
    if path[-1:] != '/':
        path += '/'

    return path


def get_size(path):
    power_map = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    siz = os.path.getsize(path)
    power = 0

    while siz > 1024:
        siz /= 1024
        power += 1

    return '{} {}'.format(round(siz, 2), power_map[power])


def get_mime(path):
    mime = mimetypes.guess_type(path)[0]
    if not mime:
        mime = "application/octet-stream"

    return mime


def populate_navbar(path):
    if path[-1:] == os.sep:
        path = path[:-1]
    if path[:1] == os.sep:
        path = path[1:]

    entries = []
    navlist = path.split(os.sep)

    if len(navlist) > 0 and navlist[0] != '':
        for index in range(len(navlist)):
            if index == 0:
                entries.append([navlist[index], navlist[index]])
            else:
                entries.append([entries[index - 1][0] + os.sep + navlist[index], navlist[index]])

    return entries
