#!/usr/bin/env python
#-*- coding: UTF-8 -*-

"""
    Copyright:  Artur "Licho" Kaleta
    License:    MIT
"""

import sys
import os
import flask

web = flask.Flask(__name__)

@web.route('/')
def index():
    return flask.redirect('/browse')

@web.route('/browse')
@web.route('/browse/')
@web.route('/browse/<path:path>')
def browse(path='/'):

    folders = []
    files = []
   
    if path[:1] != '/':
        path = '/'+path
    if path[-1:] != '/':
        path += '/'

    if os.path.isdir('./'+path):
        try:
            for entry in os.listdir('./'+path):
                if os.path.isfile('./'+path+'/'+entry):
                    files.append(entry)
                else:
                    folders.append(entry)
        finally:
            folders.sort()
            files.sort()
            return flask.render_template('browse.html',path=path,folders=folders,files=files)
    
    return flask.abort(403)


#@web.route('/info')
#@web.route('/info/<path:path>')
#def info(path='/'):
#    pass

#@web.route('/get')
#@web.route('/get/<path:path>')
#def get(path='/'):
#    pass

if(__name__ == "__main__"):
    web.run(debug=True)
