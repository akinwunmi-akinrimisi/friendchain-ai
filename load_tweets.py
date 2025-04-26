import json

def load_tweets(username):
    try:
        with open(f"{username}_tweets.json", "r") as f:
            tweets = json.load(f)
        print(f"Loaded {len(tweets)} tweets for {username}")
        return tweets
    except Exception as e:
        print(f"Error loading tweets: {e}")
        return []

if __name__ == "__main__":
    # Test with mock user
    username = "alex.base"
    tweets = load_tweets(username)
    # Print first 3 tweets for verification
    for i, tweet in enumerate(tweets[:3], 1):
        print(f"Tweet {i}: {tweet['text']} (Posted: {tweet['created_at']})")