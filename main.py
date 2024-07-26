import os
import instaloader

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

L = instaloader.Instaloader()
L.load_session_from_file(os.getenv("INSTAGRAM_USER"), os.getenv("INSTAGRAM_SESSION"))

# Purging old events
accounts = db.getData(ACCOUNTS_TABLE, "club_name")
purge_date = datetime.today() - timedelta(days=90)
db.purgeData(ACCOUNTS_TABLE, purge_date)

start_date = datetime.today() - timedelta(days=7)
end_date = datetime.today()

# Getting new Events
unfiltered_data = fetchData(accounts, start_date, end_date, L)

print(unfiltered_data)

# TODOS:

# 1. Error Handling for Instaloader
# Sometimes Instaloader throws errors that can be resolved by rerunning the scipt
# Find a way to todo this

# 2. Refining Prompt Template
# The output of LLAMA,predict_post is not exactly what we want. Fixing the prompt
# template defined in constatns.py or by manually fixing the input

# 3. Timing calls to HuggingFace Inference API
# If the data exceeds a certain size, space out the calls to the HuggingFace Inference 
# API ie the predict_post function in inference.py

# Predict content and extract dates from post
for post in unfiltered_data:
    result = LLAMA.predict_post(post=post)
    print(result)
    
# Insert into databse
# db.insertData(DATA_TABLE, unfiltered_data)