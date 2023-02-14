# This token will be valid for ~2 hours
import os
import requests
from dotenv import load_dotenv
load_dotenv()


def get_data():
    oauth_token = get_oauth_token()
    headers = {'User-Agent': 'sentiment-analysis/0.0.1',
               'Authorization': f"bearer {oauth_token}"}
    res = requests.get("https://oauth.reddit.com/r/python/hot",
                       headers=headers)
    
    posts = res.json()["data"]["children"]

    for post in posts:
        print(post["data"]["title"])

    


def get_oauth_token():
    print("getting oauth token")
    reddit_api_id = os.environ.get("REDDIT_API_ID")
    reddit_api_secret = os.environ.get("REDDIT_API_SECRET")
    reddit_username = os.environ.get("REDDIT_USERNAME")
    reddit_password = os.environ.get("REDDIT_PASSWORD")

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(reddit_api_id, reddit_api_secret)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': reddit_username,
            'password': reddit_password}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'sentiment-analysis/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    return TOKEN

    # # add authorization to our headers dictionary
    # headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

    # # while the token is valid (~2 hours) we just add headers=headers to our requests
    # requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


if __name__ == '__main__':
    get_data()
