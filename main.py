import os
import time
import feedparser
from telegram import Bot

# ======================
# 🔴 تنظیمات اصلی
# ======================
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

# ======================
# 🟢 RSS خبرگزاری‌ها
# ======================
RSS_FEEDS = [
    "https://www.irna.ir/rss",
    "https://www.isna.ir/rss",
    "https://www.jamaran.news/fa/rss/allnews",
    "https://www.mehrnews.com/rss",
    "https://www.farsnews.ir/rss",
]

# ======================
# 🟡 کلمات کلیدی لنگه‌وند
# ======================
KEYWORDS = [
    "بندرلنگه",
    "هرمزگان",
    "قشم",
    "بندرعباس",
    "خلیج فارس",
    "دریا",
    "صیادی",
    "سوخت",
    "قاچاق",
]

# ======================
# جلوگیری از تکرار خبر
# ======================
sent = set()

# ======================
# بررسی خبرها
# ======================
def check_news():
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:
            title = entry.title
            link = entry.link

            # جلوگیری از ارسال تکراری
            if link in sent:
                continue

            # فیلتر هوشمند محلی
            if any(word in title for word in KEYWORDS):
                message = f"""📰 لنگه‌وند | خبر تازه

{title}

🔗 {link}
"""
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                    sent.add(link)
                except Exception as e:
                    print("Error:", e)

# ======================
# حلقه اصلی
# ======================
print("Bot is running...")

while True:
    check_news()
    time.sleep(300)  # هر 5 دقیقه
