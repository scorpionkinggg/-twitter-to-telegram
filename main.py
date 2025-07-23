import os
import time
import subprocess
from telegram import Bot
from dotenv import load_dotenv

print("📦 Starting script...")  # Initial launch log

load_dotenv()
print("🔧 Loaded .env variables")  # Confirm .env is loaded

# === CONFIG ===
TWITTER_USERS = [
    "coinotagen", "FarsideUK", "bwenews", "BSCNheadlines",
    "lookonchain", "TreeNewsFeed", "WuBlockchain", "whale_alert"
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

print(f"🧪 BOT_TOKEN: {BOT_TOKEN}")
print(f"🧪 TARGET_CHAT_ID: {TARGET_CHAT_ID}")

if not BOT_TOKEN or not TARGET_CHAT_ID:
    print("❌ Missing BOT_TOKEN or TARGET_CHAT_ID")
    exit(1)

TARGET_CHAT_ID = int(TARGET_CHAT_ID)
bot = Bot(token=BOT_TOKEN)
seen_tweets = set()

print("🚀 Twitter-to-Telegram bot is running...")

import snscrape.modules.twitter as sntwitter

def fetch_latest_tweet(username):
    try:
        print(f"👀 Checking user: @{username}")
        for tweet in sntwitter.TwitterUserScraper(username).get_items():
            return tweet.content, str(tweet.id)
        return None, None
    except Exception as e:
        print(f"❌ Error scraping @{username}: {e}")
        return None, None

while True:
    for user in TWITTER_USERS:
        tweet_text, tweet_id = fetch_latest_tweet(user)
        if tweet_id and tweet_id not in seen_tweets:
            seen_tweets.add(tweet_id)
            print(f"✅ New tweet from @{user}: Posting to Telegram.")
            try:
                bot.send_message(chat_id=TARGET_CHAT_ID, text=tweet_text)
            except Exception as e:
                print(f"🚨 Failed to send Telegram message: {e}")
        else:
            print(f"⚠️ Skipping @{user} — no new tweet or fetch error.")
    time.sleep(15)  # check every 15 seconds
