import os, sys
import sqlite3
import operator
import  errno
from collections import OrderedDict
import matplotlib.pyplot as plt
from getsqldata import *
from datetime import datetime

uid = getCurrentUser()
conf = getRowValue('Setting',uid)
profile_path = conf[6]

direc = os.path.join(conf[5],'Website')
token = getRowValue('current_user',uid)[1]
time = datetime.now().strftime('%Y_%m_%d')
email = getRowValue('Users',uid)[1]
name = time + '-' + email+ '-' + 'history-' + token + '.txt'
logs = os.path.join(direc , name) #or full path if not in same directory
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

def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		print ("URL format error!")

def analyze(results):

   
    with open(logs, 'a', encoding='utf-8') as f:
        for site, count in sites_count_sorted.items():
            line = str(site) +'\t'+ str(count)+ '\n'
            f.write(line)
            #print (line)
  

#path to user's history database (Chrome)
user = os.path.expanduser('~')# + profile_path

## has not user in profile path
history_db = ''
if(profile_path.find(user) == -1):
    path = user + profile_path
    history_db = os.path.join(path, 'history')
else:
    history_db = os.path.join(profile_path, 'history')

print(history_db)

try:
        #querying the db
        c = sqlite3.connect(history_db)
        cursor = c.cursor()
        select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
        cursor.execute(select_statement)

        results = cursor.fetchall() #tuple

        sites_count = {} #dict makes iterations easier :D

        for url, count in results:
                url = parse(url)
                if url in sites_count:
                        sites_count[url] += 1
                else:
                        sites_count[url] = 1

        sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))

        analyze (sites_count_sorted)

		
except sqlite3.OperationalError as e:
	e = str(e)
	if (e == 'database is locked'):
		print('[!] Make sure Google Chrome is not running in the background')
		sys.exit(0)
	elif (e == 'no such table: logins'):
		print('[!] Something wrong with the database name')
		sys.exit(0)
	elif (e == 'unable to open database file'):
		print('[!] Something wrong with the database path')
		sys.exit(0)
	else:
		print(e)
		sys.exit(0)
