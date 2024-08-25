import os
import re
import json
import logging

from datetime import datetime, timedelta
import instaloader
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import backoff

from scraper import fetchData, fetchDataNoLogin
from database import Database
from inference import Inference
from constants import (
    UTM_NAMES,
    UTSG_NAMES,
    UTSC_NAMES,
    UTM_POSTS,
    UTSC_POSTS,
    UTSG_POSTS,
    MODEL,
    PROMPT_TEMPLATE,
    PURGE_BEFORE,
    START_DELTA
)

# Setting up

logger = logging.getLogger("ClubHUB")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs.txt")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%m/%d/%H:%M')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

database = Database()
LLAMA = Inference(model=MODEL, token=os.getenv("HUGGING_FACE_TOKEN"))
L = instaloader.Instaloader() 

name_tables = [UTM_NAMES, UTSC_NAMES, UTSG_NAMES]
post_tables = [UTM_POSTS, UTSC_POSTS, UTSC_POSTS]

for name_table, post_table in zip(name_tables, post_tables):
    
    # Deleting Events Older than PURGE_BEFORE
    database.purgeData(post_table, PURGE_BEFORE)
    
    # Getting New Events
    accounts = database.getData(name_table, "account")
    departments = database.getData(name_table, "department")
    names = database.getData(name_table, "name")
    
    start_date = datetime.today() - timedelta(days=START_DELTA)
    end_date = datetime.today()

    unfiltered_data = fetchData(accounts, start_date, end_date, L)
    if (unfiltered_data == []):
        unfiltered_data = fetchDataNoLogin(accounts, start_date, end_date)

    predictions = []

    # Predict content and extract dates from post
    for post in unfiltered_data:
        predictions.append(LLAMA.predict_post(post=post))

    to_upload = []
    pattern = re.compile(r'\{.*\}')
    for prediction in predictions:
        match = pattern.search(prediction)
        if match:
            dict = match.group(0)
            result = json.loads(dict)
            to_upload.append(result)

    # Insert into databse
    for i in range(0, len(to_upload)):
        if (to_upload[i].get("type") != 'Misc.' and to_upload[i].get("relevant_dates") != ''):
            to_upload[i]['caption'] = unfiltered_data[i]['caption']
            database.insertData(post_table, to_upload[i])

    logger.debug(f"Summary: {len(predictions)} events scraped and processed.")