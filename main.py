import os
import time
import ssl
import certifi

# === SSL FIX ===
os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl.create_default_context
print(f"🔒 Using cert file: {os.environ['SSL_CERT_FILE']}")

# === Imports ===
import snscrape.modules.twitter as sntwitter
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

# === Fetch tweet via snscrape native API ===
def fetch_latest_tweet(username):
    try:
        print(f"👀 Checking user: @{username}")
        scraper = sntwitter.TwitterUserScraper(username)
        tweet = next(scraper.get_items(), None)
        if tweet:
            return tweet.content, str(tweet.id)
        return None, None
    except Exception as e:
        print(f"❌ Error scraping @{username}: {e}")
        return None, None

# === Main loop ===
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
    time.sleep(15)  # Wait before next round
