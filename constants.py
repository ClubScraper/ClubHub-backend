ACCOUNTS_TABLE="club_accounts"
DATA_TABLE="test"

MODEL="meta-llama/Meta-Llama-3-8B-Instruct"


prompt_template = """
Given the following Instagram post data:

Account: {account}
Date: {date}
Caption: {caption}

Extract the following information and return it in the specified JSON format:
- Account (as 'account')
- Posting Date (as 'posting_date')
- Type of post (can be 'New Event', 'Old Event', 'Hiring' or 'Misc.')
- Relevant Dates (dates mentioned in the caption) If there are no relevant dates, put '' 

Only return the JSON data in the response. Do not include any explanations.

Example response format:
{{
  "account": "{account}",
  "posting_date": "{date}",
  "type": "<Type>",
  "relevant_dates": "<Relevant Dates>"
}}

Please provide the information based on the given data in JSON format only.
"""