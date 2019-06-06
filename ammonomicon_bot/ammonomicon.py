# https://github.com/yashar1/reddit-comment-bot
import praw
import ammonomicon_bot.wiki_parser as wp
from ammonomicon_bot.utils import format_to_comment
import time
import os
import re


def bot_login():
    print("Logging in...")
    reddit = praw.Reddit("Ammonomicon")
    print("Logged in!")

    return reddit


def run_bot(reddit, comments_replied_to):
    print("Searching last 1,000 comments")

    for comment in reddit.subreddit("testingground4bots").comments(limit=1000):
        # and comment.author != reddit.user.me()
        if is_request(comment.body) and comment.id not in comments_replied_to:
            reqs = re.findall("\{(.*?)\}", comment.body)

            if isinstance(reqs, list):
                res = None
                for i in reqs:
                    print('Request for "' + i.strip() + '" received')
                    res += wp.get_entry(i)
                    if i != reqs[len(reqs) - 1]:
                        res += "\n___\n"
            else:
                print('Request for "' + reqs.strip() + '" received')
                res = wp.get_entry(reqs)

            comment.reply(format_to_comment(res))
            print("Replied to comment " + comment.id)

            comments_replied_to.append(comment.id)

            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Search Completed.")

    print(comments_replied_to)

    print("Sleeping for 10 seconds...")
    # Sleep for 10 seconds...
    time.sleep(10)


# looks for a request inside braces in comment
def is_request(text):
    return bool(re.search("[\{][a-zA-Z0-9 '\-\+\.]*[\}]", text))


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to


reddit = bot_login()
comments_replied_to = get_saved_comments()

while True:
    run_bot(reddit, comments_replied_to)
