import palette
import tweepy
import random
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from urllib import request as urlrequest
from os import environ
from dotenv import load_dotenv

load_dotenv()

HEX_VALUES = '123456789ABCDEF'
CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = environ['TWITTER_ACCESS_SECRET']

def get_rand_hex():
    """
    Returns a random hex color code.
    """
    rand_hex = ''
    for _ in range(6):
        rand_hex += random.choice(HEX_VALUES)
    return rand_hex

# def get_color_img(hex_code):
#     """
#     Retrieves an image of the specified color from the internet.
#     """
#     link = 'https://www.colorhexa.com/' + hex_code + '.png'
#     path = 'img/' + link.split('/')[-1]
#     urllib.request.urlretrieve(link, path)


def post_tweet(img, hex_code):
    """
    Creates and posts a tweet with the color name, image, rgb and hex code. 
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    name = '"' + palette.colors.get(hex_code).upper() + '"'             # get color name 
    rgb = str(tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4)))       # get color rgb 
    status = name + '\n' + rgb + '\n#' + hex_code                       # create tweet status
    api.update_with_media(img, status)


def main():
    hex_code = ''

    # Ensure that hex code can be found in palette.py
    with open('archive.txt', 'r+') as filename:
        archive = filename.read()
        while hex_code not in palette.colors or hex_code in archive:
            hex_code = get_rand_hex()
        filename.write(hex_code + '\n')
        


    # Retrieve an image of the specified color from the internet
    link = 'https://www.colorhexa.com/' + hex_code + '.png'
    path = 'img/' + link.split('/')[-1]
    urlrequest.urlretrieve(link, path)

    # Configure proxy for PythonAnywhere 
    # proxy_host = 'proxy.server:3128'  # host and port of proxy
    # req = urlrequest.Request(link)
    # req.set_proxy(proxy_host, 'https')
    

    # Set schedule to post tweet every day at 4:20PM (PST)
    sched = BlockingScheduler(timezone='US/Pacific')
    sched.add_job(lambda: post_tweet(path, hex_code), 'cron', hour=16, minute=20)
    sched.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        sched.shutdown()

    # schedule.every().day.at('12:00').do(lambda: post_tweet(path, hex_code))
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # post_tweet(path, hex_code)


if __name__ == '__main__':
    main()
    
# api.media_upload('COLOR BOT, reporting in live!')
# USE https://www.colorhexa.com/######.png
