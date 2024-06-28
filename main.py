import scraper
from datetime import datetime
from database import Database

db = Database()
clubList = ['amacss_utsc', 'web3.uoft', 'sdssuoft', 'uoftblueprint', 'uoft_aerospaceteam', 'uoft_utmist']   
data = scraper.fetchData(club_list=clubList, StartDate=datetime(2024, 6, 1), EndDate=datetime(2024, 6, 7))

print(data)
