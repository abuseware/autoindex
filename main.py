#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
    Copyright:  Artur "Licho" Kaleta
    License:    MIT
"""

import os
import flask

import utils

web = flask.Flask(__name__)


@web.route('/')
def index():
    return flask.redirect('/browse')


@web.route('/browse')
@web.route('/browse/')
@web.route('/browse/<path:path>')
def browse(path=''):
    fullpath = flask.request.environ['DOCUMENT_ROOT'] + os.sep + path

    folders = []
    files = []

    path = utils.fill_path(path)

    if os.path.isdir(fullpath):
        try:
            for entry in os.listdir(fullpath):
                if os.path.isfile(fullpath + os.sep + entry):
                    files.append(entry)
                else:
                    folders.append(entry)
        except OSError:
            return flask.abort(404)
        else:
            nav = utils.populate_navbar(path)
            folders.sort()
            files.sort()
            return flask.render_template('browse.html', path=path, nav=nav, folders=folders, files=files)
    else:
        return flask.abort(404)


@web.route('/info')
@web.route('/info/<path:path>')
def info(path=''):
    fullpath = flask.request.environ['DOCUMENT_ROOT'] + os.sep + path

    if os.path.isfile(fullpath):
        try:
            properties = [
                ['File', path],
                ['Size', utils.get_size(fullpath)],
                ['Mimetype', utils.get_mime(fullpath)],
            ]
        except OSError:
            return flask.abort(404)
        else:
            nav = utils.populate_navbar(path)
            return flask.render_template('info.html', path=path, nav=nav, properties=properties)
    else:
        return flask.abort(404)
