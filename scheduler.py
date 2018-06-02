from datetime import datetime
import time
import schedule

# compare_from = '2018-05-25 17:56'
# compare_to = '2018-05-25 17:56'
compare_from = datetime.strptime('May 25 2018 6:12PM', '%b %d %Y %I:%M%p')
compare_to = datetime.strptime('May 25 2018 6:14PM', '%b %d %Y %I:%M%p')
# print (compare_from)
# print (compare_to)

def Compare():
    now = datetime.now()
    # now = now.replace("'","")
    # date_time = now.split(' ')
    # date = date_time[0]
    # time = date_time[1].split(':')
    # time_new = time[0] + ':' + time[1]

    # date_time_new = date + ' ' + time_new
    if (now >= compare_from and now <= compare_to):
        print ('True')
    else:
        print ('False')

schedule.every().seconds.do(Compare)

while True:
    schedule.run_pending()
    time.sleep(1)

