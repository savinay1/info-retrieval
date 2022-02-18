# Read-only instance
import praw as praw
import re

import pandas as pd
import time


reddit_read_only = praw.Reddit(client_id="SvCJdstpGCed5uhK7XJyIw",  # your client id
                               client_secret="avt5nZXQqLbwyUvyWns6L90I_8M-EQ",  # your client secret
                               user_agent="inforetrieval")  # your user agent

# Authorized instance
reddit_authorized = praw.Reddit(client_id="SvCJdstpGCed5uhK7XJyIw",  # your client id
                                client_secret="avt5nZXQqLbwyUvyWns6L90I_8M-EQ",  # your client secret
                                user_agent="inforetrieval",  # your user agent
                                username="AnyAcanthocephala173",  # your reddit username
                                password="Beyblade123@")


subreddit = reddit_read_only.subreddit("netflix")
timestart=time.time()
#
posts = subreddit.top(limit=50000)

posts_dict = {"Post Text":[],"Comments": [] }

for post in posts:
    post=reddit_read_only.submission(id=post.id)
    post.comments.replace_more(limit=0)
    if len(post.comments) < 100:
        continue
    for commentid,comment in enumerate(post.comments):
        posts_dict["Post Text"].append(re.sub("&.*"," ",post.selftext))
        posts_dict["Comments"].append(re.sub("&.*"," ",comment.body))
        title = post.title.replace("/", " ")
        if (commentid+1)%10==0:
            top_posts = pd.DataFrame(posts_dict)
            top_posts.to_csv("csv/" + title[0:min(len(title), 50)] + str(commentid+1) + ".csv", index=True)
            posts_dict["Post Text"] = []
            posts_dict["Comments"] = []


timednd=time.time()
print(timednd-timestart)