import instaloader
from datetime import datetime
from itertools import dropwhile, takewhile

"""
This function returns the caption and post date for all Instagram posts made by 
each account in accounts between StartDate and EndDate as a list of dictionaries.
"""
def fetchData(accounts, StartDate, EndDate, L):
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



def fetchDataNoLogin(accounts, StartDate, EndDate):
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