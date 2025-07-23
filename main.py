import os
import time
import subprocess
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
TWITTER_USERS = [
    "coinotagen", "FarsideUK", "bwenews", "BSCNheadlines",
    "lookonchain", "TreeNewsFeed", "WuBlockchain", "whale_alert"
]

BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))
bot = Bot(token=BOT_TOKEN)
seen_tweets = set()

print("🚀 Twitter-to-Telegram bot is running...")

def fetch_latest_tweet(username):
    try:
        print(f"👀 Checking user: @{username}")
        cmd = f"snscrape --max-results 1 twitter-user '{username}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        tweet = result.stdout.strip()
        if tweet:
            tweet_id = tweet.split()[-1]
            return tweet, tweet_id
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
