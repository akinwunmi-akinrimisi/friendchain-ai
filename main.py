from fastapi import FastAPI, HTTPException
import json
import tweepy
import ipfshttpclient
from pydantic import BaseModel
from typing import List
import torch
from transformers import DistilBertTokenizer, DistilBertModel
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize
import numpy as np
import random
import os

app = FastAPI()

# NLTK setup
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

# DistilBERT setup
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

# Mock X API setup (replace with real credentials)
X_API_KEY = "your_api_key"
X_API_SECRET = "your_api_secret"
X_ACCESS_TOKEN = "your_access_token"
X_ACCESS_TOKEN_SECRET = "your_access_token_secret"

# IPFS setup (optional)
try:
    ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
except Exception as e:
    print(f"IPFS connection failed: {e}. Storing files locally.")
    ipfs_client = None

class Tweet(BaseModel):
    text: str
    created_at: str

class AvatarRequest(BaseModel):
    username: str
    tweets: List[Tweet] = None

def preprocess_tweets(tweets):
    stop_words = set(stopwords.words('english'))
    cleaned_tweets = []
    for tweet in tweets:
        text = tweet.text.lower()
        text = ' '.join(word for word in text.split() if not (word.startswith('#') or word.startswith('@') or 'http' in word))
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
        cleaned_tweets.append(' '.join(tokens))
    return cleaned_tweets

def extract_features(cleaned_tweets):
    embeddings = []
    for text in cleaned_tweets:
        if not text.strip():
            continue
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(embedding)
    if not embeddings:
        return np.zeros(768)
    return normalize(np.mean(embeddings, axis=0).reshape(1, -1))[0]

def infer_big5_features(features):
    openness = min(0.8 + np.random.uniform(-0.1, 0.1), 1.0)
    conscientiousness = min(0.7 + np.random.uniform(-0.1, 0.1), 1.0)
    extraversion = min(0.6 + np.random.uniform(-0.1, 0.1), 1.0)
    agreeableness = min(0.5 + np.random.uniform(-0.1, 0.1), 1.0)
    neuroticism = min(0.3 + np.random.uniform(-0.1, 0.1), 1.0)
    return {
        "Openness": openness,
        "Conscientiousness": conscientiousness,
        "Extraversion": extraversion,
        "Agreeableness": agreeableness,
        "Neuroticism": neuroticism
    }

def infer_attributes(tweets):
    text = ' '.join(tweet.text.lower() for tweet in tweets)
    interests = []
    if 'ai' in text or 'machine learning' in text or 'distilbert' in text:
        interests.append("Artificial Intelligence")
    if 'blockchain' in text or 'base' in text or 'web3' in text:
        interests.append("Blockchain")
    if 'coding' in text or 'developer' in text:
        interests.append("Coding")
    if 'san francisco' in text or 'sf' in text:
        interests.append("Tech Events")
    values = ["Innovation", "Transparency"] if 'open-source' in text or 'ethics' in text else ["Innovation"]
    goals = ["Build decentralized solutions"] if 'web3' in text else ["Advance technology"]
    communication_style = "Enthusiastic and technical" if any(word in text for word in ['excited', '🔥']) else "Informative"
    return {
        "interests": interests,
        "values": values,
        "goals": goals,
        "communication_style": communication_style
    }

def generate_avatar(tweets, username):
    cleaned_tweets = preprocess_tweets(tweets)
    features = extract_features(cleaned_tweets)
    big5_traits = infer_big5_features(features)
    attributes = infer_attributes(tweets)
    avatar = {
        "username": username,
        "big5_traits": big5_traits,
        "interests": attributes["interests"],
        "values": attributes["values"],
        "goals": attributes["goals"],
        "communication_style": attributes["communication_style"],
        "description": (
            f"{username} is a highly open and conscientious individual, driven by a passion for innovation in technology. "
            f"They thrive in dynamic environments like San Francisco’s tech scene, where they engage with AI, blockchain, and coding. "
            f"Their communication is enthusiastic and technical, often sharing insights with excitement. "
            f"With a goal to build decentralized solutions, {username} values transparency and collaboration, reflecting a forward-thinking mindset."
        )
    }
    # Save avatar
    with open(f"{username}_avatar.json", "w") as f:
        json.dump(avatar, f, indent=2)
    ipfs_hash = None
    if ipfs_client:
        try:
            ipfs_hash = ipfs_client.add(f"{username}_avatar.json")["Hash"]
            avatar["ipfs_hash"] = ipfs_hash
        except Exception as e:
            print(f"Failed to upload avatar to IPFS: {e}")
    return avatar

