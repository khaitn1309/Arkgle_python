#!/usr/bin/env python

from __future__ import print_function
import argparse
import io,errno,os
from json import loads
from os import environ
from os.path import expanduser
from platform import system
from re import match
from sys import argv, stderr
from getsqldata import *


uid = getCurrentUser()
conf = getRowValue('Setting',uid)
profile_path = conf[6]

# path to user's login data
path = os.path.expanduser('~') + profile_path
#print(path)
login_db = os.path.join(path, 'Bookmarks')

direc = os.path.join(conf[5],'Website')
logs = os.path.join(direc , 'bookmark.html')
#or full path if not in same directory
# create file log
try:
    os.makedirs(direc)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# create file log
try:
    if(os.path.exists(logs)):
        os.remove(logs)
    f = open(logs, 'x')
    f.close()
except :
    pass

script_version = "2.0.1"

# html escaping code from http://wiki.python.org/moin/EscapingHtml

html_escape_table = {
	"&": "&amp;",
	'"': "&quot;",
	"'": "&#39;",
	">": "&gt;",
	"<": "&lt;",
	}

output_file_template = """<!DOCTYPE NETSCAPE-Bookmark-file-1>

<meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
<title>Bookmarks</title>
<h1>Bookmarks</h1>

<dl><p>

<dl>{bookmark_bar}</dl>

<dl>{other}</dl>
"""

def html_escape(text):
	return ''.join(html_escape_table.get(c,c) for c in text)

def sanitize(string):
	res = ''
	string = html_escape(string)

	for i in range(len(string)):
		if ord(string[i]) > 127:
			res += '&#x{:x};'.format(ord(string[i]))
		else:
			res += string[i]

	return res

def html_for_node(node):
	if 'url' in node:
		return html_for_url_node(node)
	elif 'children' in node:
		return html_for_parent_node(node)
	else:
		return ''

def html_for_url_node(node):
	if not match("javascript:", node['url']):
		return '<dt><a href="{}">{}</a>\n'.format(sanitize(node['url']), sanitize(node['name']))
	else:
		return ''

def html_for_parent_node(node):
	return '<dt><h3>{}</h3>\n<dl><p>{}</dl><p>\n'.format(sanitize(node['name']),
			''.join([html_for_node(n) for n in node['children']]))


input_filename = login_db
#environ["LOCALAPPDATA"] + r"\Google\Chrome\User Data\Profile 7\Bookmarks"

try:
	input_file = io.open(input_filename, 'r', encoding='utf-8')
except IOError as e:
	if e.errno == 2:
		print("The bookmarks file could not be found in its default location. \r\nPlease specify the input file manually.")
		exit(1)

output_file = io.open(logs, 'a', encoding='utf-8')

contents = loads(input_file.read())
input_file.close()

bookmark_bar = html_for_node(contents['roots']['bookmark_bar'])
other = html_for_node(contents['roots']['other'])

output_file.write(output_file_template.format(bookmark_bar=bookmark_bar, other=other))
output_file.close()
