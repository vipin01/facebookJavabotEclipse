import csv
ifile  = open('ques.csv', "r")
read = csv.reader(ifile)
for row in read :
    print (row)