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


def search_and_reply(reddit, comments_replied_to, seconds_of_sleep):
    """Searches last 1000 comments in subreddit for requests, replies, then sleeps for seconds_of_sleep seconds
    """
    print("Searching last 1,000 comments...")

    for comment in reddit.subreddit("testingground4bots").comments(limit=1000):
        # if is_request(comment.body) and comment.id not in comments_replied_to:
        if is_request(comment.body) and not has_been_replied_to(comment.id):
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

            comments_replied_to.append(comment.id)

            with open(PATH_TO_COMMENT_IDS, "a") as f:
                f.write(comment.id + "\n")

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
    request = praw.Reddit.comment(request_id)
    request.refresh()
    replies = request.replies.list()
    for r in replies:
        if r.author == "AmmonomiconBot" and r.parent() == request_id:
            return True
    return False


def get_saved_comments():
    """Gets comment IDs inside comments_replied_to.txt
    """
    # if file doesn't exist yet, comments_replied_to is set to an empty list
    if not os.path.isfile(PATH_TO_COMMENT_IDS):
        comments_replied_to = []
    else:
        with open(PATH_TO_COMMENT_IDS, "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to


def get_last_update():
    with open(PATH_TO_UPDATE_DATE, "r") as f:
        return f.read()


def set_last_update():
    with open(PATH_TO_UPDATE_DATE, "w") as f:
        f.write(str(datetime.datetime.now()))


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
comments_replied_to = get_saved_comments()
update_db()

while True:
    search_and_reply(reddit, comments_replied_to, 10)
    # updates entry database if a week has passed since last update
    if (
        datetime.datetime.now()
        - datetime.datetime.strptime(get_last_update(), "%Y-%m-%d %H:%M:%S.%f")
    ).days >= 7:
        update_db()
