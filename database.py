from supabase import create_client, Client
from define import KEY, URL

class Database:
    def __init__(self):
        self.db: Client = create_client(URL, KEY)
    
        """
        TO DO! As of right now this function is useless as its functionality 
        already exists within the Supabase Python client 
        """
    def getData(self, table_name, column):      
        response = self.db.table(table_name).select("*").execute()
        data = [d[column] for d in response.data]
        return data

        """
        This function both format and inserts data data to the table table_name. 
        data is expected to be in json format enclosed within a list.
        """
    def insertData(self, table_name, data):
        try:
            response = self.db.table(table_name).insert(data).execute()
            return response
        except Exception as exception:
            return exception
    
        """
        This function deletes all rows from the specified database whose date 
        attribute is before the specified date date
        """
    def purgeData(self, table_name, date):
        response = self.db.table(table_name).delete().lt("date", date).execute()
        try:
            return response
        except Exception as exception:
            return exception
        



