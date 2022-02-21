# Read-only instance
import praw as praw
import re
import pandas as pd
import time


reddit_read_only = praw.Reddit(client_id="SvCJdstpGCed5uhK7XJyIw",  # your client id
                               client_secret="avt5nZXQqLbwyUvyWns6L90I_8M-EQ",  # your client secret
                               user_agent="inforetrieval")  # your user agent


#
# posted_after = int(datetime.datetime(2009, 1, 1).timestamp())
# posted_before = int(datetime.datetime(2021, 12,30 ).timestamp())

#posts = psraw.submission_search(reddit_authorized,subreddit="TrueFilm",limit=None)
subreddit = reddit_read_only.subreddit("TrueFilm")
subreddit2 = reddit_read_only.subreddit("MovieSuggestions")
subreddit3= reddit_read_only.subreddit("movies")

postsl=[]
posts = subreddit.top(limit=None)
postsl.append(posts)
postsl.append(subreddit2.top(limit=None))
postsl.append(subreddit3.top(limit=None))
posts_dict = {"Post Text":[],"Comments": [] }
posts_replies = {"Comments":[],"Replies": [] }
for posts in postsl:
    for post in posts:
        post=reddit_read_only.submission(id=post.id)
        post.comments.replace_more(limit=0)
        if len(post.comments) < 10:
            continue
        count=0
        for commentid,comment in enumerate(post.comments.list()):
            posts_dict["Post Text"].append(re.sub("&.*"," ",post.selftext))
            posts_dict["Comments"].append(re.sub("&.*"," ",comment.body))
            title = post.title.replace("/", " ")
            if len(comment.replies) >0:
                for replyid,reply in enumerate(comment.replies):
                    posts_replies["Comments"].append(re.sub("&.*", " ", comment.body))
                    posts_replies["Replies"].append(re.sub("&.*", " ", reply.body))
                    if (replyid + 1) % 10 == 0:
                        top_posts = pd.DataFrame(posts_replies)
                        top_posts.to_csv("csv/" + title[0:min(len(title), 50)] + "Replies"+str(replyid + 1) + ".csv", index=True)
                        posts_replies["Comments"] = []
                        posts_replies["Replies"] = []
                top_posts = pd.DataFrame(posts_replies)
                top_posts.to_csv("csv/" + title[0:min(len(title), 50)] + "Replies" + str(replyid + 1) + ".csv", index=True)
                posts_replies["Comments"] = []
                posts_replies["Replies"] = []

            if (commentid+1)%10==0:
                top_posts = pd.DataFrame(posts_dict)
                top_posts.to_csv("csv/" + title[0:min(len(title), 50)] + str(commentid+1) + ".csv", index=True)
                posts_dict["Post Text"] = []
                posts_dict["Comments"] = []
        top_posts.to_csv("csv/" + title[0:min(len(title), 50)] + str(commentid + 1) + ".csv", index=True)
        posts_dict["Post Text"] = []
        posts_dict["Comments"] = []

timednd=time.time()
