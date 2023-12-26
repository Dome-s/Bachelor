import csv
import random
import os

source = ['address', 'country', 'Order', 'Name', 'email','test1','test2','test3']
target = ['shippingAddress', 'country', 'OrderId', 'FirstName', 'LastName','test1','test2','test3','test4','test5']


print("Current working directory:", os.getcwd())
with open("C:/Users/dominic/Desktop/Bachelor/Repos/DSMA/data.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["","instance","candName","targName","conf","realConf","pair"])
    for i in source:
        for j in target:
            randConf = random.random()
            randRconf = random.randint(0,1)
            writer.writerow ([((source.index(i))*len(target))+target.index(j),"1, Test",i,j,randConf,randRconf,""])
    for i in source:
        for j in target:
            randConf = random.random()
            randRconf = random.randint(0,1)
            writer.writerow ([((source.index(i))*len(target))+target.index(j)+len(target)*len(source),"2, Test",i,j,randConf,randRconf,""])

print(f"CSV file '{file}' created successfully.")