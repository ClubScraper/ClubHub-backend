import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    token=os.getenv("HUGGING_FACE_TOKEN")
)

template = """
Given the following Instagram post data:

Account: {account}
Date: {date}
Caption: {caption}

Extract the following information and return it in the specified JSON format:
- Account (as 'account')
- Posting Date (as 'posting_date')
- Type of post (can be 'New Event', 'Old Event', or 'Hiring')
- Relevant Dates (dates mentioned in the caption)

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

def generate_prompt(account, date, caption):
    return template.format(account=account, date=date, caption=caption)

account = 'amacss_utsc'
date = '2024/07/03'
caption = """🚨 Executive Team Hiring is Live! 🚨

❗️We're looking for people who are motivated to make a difference in the CMS community through AMACSS for the 2024-2025 year❗️

🕐 Applications are due July 12 but will be reviewed on a rolling basis.

🔗 Apply now with the link in our bio!"""

prompt = generate_prompt(account, date, caption)


response = client.text_generation(prompt)
print(response)
