import praw
from threading import Thread
import logging
import keyring
import yagmail

keyring.get_keyring()

secret = keyring.get_password('reddit', 'secret')
client_id = keyring.get_password('reddit', 'client_id')

user_agent = "script:com.ghandifixer:v1.0 (by /u/GandhiNotGhandiBot)"

username = "GandhiNotGhandiBot"
password = keyring.get_password('reddit', 'user')

reddit = praw.Reddit(client_id=client_id,
                     client_secret=secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

subreddit = reddit.subreddit('civ')

def main():
    init_logger()
    submissions_thread = Thread(target=get_sumbmissions)
    submissions_thread.start()
    comments_thread = Thread(target=get_comments)
    comments_thread.start()


def get_sumbmissions():
    submission_count = 0
    mistake_count = 0
    try:
        for submission in subreddit.stream.submissions():
            submission_count += 1
            words = submission.title.split() + submission.selftext.split()
            if contains_ghandi(words):
                print("Sub: ", submission.url)
                mistake_count += 1
    except (APIException, ClientException, PRAWException) as ex:
        logging.error(ex.message)
        send_email(ex.message)
    finally:
        print("Submissions %d" % submission_count)
        print("Mistakes %d" % mistake_count)
        logging.error("get_sumbmissions() finally block executed")
        send_email()

def get_comments():
    comments_count = 0
    mistake_count = 0
    try:
        for comment in subreddit.stream.comments():
            comments_count += 1
            words = comment.body
            if contains_ghandi(words):
                print("Comm: ", comment.body)
                mistake_count += 1
    except (APIException, ClientException, PRAWException) as ex:
        logging.error(ex.message)
        send_email(ex.message)
    finally:
        print("Comments %d" % comments_count)
        print("Mistakes %d" % mistake_count)
        logging.error("get_comments() finally block executed")
        send_email()

def contains_ghandi(content):
    if ("Ghandi" or "ghandi") in content:
        return True
    else:
        return False

def send_email(message=None):
    print("email error: ", message)
    yag = yagmail.SMTP('bcgroom')
    subject = 'An error with GandhiNotGhandiBot has occurred'
    body = message
    yag.send(subject = subject, contents = body)

def init_logger():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.WARNING, filename="debug.txt")
    logging.info('Logging app started')



if __name__ == "__main__" : main()
