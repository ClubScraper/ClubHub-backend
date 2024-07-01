from scraper import fetchData
from datetime import datetime, timedelta
from database import Database
from constants import ACCOUNTS_TABLE, DATA_TABLE

db = Database()

# Purging old events
accounts = db.getData(ACCOUNTS_TABLE, "club_name")
purge_date = datetime.today() - timedelta(days=90)
purge_date = purge_date.date()
db.purgeData(ACCOUNTS_TABLE, purge_date)

# Adding new events
start_date = datetime.today() - timedelta(days=7)
start_date = start_date.date()
end_date = datetime.today().date()

unfiltered_data = fetchData(accounts, start_date, end_date)
 
# Note that the data returned by fetchData is unfiltered because it returns all
# posts not just events and currently the "date" attribute is the posting date
# rather than the event date

# ToDo !
# Filter data for events and event date. 

db.insertData(DATA_TABLE, unfiltered_data)