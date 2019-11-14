import os
path = "~/Downloads/"
num = input('number of records:')
num = int(num)       

fileList=os.listdir(path)
oldname = path + "hd1.mp4"
newname = path + "Lecture 1.mp4"
os.rename(oldname,newname) 

for i in range(1, num):
    oldname= path + "hd1 (" + str(i) + ").mp4"
    newname= path + "Lecture " + str(i+1) + ".mp4"