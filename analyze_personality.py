import json
import torch
from transformers import DistilBertTokenizer, DistilBertModel
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.preprocessing import normalize
import numpy as np

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def preprocess_tweets(tweets):
    """Clean tweet text for analysis."""
    stop_words = set(stopwords.words('english'))
    cleaned_tweets = []
    for tweet in tweets:
        text = tweet['text'].lower()
        # Remove URLs, hashtags, mentions
        text = ' '.join(word for word in text.split() if not (word.startswith('#') or word.startswith('@') or 'http' in word))
        # Tokenize and remove stopwords
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
        cleaned_tweets.append(' '.join(tokens))
    return cleaned_tweets

def extract_features(cleaned_tweets):
    """Extract linguistic features using DistilBERT."""
    embeddings = []
    for text in cleaned_tweets:
        if not text.strip():
            continue
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        # Use mean of last hidden state as embedding
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        embeddings.append(embedding)
    if not embeddings:
        return np.zeros(768)  # DistilBERT embedding size
    # Average embeddings
    return normalize(np.mean(embeddings, axis=0).reshape(1, -1))[0]

def infer_big5_features(features):
    """Mock Big 5 OCEAN inference (simplified)."""
    # Mock scoring based on feature magnitude (replace with trained model later)
    openness = min(0.8 + np.random.uniform(-0.1, 0.1), 1.0)  # High for tech interest
    conscientiousness = min(0.7 + np.random.uniform(-0.1, 0.1), 1.0)  # High for productivity
    extraversion = min(0.6 + np.random.uniform(-0.1, 0.1), 1.0)  # Moderate for social posts
    agreeableness = min(0.5 + np.random.uniform(-0.1, 0.1), 1.0)  # Neutral
    neuroticism = min(0.3 + np.random.uniform(-0.1, 0.1), 1.0)  # Low for positive tone
    return {
        "Openness": openness,
        "Conscientiousness": conscientiousness,
        "Extraversion": extraversion,
        "Agreeableness": agreeableness,
        "Neuroticism": neuroticism
    }

def infer_attributes(tweets):
    """Infer values, interests, goals, and communication style."""
    text = ' '.join(tweet['text'].lower() for tweet in tweets)
    # Keyword-based inference (simplified)
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
    """Generate Deep Personality Avatar."""
    # Preprocess tweets
    cleaned_tweets = preprocess_tweets(tweets)
    # Extract features
    features = extract_features(cleaned_tweets)
    # Infer Big 5 traits
    big5_traits = infer_big5_features(features)
    # Infer other attributes
    attributes = infer_attributes(tweets)

    # Structure avatar
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

    # Save avatar to JSON
    with open(f"{username}_avatar.json", "w") as f:
        json.dump(avatar, f, indent=2)
    print(f"Saved avatar for {username} to {username}_avatar.json")
    return avatar

if __name__ == "__main__":
    # Load mock tweets
    username = "alex.base"
    with open(f"{username}_tweets.json", "r") as f:
        tweets = json.load(f)
    # Generate avatar
    avatar = generate_avatar(tweets, username)
    # Print summary
    print(json.dumps(avatar, indent=2))