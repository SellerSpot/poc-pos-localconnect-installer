# importing the module
import subprocess
import os
import csv
import codecs

os.system("wmic product get name,version /format:csv > installedapps.csv")

spamreader = csv.reader(codecs.open(
    'installedapps.csv', 'rU', 'utf-16'), delimiter=',', quotechar='|')
for row in spamreader:
    if "MongoDB" in row[1]:
        print('.'.join(row[2].split('.')[0:2]))

# # traverse the software list
# Data = subprocess.(
#     ['wmic', 'product', 'get', 'name', ',', 'version'])

# for app in Data:
#     print(app)

# # a = str(Data)

# # # try block
# # try:

# #     # arrange the string
# #     for i in range(len(a)):
# #         app = a.split("\\r\\r\\n")[6:][i]
# #         print(app)

# # except IndexError as e:
# #     print("All Done"+e)
