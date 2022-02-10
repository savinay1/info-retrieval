# Read-only instance
import praw as praw

import pandas as pd


reddit_read_only = praw.Reddit(client_id="SvCJdstpGCed5uhK7XJyIw",  # your client id
                               client_secret="avt5nZXQqLbwyUvyWns6L90I_8M-EQ",  # your client secret
                               user_agent="inforetrieval")  # your user agent

# Authorized instance
reddit_authorized = praw.Reddit(client_id="SvCJdstpGCed5uhK7XJyIw",  # your client id
                                client_secret="avt5nZXQqLbwyUvyWns6L90I_8M-EQ",  # your client secret
                                user_agent="inforetrieval",  # your user agent
                                username="AnyAcanthocephala173",  # your reddit username
                                password="Beyblade123@")

# subreddit = reddit_read_only.subreddit("redditdev")
#
# # Display the name of the Subreddit
# print("Display Name:", subreddit.display_name)
#
# # Display the title of the Subreddit
# print("Title:", subreddit.title)
#
# # Display the description of the Subreddit
# print("Description:", subreddit.description)

subreddit = reddit_read_only.subreddit("movies")



posts = subreddit.hot(limit=5)
# Scraping the top posts of the current month

posts_dict = {"Title": [], "Post Text": [],
              "ID": [], "Score": [],
              "Comments": [], "Post URL": []
              }

for post in posts:
    # Title of each post
    posts_dict["Title"].append(post.title)

    # Text inside a post
    posts_dict["Post Text"].append(post.selftext)

    # Unique ID of each post
    posts_dict["ID"].append(post.id)

    # The score of a post
    posts_dict["Score"].append(post.score)

    # Total number of comments inside the post
    comments=""
    for commentid,comment in enumerate(post.comments):
        comments+=str(commentid)+". "+str(comment.body)+"\n"
        if commentid==5:
            break
    posts_dict["Comments"].append(comments)

    # URL of each post
    posts_dict["Post URL"].append(post.url)

# Saving the data in a pandas dataframe
top_posts = pd.DataFrame(posts_dict)
top_posts.to_csv("Top Posts.csv", index=True)

print(top_posts)