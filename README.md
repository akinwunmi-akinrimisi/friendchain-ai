FriendChain AI
A Web3 social trivia game that decodes user personalities from X tweets and creates fun, dynamic trivia games on the Base blockchain.
Overview
The Personality Decoder Buddy analyzes up to 50 tweets to generate:

A personality report with Big Five traits, nickname, posting style, motto, superpower, and quirk.
15 dynamic trivia questions for a "How well do you know [user]?" game, divided into 3 stages (5 questions each).
Data stored on IPFS, with CIDs on the Base testnet smart contract.

Players stake ~$10 in ETH (0.003 ETH placeholder) to play, with stage-based refunds:

Stage 1 (Q1–5): 30% refund (0.0009 ETH).
Stage 2 (Q6–10): 70% refund (0.0021 ETH).
Stage 3 (Q11–15): 100% refund (0.003 ETH).Prize pool (lost stakes + optional creator reward) is shared: 50% (1st), 30% (2nd), 15% (3rd), 10% (creator), 5% (platform).

Setup

Install Dependencies:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Install IPFS (kubo v0.7.0):
wget https://github.com/ipfs/kubo/releases/download/v0.7.0/go-ipfs_v0.7.0_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.7.0_linux-amd64.tar.gz
cd go-ipfs
sudo bash install.sh
ipfs init
ipfs daemon &

Note: Currently using kubo v0.30.0; upgrade to v0.7.0 to resolve version mismatch.

Set X API Credentials:

Update main.py with your X API key (for real tweets, not implemented yet).


Run FastAPI:
uvicorn main:app --host 0.0.0.0 --port 8000



Endpoints

POST /generateAvatarAndQuestions
Input:{
  "username": "string",
  "tweets": [
    { "text": "string", "created_at": "string" }
  ]
}


Output: Personality report and 15 trivia questions with IPFS hashes.


GET /testTweets/{username}
Output: Mock tweets for testing (due to 0/100 X API limit).



Notes

Uses ~50 tweets/user (100-tweet X API limit).
IPFS stores username_personality.json and username_trivia.json.
Staking: ~$10 ETH (0.003 ETH) for 15 questions, with stage-based refunds.
Prize pool: Distributed to top 3 winners, creator, and platform (5% fee).
Base testnet for MVP.
Current issue: kubo v0.30.0 causes version mismatch; upgrade to v0.7.0.
Uses nlptown/bert-base-multilingual-uncased-sentiment for sentiment analysis.

Next Steps

Resolve kubo v0.7.0 installation.
Test with real tweets.
Deploy smart contract (FriendChain.sol).
Deploy to Vercel.

