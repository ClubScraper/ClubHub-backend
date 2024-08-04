import os
from huggingface_hub import InferenceClient

from dotenv import load_dotenv
from constants import prompt_template
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

class Inference:
    def __init__(self, model, token):
        self.model = client = InferenceClient(model, token=token)
    
    def predict_post(self, post):
        prompt = prompt_template.format(account=post['account'], 
                                        date=post['date'], 
                                        caption=post['caption'])
        response = self.model.text_generation(prompt=prompt)
        return response
    
    