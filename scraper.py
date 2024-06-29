import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile

"""
This function returns the caption and post date for all Instagram posts made by 
each account in accounts between StartDate and EndDate as a list of dictionaries.
"""
def fetchData(accounts, StartDate, EndDate):
    L = instaloader.Instaloader()
    data = []
  
    for account in accounts:
        posts = instaloader.Profile.from_username(L.context, account).get_posts()
        
        filter_after_since = lambda p: p.date > EndDate
        filter_until = lambda p: p.date > StartDate
        
        filtered_posts = takewhile(filter_until, dropwhile(filter_after_since, posts))
        
        for post in filtered_posts:
            data.append({"account": account, 
                         "date": post.date.strftime('%Y/%m/%d'), 
                         "caption": post.caption})
    
    return data

"""
This is the old implementation and returns data the format {account: [(date, caption)]}.
This implementation was depreciated because further data proprocessing was 
needed before uploading to Supabase

def fetchData(club_list, StartDate, EndDate):
    L = instaloader.Instaloader()
    data = {club: [] for club in club_list}
  
    for club in club_list:
        posts = instaloader.Profile.from_username(L.context, club).get_posts()
        
        filter_after_since = lambda p: p.date > EndDate
        filter_until = lambda p: p.date > StartDate
        
        filtered_posts = takewhile(filter_until, dropwhile(filter_after_since, posts))
        
        for post in filtered_posts:
            data[club].append((post.date.strftime('%Y/%m/%d'), post.caption))
    
    return data
"""
## Runable Example
# accounts = ['amacss_utsc', 'web3.uoft', 'sdssuoft', 
#             'uoftblueprint', 'uoft_aerospaceteam', 
#             'uoft_utmist']   

# print(fetchData(accounts=accounts, StartDate=datetime(2024, 6, 1), EndDate=datetime(2024, 6, 7)))