import mysql.connector
from pathlib import Path
import pathlib
import os

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="podcast_tracker",
)

cursor = conn.cursor()

select_podcast_query = "SELECT * FROM podcast"

cursor.execute(select_podcast_query)
result = cursor.fetchall()

for row in result:
    dir_path = os.path.join(os.path.dirname(__file__) + "\crawlers\\" ) # B:\workspace\mcflurry\podcast-tracker\crawlers\
    onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    if ( row[2] +".py" in onlyfiles): # if file name exist in directory array
        print(dir_path + row[2] +".py")
        exec(open(dir_path + "\\" + row[2] +".py").read())



# print(Path(__file__).resolve().parent.__str__() + "\crawlers\\")
# print(os.path.join(os.path.dirname(__file__) + "\crawlers\\" ))
# dir_path = os.path.join(os.path.dirname(__file__) + "\crawlers\\" )
# onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
# print(onlyfiles)
# if ("DarknetDiaries.py" in onlyfiles):
#     print("yes")