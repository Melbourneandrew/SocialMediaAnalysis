from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache

# from RedditData import get_oauth_token, get_reddit_data, reddit_test_data
# from Analysis import analyze

app = Flask(__name__)
CORS(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)


@app.route("/")
def test():
    data = {
        "hello": "world :)"
    }
    return jsonify(data)


# @app.route("/a", methods=['POST'])
# def test2():
#     print("/a endpoint hit")
#     data = {
#         "analysis": "results"
#     }
#     return jsonify(data)
@app.route("/a", methods=['POST'])
def analyze_endpoint():
    body = request.get_json()
    if body is None or len(body['subreddits']) == 0 or len(body['analysis_options']) == 0:
        return {"err": "Invalid request"}

    print(body)
    subreddits = body['subreddits']
    analysis_options = body['analysis_options']

    reddit_oauth_token = cache.get("reddit_oauth_token")
    if reddit_oauth_token is None:
        reddit_oauth_token = get_oauth_token()
        cache.set("reddit_oauth_token", reddit_oauth_token)

    results = {'totals': {}}
    total_posts = 0
    for sub in subreddits:
        reddit_data = get_reddit_data(sub, reddit_oauth_token)
        results[sub] = analyze(reddit_data, analysis_options)
        print(results[sub])
        results[sub]["total_posts"] = len(reddit_data)
        total_posts += len(reddit_data)

    # Calculate averages
    for sub in results:
        for option in results[sub]:
            if option == "total_posts":
                continue
            # Initialize the total label count to 0
            for label in results[sub][option]:
                results['totals'][label] = 0
            # Calculate the average for each label within the subreddit
            for label in results[sub][option]:
                # Tally the total number of posts with this label
                print(results[sub][option][label])
                results['totals'][label] += results[sub][option][label]
                # Calculate the percent of posts with this label in a particular subreddit
                results[sub][option][label] = results[sub][option][label] / results[sub]["total_posts"]

        for label in results['totals']:
            # Calculate the percent of posts with this label in all subreddits
            results['totals'][label] = results['totals'][label] / total_posts
    return results
