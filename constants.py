ACCOUNTS_TABLE="club_accounts"
DATA_TABLE="test"

MODEL="meta-llama/Meta-Llama-3-8B-Instruct"


prompt_template = """
Given the following Instagram post data:

Account: {account}
Date: {date}
Caption: {caption}

Extract the following information and return it in this format with NO EXPLANATIONS:
- Account (as 'account')
- Posting Date (as 'posting_date')
- Type of post ('Competition', 'Networking/Orientation', 'Workshop/Review Seminar', 'Hiring', or 'Misc.')
- Relevant Dates (dates mentioned in the caption, EXCLUDE THE DATE POSTED, EXCLUDE DATES IN THE PAST, MUST BE IN YYYY/MM/DD FORMAT) If the event happened in the past, put '', and please 
coordinate dates accordingly (for example, if the post date is 7/26/24, a Friday, and the captions mentions an event taking place THIS Saturday, the relevant
date will be 7/27/24, a Saturday).

Only return the data in the response AS A DICTIONARY. DO NOT INCLUDE ANY EXPLANATIONS, CODE, OR RAW DATA.
PLEASE EXCLUDE ANY STATEMENTS SUCH AS "import re, import json, def extract_info, ''', #, Note: ", etc.

Response format: {{"account": "{account}", "posting_date": "{date}", "type": "<Type>", "relevant_dates": "<Relevant Dates>"}}

ONLY OUTPUT THE LIST, NO EXPLANATIONS, # COMMENTS, DUPLICATE DATA, NOTES, OR EXTRA TEXT.
"""