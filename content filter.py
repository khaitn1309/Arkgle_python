import os

os.system('wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ("208.67.222.222", "208.67.220.220")')

#vào gpedit: User Configuration => Administrative template => Network => Network connections