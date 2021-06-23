import tweepy
import palette
import random
import time
import schedule
from urllib import request as urlrequest
import os 
from os import environ

HEX_VALUES = '123456789ABCDEF'
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

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
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
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
        

    # Configure proxy for PythonAnywhere 
    # proxy_host = 'proxy.server:3128'  # host and port of proxy

    # Retrieve an image of the specified color from the internet
    link = 'https://www.colorhexa.com/' + hex_code + '.png'
    # req = urlrequest.Request(link)
    # req.set_proxy(proxy_host, 'https')
    path = 'img/' + link.split('/')[-1]
    urlrequest.urlretrieve(link, path)

    # Set schedule to post tweet every day at 4:20PM (PST)
    schedule.every().day.at('16:20').do(lambda: post_tweet(path, hex_code))
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
    
# api.media_upload('COLOR BOT, reporting in live!')
# USE https://www.colorhexa.com/######.png
