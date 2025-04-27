# FriendChain AI

A Web3 social trivia game generating avatars and questions from X tweets.

## Setup
1. Install: `pip install -r requirements.txt` (ensure `ipfshttpclient==0.7.0`)
2. Set X API credentials in `main.py`.
3. Install IPFS (kubo v0.7.0):
   ```bash
   wget https://github.com/ipfs/kubo/releases/download/v0.7.0/go-ipfs_v0.7.0_linux-amd64.tar.gz
   tar -xvzf go-ipfs_v0.7.0_linux-amd64.tar.gz
   cd go-ipfs
   sudo bash install.sh
   ipfs init