import os
import instaloader
import re
import json

from datetime import datetime, timedelta
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from scraper import fetchData, fetchDataNoLogin
from database import Database
from inference import Inference
from constants import ACCOUNTS_TABLE, DATA_TABLE, MODEL

load_dotenv()

db = Database()
LLAMA = Inference(model=MODEL, token=os.getenv("HUGGING_FACE_TOKEN"))

L = instaloader.Instaloader()
L.load_session_from_file(os.getenv("INSTAGRAM_USER"), os.getenv("INSTAGRAM_SESSION"))

# Purging old events
accounts = db.getData(DATA_TABLE, "account")
purge_date = datetime.today() - timedelta(days=90)
db.purgeData(DATA_TABLE, purge_date)

start_date = datetime.today() - timedelta(days=7)
end_date = datetime.today()

# Getting new Events
# Getting new Events
unfiltered_data = fetchData(accounts, start_date, end_date, L)
if (unfiltered_data == []):
    unfiltered_data = fetchDataNoLogin(accounts, start_date, end_date)


# TODOS:



# 2. Refining Prompt Template
# The output of LLAMA,predict_post is not exactly what we want. Fixing the prompt
# template defined in constatns.py or by manually fixing the input

# 3. Timing calls to HuggingFace Inference API
# If the data exceeds a certain size, space out the calls to the HuggingFace Inference 
# API ie the predict_post function in inference.py

predictions = []

# Predict content and extract dates from post
for post in unfiltered_data:
    predictions.append(LLAMA.predict_post(post=post))

print(predictions)

to_upload = []
pattern = re.compile(r'\{.*\}')
for prediction in predictions:
    match = pattern.search(prediction)
    if match:
        dict = match.group(0)
        result = json.loads(dict)
        to_upload.append(result)

print(to_upload)

# Insert into databse
for i in range(0, len(to_upload)):
    if (to_upload[i].get("type") != 'Misc.' and to_upload[i].get("relevant_dates") != ''):
        to_upload[i]['caption'] = unfiltered_data[i]['caption']
        db.insertData(DATA_TABLE, to_upload[i])



print(to_upload)