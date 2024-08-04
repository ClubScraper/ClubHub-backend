## Data Wrangling for Uoft Club HUB

This repository contains code that scrapes the latest posts from Instagram accounts oultined in the Supabase table ACCOUNTS_TABLE obtaining their captions and posting date. Using Llama 3.1, it then classifies these posts into four categories 'Competition', 'Networking/Orientation', 'Workshop/Review Seminar', 'Hiring', or 'Misc' to then be uploaded into the Supabase table DATA_TABLE. 

</b>

A .env file is expected with the following contents:

```python
SUPABASE_URL=""
SUPABASE_KEY=""
HUGGING_FACE_TOKEN=""
TF_ENABLE_ONEDNN_OPTS=0
HUGGING_FACE_TOKEN_2=""
INSTAGRAM_USER=""
INSTAGRAM_PASS=""
INSTAGRAM_SESSION=""
```

To run this repository, clone and then do the following:

```bash
$ cd DataWrangling
$ venv/Scripts/activate
$ pip -r install requirements.txt
```