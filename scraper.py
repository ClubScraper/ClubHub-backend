import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile

def fetchData(club_list, StartDate, EndDate):
    L = instaloader.Instaloader()
    data = {club: [] for club in club_list}
  
    for index, club in enumerate(club_list):
        posts = instaloader.Profile.from_username(L.context, club).get_posts()
        
        filter_after_since = lambda p: p.date > EndDate
        filter_until = lambda p: p.date > StartDate
        
        filtered_posts = takewhile(filter_until, dropwhile(filter_after_since, posts))
        
        for post in filtered_posts:
            data[club].append((post.date.strftime('%Y/%m/%d'), post.caption))
    
    return data


## Runable Example

# clubList = ['amacss_utsc', 'web3.uoft', 'sdssuoft', 'uoftblueprint', 'uoft_aerospaceteam', 'uoft_utmist']   
# print(fetchData(club_list=clubList, StartDate=datetime(2024, 6, 1), EndDate=datetime(2024, 6, 7)))