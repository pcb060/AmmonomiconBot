# https://github.com/yashar1/reddit-comment-bot
import praw
import wiki_parser as wp
import db_manager as dbm
from utils import format_to_comment, comment_help
from conf.txt_files import PATH_TO_COMMENT_IDS, PATH_TO_UPDATE_DATE
import time
import os
import re
import datetime


def bot_login():
    """Logs the bot into reddit through praw
    """
    print("Logging in...")
    reddit = praw.Reddit(
        client_id=os.environ["client_id"],
        client_secret=os.environ["client_secret"],
        password=os.environ["password"],
        user_agent=os.environ["user_agent"],
        username=os.environ["username"],
    )
    print("Logged in!")

    return reddit


def search_and_reply(reddit, seconds_of_sleep):
    """Searches last 1000 comments in subreddit for requests, replies, then sleeps for seconds_of_sleep seconds
    """
    print("Searching last 1,000 comments...")

    for comment in reddit.subreddit("testingground4bots").comments(limit=1000):
        if is_request(comment.body) and not has_been_replied_to(str(comment.id)):
            reqs = re.findall(r"{(.*?)}", comment.body)

            if isinstance(reqs, list):
                tmp = list()
                for i in reqs:
                    print('Request for "' + i.strip() + '" received!')
                    tmp.append(format_to_comment(dbm.get_entry(i)))
                    # add separator between every request found except last one
                    if i != reqs[len(reqs) - 1]:
                        tmp.append("\n___\n")
                    # add help line if last request was appended
                    else:
                        tmp.append("\n" + comment_help())

                # unifies tmp items inside a single 'res' string
                res = ""
                ind = 0
                for i in tmp:
                    res += tmp[ind]
                    ind += 1

            else:
                print('Request for "' + reqs.strip() + '" received!')
                res = format_to_comment(dbm.get_entry(reqs))
                res += "\n" + comment_help()

            comment.reply(res)
            print("Replied to comment " + comment.id)

    print("Search Completed.")
    print("Sleeping for " + str(seconds_of_sleep) + " seconds...")
    time.sleep(seconds_of_sleep)


def is_request(text):
    """Checks if text contains a valid request (entry inside braces '{ }')
    """
    return bool(re.search(r"[{][a-zA-Z0-9 '-+.]*[}]", text))


def has_been_replied_to(request_id):
    """Returns True if the comment with id request_id has already received a reply by the bot, False otherwise
    """
    request = reddit.comment(request_id)
    request.refresh()
    replies = request.replies.list()
    for r in replies:
        if r.author == "AmmonomiconBot" and str(r.parent()) == str(request_id):
            return True
    return False


def get_last_update():
    return last_update


def set_last_update():
    global last_update
    last_update = datetime.datetime.now()


def update_db():
    """Updates entry database
    """
    try:
        print("Updating the database... (last update: " + get_last_update() + ")")
        wp.parse_enemies()
        wp.parse_guns()
        wp.parse_items()
        print("Update completed!")
        set_last_update()
    except:
        print(
            "Something went wrong while trying to update the database. Update will be skipped."
        )


reddit = bot_login()
last_update = None
update_db()

while True:
    search_and_reply(reddit, 10)
    # updates entry database if a week has passed since last update
    if (datetime.datetime.now() - get_last_update()).days >= 7:
        update_db()
