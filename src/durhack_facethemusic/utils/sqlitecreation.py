import sqlite3
import re
from pathlib import Path

name = "stockdata.db"
connection = sqlite3.connect("stockdata.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usdjpy (
timestamp TEXT NOT NULL PRIMARY KEY,
open REAL
)""")

connection.commit()

datastr = "Challenge1/USDJPY_USD_FORWARD_1M_1000000_20260701-20260831/"
datapath = Path("/home/ellew/Code/programmingtesting/Challenge1/USDJPY_USD_FORWARD_1M_1000000_20260701-20260831")

files = []

print(len(list(datapath.glob("*.csv"))))
print(53*24*60)

for file in datapath.glob("*.csv"):
    with open(file,"r") as f:
        filedata = f.read()
        stockdata = re.split(',|\n', filedata)
        allNumbersList = stockdata[30:]
        counter=0
        while True:
            try:
                files.append((allNumbersList[counter],allNumbersList[counter+4]))
            except:
                break
            counter += 30

statement = """
INSERT INTO usdjpy (timestamp, open)
VALUES (?, ?)
"""

cursor.executemany(statement,files)
connection.commit()
print("inserted:", cursor.rowcount)

startDate = datastr[-18:-10]
endDate = datastr[-9:-1]



print(startDate, endDate)

connection.close()