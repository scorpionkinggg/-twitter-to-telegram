import os
import time
import ssl
import certifi
import subprocess

# ================= SSL FIX FOR REQUESTS + SNSCRAPE =================

# Set certifi for SSL
os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl.create_default_context

# Patch urllib3 + requests with certifi certs
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class CertifiSSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl.create_default_context(cafile=certifi.where())
        return super().init_poolmanager(*args, **kwargs)

import requests
session = requests.Session()
adapter = CertifiSSLAdapter()
session.mount('https://', adapter)
session.mount('http://', adapter)

# Patch snscrape to use this requests session
import snscrape.base
snscrape.base._session = session

# ================== REGULAR IMPORTS =====================

from telegram import Bot
from dotenv import load_dotenv

# === Load environment variables ===
print("📦 Starting script...")
load_dotenv()
print("🔧 Loaded .env variables")

# === CONFIG ===
TWITTER_USERS = [
    "coinotagen", "FarsideUK", "bwenews", "BSCNheadlines",
    "lookonchain", "TreeNewsFeed", "WuBlockchain", "whale_alert"
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

print(f"🧪 BOT_TOKEN: {'SET' if BOT_TOKEN else 'MISSING'}")
print(f"🧪 TARGET_CHAT_ID: {'SET' if TARGET_CHAT_ID else 'MISSING'}")

if not BOT_TOKEN or not TARGET_CHAT_ID:
    print("❌ Missing BOT_TOKEN or TARGET_CHAT_ID")
    exit(1)

TARGET_CHAT_ID = int(TARGET_CHAT_ID)
bot = Bot(token=BOT_TOKEN)
seen_tweets = set()

print("🚀 Twitter-to-Telegram bot is running...")

# === Fetch Latest Tweet ===
def fetch_latest_tweet(username):
    try:
        print(f"👀 Checking user: @{username}")
        cmd = f"snscrape --max-results 1 twitter-user '{username}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        tweet = result.stdout.strip()
        if tweet:
            lines = tweet.splitlines()
            tweet_text = lines[0]
            tweet_id = tweet.split()[-1]  # crude but often works with snscrape output
            return tweet_text, tweet_id
        return None, None

    except Exception as e:
        print(f"❌ Scrape error for @{username}: {e}")
        return None, None

# === Main Loop ===
while True:
    for user in TWITTER_USERS:
        tweet_text, tweet_id = fetch_latest_tweet(user)
        if tweet_id and tweet_id not in seen_tweets:
            seen_tweets.add(tweet_id)
            print(f"✅ New tweet from @{user}: Posting to Telegram.")
            try:
                bot.send_message(chat_id=TARGET_CHAT_ID, text=f"🧵 @{user}:\n{tweet_text}")
            except Exception as e:
                print(f"🚨 Failed to send Telegram message: {e}")
        else:
            print(f"⚠️ Skipping @{user} — no new tweet or fetch error.")
    time.sleep(15)  # Check every 15 seconds
