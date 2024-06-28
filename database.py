from supabase import create_client, Client
from define import KEY, URL

class Database:
    def __init__(self):
        self.db: Client = create_client(URL, KEY)
    
    def getData(self, table_name, column):      
        response = self.db.table(table_name).select("*").execute()
        data = [d[column] for d in response.data]
        return data

        """
        This function both format and inserts data data to the table table_name. 
        data is expected to be in the format {account: [(date, caption)]}.
        """
    def insertData(self, table_name, data):
        # The following code formats the data so that it can be easily uploaded to our DB
        formatted_data = []
        index = 1
        for account in data:
            for post in data[account]:
                row = {"id": index, "account": account, "date": post[0], 
                       "caption": post[1]}
                index += 1
                formatted_data.append(row)
            
        try:
            response = self.db.table(table_name).insert([formatted_data]).execute()
            return response
        except Exception as exception:
            return exception
    
        """
        This function deletes all rows from the specified database whose date attribute is before the specified date
        """
    def purgeData(self, table_name, date):
        self.db.table(table_name).delete().lt("date", date).execute()
        

        