def generate_trivia(avatar, username):
    questions = []
    categories = {
        "Mindset": [],
        "Career": [],
        "Life Goals": [],
        "Vibe": [],
        "Online Habits": []
    }
    templates = [
        {"category": "Mindset", "questionText": f"What personality trait is {username} most known for?", "options": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness"], "correctAnswer": 0},
        {"category": "Mindset", "questionText": f"What value does {username} prioritize most?", "options": ["Transparency", "Competition", "Tradition", "Security"], "correctAnswer": 0},
        {"category": "Mindset", "questionText": f"What drives {username}’s motivation?", "options": ["Innovation", "Stability", "Fame", "Comfort"], "correctAnswer": 0},
        {"category": "Career", "questionText": f"What is {username}’s top interest?", "options": ["Artificial Intelligence", "Finance", "Sports", "Art"], "correctAnswer": 0},
        {"category": "Career", "questionText": f"What technology does {username} engage with?", "options": ["Blockchain", "Virtual Reality", "Quantum Computing", "Robotics"], "correctAnswer": 0},
        {"category": "Career", "questionText": f"What skill is {username} passionate about?", "options": ["Coding", "Marketing", "Design", "Writing"], "correctAnswer": 0},
        {"category": "Career", "questionText": f"Where does {username} thrive professionally?", "options": ["San Francisco tech scene", "Wall Street", "Hollywood", "Academic research"], "correctAnswer": 0},
        {"category": "Career", "questionText": f"What field excites {username}?", "options": ["Tech Events", "Fashion", "Politics", "Culinary Arts"], "correctAnswer": 0},
        {"category": "Life Goals", "questionText": f"What is {username}’s main goal?", "options": ["Build decentralized solutions", "Start a traditional business", "Become a teacher", "Travel the world"], "correctAnswer": 0},
        {"category": "Life Goals", "questionText": f"What impact does {username} want to have?", "options": ["Advance technology", "Preserve tradition", "Promote art", "Protect environment"], "correctAnswer": 0},
        {"category": "Life Goals", "questionText": f"What does {username} aim to build?", "options": ["Decentralized platforms", "Corporate empires", "Charity organizations", "Social media apps"], "correctAnswer": 0},
        {"category": "Life Goals", "questionText": f"What future does {username} envision?", "options": ["Decentralized internet", "Global corporation", "Sustainable cities", "Space exploration"], "correctAnswer": 0},
        {"category": "Vibe", "questionText": f"How does {username} communicate?", "options": ["Enthusiastic and technical", "Formal and reserved", "Casual and humorous", "Direct and blunt"], "correctAnswer": 0},
        {"category": "Vibe", "questionText": f"What tone does {username} use in posts?", "options": ["Excited", "Sarcastic", "Neutral", "Critical"], "correctAnswer": 0},
        {"category": "Vibe", "questionText": f"What’s {username}’s social vibe?", "options": ["Tech enthusiast", "Corporate professional", "Free spirit", "Activist"], "correctAnswer": 0},
        {"category": "Vibe", "questionText": f"How would friends describe {username}’s energy?", "options": ["Innovative", "Conservative", "Relaxed", "Intense"], "correctAnswer": 0},
        {"category": "Online Habits", "questionText": f"When does {username} typically post about tech?", "options": ["Morning", "Afternoon", "Evening", "Late Night"], "correctAnswer": 2},
        {"category": "Online Habits", "questionText": f"What events does {username} share online?", "options": ["Tech Events", "Music Festivals", "Book Clubs", "Sports Games"], "correctAnswer": 0},
        {"category": "Online Habits", "questionText": f"What’s {username}’s favorite online topic?", "options": ["Web3", "Politics", "Travel", "Food"], "correctAnswer": 0},
        {"category": "Online Habits", "questionText": f"How often does {username} post about coding?", "options": ["Frequently", "Occasionally", "Rarely", "Never"], "correctAnswer": 0}
    ]
    random.shuffle(templates)
    for i, template in enumerate(templates[:20], 1):
        question = {
            "questionText": template["questionText"],
            "options": template["options"],
            "correctAnswer": template["correctAnswer"],
            "category": template["category"],
            "stake_amount": 0.01,
            "reward": 0.02,
            "questionId": i
        }
        categories[template["category"]].append(question)
        questions.append(question)
    output = {
        "username": username,
        "questions": questions,
        "categories": {k: len(v) for k, v in categories.items()}
    }
    # Save trivia
    with open(f"{username}_trivia.json", "w") as f:
        json.dump(output, f, indent=2)
    ipfs_hash = None
    if ipfs_client:
        try:
            ipfs_hash = ipfs_client.add(f"{username}_trivia.json")["Hash"]
            output["ipfs_hash"] = ipfs_hash
        except Exception as e:
            print(f"Failed to upload trivia to IPFS: {e}")
    return output

@app.post("/generateAvatarAndQuestions")
async def generate_avatar_and_questions(request: AvatarRequest):
    username = request.username
    tweets = request.tweets

    if not tweets:
        # Fetch real tweets (limited to 50)
        try:
            auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
            auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
            api = tweepy.API(auth)
            tweets_data = api.user_timeline(screen_name=username, count=50, tweet_mode="extended")
            tweets = [Tweet(text=t.full_text, created_at=str(t.created_at)) for t in tweets_data]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching tweets: {e}")

    # Generate avatar
    avatar = generate_avatar(tweets, username)
    # Generate trivia
    trivia = generate_trivia(avatar, username)
    return {
        "avatar": avatar,
        "trivia": trivia
    }

@app.get("/testTweets/{username}")
async def test_tweets(username: str):
    try:
        auth = tweepy.OAuthHandler(X_API_KEY, X_API_SECRET)
        auth.set_access_token(X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=username, count=50, tweet_mode="extended")
        return [{"text": t.full_text, "created_at": str(t.created_at)} for t in tweets]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)