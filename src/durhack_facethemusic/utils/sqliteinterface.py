import sqlite3

class Interface():
    def __init__(self,name):
        self.name = name
    
    def getRange(self, currency, startDate, endDate):
        con = sqlite3.connect(self.name)
        cur = con.cursor()

        data = {
            "startDate":startDate,
            "endDate":endDate + " 23:59:59"
        }

        match currency:
            case "eurusd":
                statement = """
SELECT open FROM eurusd WHERE timestamp >= :startDate AND timestamp <= :endDate;
"""
            case "usdjpy":
                statement = """
SELECT open FROM usdjpy WHERE timestamp >= :startDate AND timestamp <= :endDate;
"""
            case "usdsgd":
                statement = """
SELECT open FROM usdsgd WHERE timestamp >= :startDate AND timestamp <= :endDate;
"""

        res = cur.execute(statement, data).fetchall()

        con.commit()
        con.close()
        return list(map(lambda x: x[0], res))

#interface = Interface("/path/to/stockdata.db")
#print(interface.getRange('usdjpy', '2026-07-12', '2026-07-14'))
#returns 1D list of values in time period inclusive