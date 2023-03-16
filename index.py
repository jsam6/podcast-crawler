import mysql.connector
from pathlib import Path
import pathlib
import os

database_name = "podcast_tracker"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
)

cursor = conn.cursor()

# migration of Database
cursor.execute("SHOW DATABASES")

# Check if podcast_tracker table exist
for x in cursor:
    if x[0] == database_name:
        print("The database exists")
        break
else:
    print("The database does not exist")
    cursor.execute("CREATE DATABASE " + database_name)

cursor.reset() 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database=database_name,
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")

table_exists = False
for x in cursor:
    if x[0] == "podcast":
        table_exists = True
        break


# If the table does not exist, create it
if not table_exists:
    cursor.execute("""
        CREATE TABLE `podcast_tracker`.`podcast` (
            `id` INT NOT NULL,
            `name` VARCHAR(45) NULL DEFAULT NULL,
            `url` TEXT NULL DEFAULT NULL,
            `file_name` TEXT NULL DEFAULT NULL,
            `created_at` DATETIME NULL DEFAULT NULL,
            PRIMARY KEY (`id`)
        );
    """)

    print("The table has been created")

select_podcast_query = "SELECT * FROM podcast"
cursor.execute(select_podcast_query)
results = cursor.fetchall()

if len(results) == 0:
    sql = "INSERT INTO `podcast_tracker`.`podcast` (`id`, `name`, `url`, `file_name`) VALUES ('1', 'Darknet Diaries', 'https://darknetdiaries.com/episode/',  'DarknetDiaries');"
    cursor.execute(sql)
    conn.commit()

select_podcast_query = "SELECT * FROM podcast"
cursor.execute(select_podcast_query)
results = cursor.fetchall()

for row in results:
    print(row[3])
    dir_path = os.path.join(os.path.dirname(__file__) + "\crawlers\\" ) # B:\workspace\mcflurry\podcast-tracker\crawlers\
    onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    if ( row[3] +".py" in onlyfiles): # if file name exist in directory array
        print(dir_path + row[2] +".py")
        exec(open(dir_path + "\\" + row[3] +".py").read())



# print(Path(__file__).resolve().parent.__str__() + "\crawlers\\")
# print(os.path.join(os.path.dirname(__file__) + "\crawlers\\" ))
# dir_path = os.path.join(os.path.dirname(__file__) + "\crawlers\\" )
# onlyfiles = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
# print(onlyfiles)
# if ("DarknetDiaries.py" in onlyfiles):
#     print("yes")