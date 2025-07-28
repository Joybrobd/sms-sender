sms_bot.py

import logging from aiogram import Bot, Dispatcher, executor, types from aiogram.types import ParseMode from filters import bad_words
API_TOKEN = '8441283363:AAFDUl1lpl0CAhOTl7brLPWh_9ZKw_oLcrA'
USERS = {}
ADMINS = [6556220592]  # Replace with your own Telegram user ID
SMS_NUMBER, SMS_MESSAGE = range(2)

def is_admin(user_id):
    return user_id in ADMINS

Configure logging

logging.basicConfig(level=logging.INFO)

Initialize bot and dispatcher

bot = Bot(token=API_TOKEN) dp = Dispatcher(bot)

In-memory database

users = {}  # user_id: {"name": str, "coins": int, "permission": bool, "mute": bool}

Telegram group links

GROUP_LINK_1 = "https://t.me/bdjoybro" GROUP_LINK_2 = "https://t.me/+gSJ3BansNbAwODhl"

SMS API URL

API_URL = "https://hl-hadi.info.gf/cmsg/api.php" API_KEY = "parvej"

def is_bad_message(text): text = text.lower() return any(word in text for word in bad_words)

def get_user(uid): if uid not in users: users[uid] = {"name": "Unknown", "coins": 0, "permission": False, "mute": False} return users[uid]

@dp.message_handler(commands=['start']) async def send_welcome(message: types.Message): uid = message.from_user.id user = get_user(uid) user["name"] = message.from_user.full_name

welcome_msg = (
    "<b>🌟 Welcome to TEAM Jubair  SMS Bot!</b>\n\n"
    "👉 Before using the bot, please join our groups:\n"
    f"🔹 <a href='{GROUP_LINK_1}'>Join Group 1</a>\n"
    f"🔹 <a href='{GROUP_LINK_2}'>Join Group 2</a>\n\n"
    "Type /insight to see available commands ✨"
)
await message.reply(welcome_msg, parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['balance']) async def check_balance(message: types.Message): uid = message.from_user.id user = get_user(uid) await message.reply(f"💰 Your balance: {user['coins']} coin{'s' if user['coins'] != 1 else ''} 🥲")

@dp.message_handler(commands=['insight']) async def insight(message: types.Message): help_text = ( "<b>🧊 Available Commands for Users:</b>\n\n" "1. /start - Start the bot 🌟\n" "2. /sms - Send an SMS (requires permission♡ & 1 coin) 📱\n" "3. /balance - Check your coin balance 💰🥲\n" "4. /insight - Show this list 🧊" ) await message.reply(help_text, parse_mode=ParseMode.HTML)

@dp.message_handler(commands=['sms']) async def send_sms(message: types.Message): uid = message.from_user.id user = get_user(uid)

if user["mute"]:
    await message.reply("🚫 You are muted and cannot send SMS!")
    return

if not user["permission"]:
    await message.reply("⚠️ You don't have permission to send SMS!")
    return

if user["coins"] < 1:
    await message.reply("💰 You need at least 1 coin to send an SMS! 🥲")
    return

args = message.text.split(maxsplit=2)
if len(args) < 3:
    await message.reply("📱 Use format: /sms 01XXXXXXXXX message")
    return

number = args[1]
text = args[2]

if is_bad_message(text):
    await message.reply("🚫 SMS not sent due to bad words detected!")
    return

import urllib.parse, urllib.request
params = urllib.parse.urlencode({
    "key": API_KEY,
    "number": number,
    "msg": text
})
url = f"{API_URL}?{params}"
try:
    with urllib.request.urlopen(url) as response:
        data = response.read()
    user["coins"] -= 1
    await message.reply("✅ SMS sent successfully! 📤")
except Exception as e:
    await message.reply(f"❌ Failed to send SMS: {e}")

if name == 'main': from aiogram import executor executor.start_polling(dp, skip_updates=True)

