from apscheduler.schedulers.blocking import BlockingScheduler

import requests

import tweepy

from local_settings import TWITTER_API_KEY
from local_settings import TWITTER_SECRET
from local_settings import TWITTER_ACCESS_TOKEN
from local_settings import TWITTER_ACCESS_SECRET


sched = BlockingScheduler()


sched.week = 4
sched.snap_percentage = 98.1


@sched.scheduled_job('cron',
                     minute="*/15",
                     hour="*/15",
                     day="*",
                     month="9-12",
                     day_of_week="0,1,4")
def check_snap_count():
    print("Checking snap count...")
    result = requests.get('https://api.lineups.com/nfl/'
                          'fetch/snaps/2021/QB?season_type=1')

    if result.status_code == 200:
        data = result.json()

        for player in data['data']:
            if player['full_name'] == "Carson Wentz":
                if len(player['weeks']) > sched.week and sched.snap_percentage != player['season_snap_percent']:
                    sched.week = len(player['weeks'])
                    sched.snap_percentage = player['season_snap_percent']

                    return tweet_snap_count(player['season_snap_percent'])


def tweet_snap_count(snap_percentage):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY,
                               TWITTER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN,
                          TWITTER_ACCESS_SECRET)

    twitter = tweepy.API(auth)

    tweet = construct_tweet(snap_percentage)

    print("Tweeting this: {0}".format(tweet))

    return twitter.update_status(tweet)


def generate_chart(snap_percentage):
    progress = int(round((snap_percentage * 0.15), 0))
    remaining = 15 - progress

    chart = ""

    for i in range(0, progress):
        chart += "▓"

    for i in range(0, remaining):
        chart += "░"

    chart += " {0}%".format(snap_percentage)

    return chart


def construct_tweet(snap_percentage):
    if snap_percentage >= 90:
        tweet = "Wentz is solidly above the snaps needed for Philly to get " \
                "a first round pick."
    elif snap_percentage >= 80:
        tweet = "Wentz remains above the snaps needed for Philly to get " \
                "a first round pick."
    elif snap_percentage >= 77:
        tweet = "Wentz is just above the snaps needed for Philly to get " \
                "a first round pick."
    elif snap_percentage >= 75:
        tweet = "Wentz is barely above the snaps needed for Philly to get " \
                "a first round pick."
    elif snap_percentage >= 70:
        tweet = "Wentz is just below the snaps needed for Philly to get " \
                "a first round pick."
    elif snap_percentage >= 60:
        tweet = "Wentz is below the snaps needed for Philly to get " \
                "a first round pick."
    else:
        tweet = "Wentz is well below the snaps needed for Philly to get " \
                "a first round pick."

    chart = generate_chart(snap_percentage)

    return "{0}\n\n{1}".format(tweet, chart)


if __name__ == "__main__":
    sched.start()
