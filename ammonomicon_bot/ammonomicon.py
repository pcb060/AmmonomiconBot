# https://github.com/yashar1/reddit-comment-bot
import praw
import wiki_parser as wp
import db_manager as dbm
from dotenv import load_dotenv
from utils import format_to_comment, comment_help
import json
import time
import os
import re
from datetime import datetime


def bot_login():
    """Logs the bot into reddit through praw
    """
    print("SYSTEM: Logging in...")
    reddit = praw.Reddit(
        client_id=os.getenv("client_id"),
        client_secret=os.getenv("client_secret"),
        password=os.getenv("password"),
        user_agent=os.getenv("user_agent"),
        username=os.getenv("username"),
    )
    print("SYSTEM: Logged in!")

    return reddit


def search_and_reply(reddit):
    """Searches last 1000 comments in subreddit for requests and replies
    """
    print("SEARCH: Searching last 1,000 comments...")

    for comment in reddit.subreddit("EnterTheGungeon").comments(limit=1000):
        if is_request(comment.body) and not has_been_replied_to(str(comment.id)):
            reqs = re.findall(r"{(.*?)}", comment.body)

            if isinstance(reqs, list):
                tmp = list()
                for i in reqs:
                    print('SEARCH: Request for "' + i.strip() + '" received!')
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
                print('SEARCH: Request for "' + reqs.strip() + '" received!')
                res = format_to_comment(dbm.get_entry(reqs))
                res += "\n" + comment_help()

            comment.reply(res)
            print("SYSTEM: Replied to comment " + comment.id)
    print("SEARCH: Search Completed.")


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
    """Retrieve last datetime written to updatetime.txt
    """
    try:
        timefile = open("updatetime.txt", "r")
        t = timefile.readline()
        if t != "":
            return datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        else:
             return datetime(1900, 1, 1)
    except:
        print(
            "!!! WARNING!!! UPDATE: Something went wrong while trying to get the last update time."
        )


def set_last_update(time):
    """Write datetime to updatetime.txt
    """
    try:
        timefile = open("updatetime.txt", "w")
        timefile.write(str(time))
    except:
        print(
            "!!! WARNING!!! UPDATE: Something went wrong while trying to set the last update time."
        )


def reset_db():
    """Resets db.json in order to remove outdated/redundant entries
    """
    try:
        print("SYSTEM: Resetting database...")
        empty_json = {'_default' : {}}
        dbfile = open("ammonomicon_bot/dbs/db.json", "w")
        json.dump(empty_json, dbfile)
    except:
        print(
            "!!! WARNING!!! SYSTEM: Something went wrong while trying to reset the database"
        )

def update_db():
    """Updates entry database
    """
    try:
        print(
            "UPDATE: Updating the database... (last update: " +
            str(get_last_update()) + ")"
        )
        wp.parse_enemies()
        wp.parse_guns()
        wp.parse_items()
        print("UPDATE: Update completed!")
        set_last_update(datetime.now())
    except:
        print(
            "!!! WARNING!!! UPDATE: Something went wrong while trying to update the database. Update will be skipped."
        )


load_dotenv()
days_between_db_updates = int(os.getenv("days_between_db_updates"))
reddit = bot_login()

# updates entry database if a week has passed since last update
if (datetime.now() - get_last_update()).days >= days_between_db_updates:
    reset_db()
    update_db()
else:
    print("SYSTEM: Skipping update. (last update: " + str(get_last_update()) + ")")
search_and_reply(reddit)
