from datetime import datetime
from itertools import dropwhile, takewhile
import instaloader

L = instaloader.Instaloader()

posts = instaloader.Profile.from_username(L.context, "web3.uoft").get_posts()

SINCE = datetime(2024, 8, 5)
UNTIL = datetime(2024, 5, 8)

for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):
    print(post.date)
    L.download_post(post, "web3.uoft")