import sql_transactions as sqlt
from datetime import date

sqlt.db.connect
mytrans = ("HSBC", date(1980, 8, 1), 5, "Helo", "toolate", "Salesteam", "test", "EUR", 1.0, False, False)

sqlt.insert_transaction(mytrans)
print(sqlt.match_transaction(mytrans))
