from supabase import create_client, Client
from define import KEY, URL
import os

def getData():  
    supabase: Client = create_client(URL, KEY)
    response = supabase.table("club_accounts").select("*").execute()
    test = [l["club_name"] for l in list(response)[0][1]]
    return test


def uploadData():
    pass
    