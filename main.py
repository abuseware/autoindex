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
    """
    @return: Redirect user to autoindexed page
    """
    return flask.redirect('/browse/')


@web.route('/browse')
@web.route('/browse/')
@web.route('/browse/<path:path>')
def browse(path=''):
    """
    @param path: Path to directory
    @return: Generated index page or error
    """
    os.chdir(flask.request.environ['DOCUMENT_ROOT'])
    path = os.path.normpath(path)
    folders = []
    files = []

    if os.path.isdir(path):
        try:
            for entry in os.listdir(path):
                item = os.path.join(path, entry)

                if os.path.isfile(item):
                    files.append(entry)
                elif os.path.isdir(item):
                    folders.append(entry)

        except OSError:
            return flask.abort(403)

        else:
            nav = utils.populate_navbar(path)
            folders.sort()
            files.sort()
            return flask.render_template('browse.html', path=path, nav=nav, folders=folders, files=files, error=flask.request.args.get('error'))

    else:
        return flask.abort(404)


@web.route('/info')
@web.route('/info/<path:path>')
def info(path=''):
    """
    @param path: Path to file
    @return: Generated file info page or error
    """
    os.chdir(flask.request.environ['DOCUMENT_ROOT'])
    path = os.path.normpath(path)

    if os.path.isfile(path):
        try:
            properties = [
                ['File', os.path.basename(path)],
                ['Path', '/' + os.path.split(path)[0]],
                ['Size', utils.get_size(path)],
                ['Mimetype', utils.get_mime(path)],
            ]

        except OSError:
            return flask.abort(403)

        else:
            nav = utils.populate_navbar(path)
            return flask.render_template('info.html', path=path, nav=nav, properties=properties)

    else:
        return flask.abort(404)

@web.errorhandler(403)
@web.errorhandler(404)
@web.errorhandler(410)
@web.errorhandler(500)
def ehandler(e):
    return flask.redirect('/browse/?error={}'.format(e))
