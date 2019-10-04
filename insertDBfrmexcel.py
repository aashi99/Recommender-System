import csv
import MySQLdb

#setting connection
conn=MySQLdb.connect(host='localhost', user='root', passwd='root', db='pythonlogin')
cursor=conn.cursor()
with open('C:\\Users\\USER\\Desktop\\Recommender_Sys\\ml-latest-small\\ratings.csv','r')as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)
    list=[]

    for row in csvreader:
        if row[0] not in list:
            list.append(row[0])
            cursor.execute("INSERT INTO accounts(password,name,userid) VALUES( %s, %s, %s)",(row[0],row[0],row[0]))
        # print(row,sep="")
        else:
            continue
conn.commit()
cursor.close()
print(list)
