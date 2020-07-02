import csv
import os.path
from datetime import date
from datetime import datetime
def write_csv():
    with open('conversation.csv', 'w') as newFile:

        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(['date','time','conversation'])

def append_csv(statement):
    with open('conversation.csv', 'a') as newFile:
        now = datetime.now()
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow([date.today(),now.strftime("%H:%M:%S"),statement])

def read_csv():

    with open('conversation.csv', 'r') as userFile:
        userFileReader = csv.reader(userFile)
        for row in userFileReader:
            print(row)


