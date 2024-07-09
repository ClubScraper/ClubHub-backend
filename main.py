import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from scraper import fetchData
from database import Database
from inference import Inference
from constants import ACCOUNTS_TABLE, DATA_TABLE, MODEL

load_dotenv()

db = Database()
LLAMA = Inference(model=MODEL, token=os.getenv("HUGGING_FACE_TOKEN"))

# Purging old events
accounts = db.getData(ACCOUNTS_TABLE, "club_name")
purge_date = datetime.today() - timedelta(days=90)
db.purgeData(ACCOUNTS_TABLE, purge_date)

start_date = datetime.today() - timedelta(days=7)
end_date = datetime.today()

# Getting new Events
unfiltered_data = fetchData(accounts, start_date, end_date)

print(unfiltered_data)

# Predict content and extract dates from post
for post in unfiltered_data:
    result = LLAMA.predict_post(post=post)
    print(result)
    
# Insert into databse
# db.insertData(DATA_TABLE, unfiltered_data)