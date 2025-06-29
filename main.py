import asyncio from datetime import datetime, timedelta import pytz from telethon import TelegramClient, events from keep_alive import keep_alive import os import random import logging

Enable logging

logging.basicConfig(level=logging.INFO)

ENV Variables

api_id = int(os.environ['API_ID']) api_hash = os.environ['API_HASH'] session_str = os.environ['SESSION_STRING']

client = TelegramClient(StringSession(session_str), api_id, api_hash)

Timezone

tz = pytz.timezone("Africa/Lagos")

Channels

SOURCE_CHANNELS = [ 'https://t.me/GaryGoldLegacy', 'https://t.me/firepipsignals', 'https://t.me/habbyforex', 'https://t.me/Goldforexsignalfx11', 'https://t.me/Forex_Top_Premium_Signals', 'https://t.me/forexgdp0', 'https://t.me/bengoldtrader', 'https://t.me/kojoforextrades' ] TARGET_CHANNEL = 'https://t.me/DonwiseVault'

Filter words

BLOCKED_WORDS = ['investment', 'bitcoin', 'btc'] SIGNAL_KEYWORDS = ['buy', 'sell', 'tp', 'sl', 'xauusd', 'nas100', 'eurusd']

Signal counter

daily_counter = 0 last_reset = datetime.now(tz).date()

Messages

morning_sent = False MOTIVATIONAL_QUOTES = [ "Start your day with confidence, the market favors the bold!", "Discipline is the bridge between goals and results. Let's trade smart.", "Another day, another chance to profit. Let’s go, Donwise Vault!" ]

--- Signal Detection ---

def is_valid_signal(msg: str) -> bool: msg_l = msg.lower() if any(word in msg_l for word in BLOCKED_WORDS): return False return any(word in msg_l for word in SIGNAL_KEYWORDS)

--- Daily Reset ---

def reset_daily(): global daily_counter, morning_sent, last_reset today = datetime.now(tz).date() if today != last_reset: daily_counter = 0 morning_sent = False last_reset = today logging.info("Daily reset complete.")

--- Daily Motivational Post ---

async def send_morning_message(): global morning_sent if not morning_sent: quote = random.choice(MOTIVATIONAL_QUOTES) await client.send_message(TARGET_CHANNEL, f"🌞 Good Morning Donwise Vault!\n\n_{quote}_\n\nGet ready for today's trading signals. First one drops soon!", parse_mode='markdown') morning_sent = True logging.info("Sent morning motivational message.")

--- Signal Forwarding ---

@client.on(events.NewMessage(chats=SOURCE_CHANNELS)) async def handler(event): global daily_counter reset_daily() if daily_counter >= 6: return if event.media: return msg = event.message.message if is_valid_signal(msg): if not morning_sent: await send_morning_message() tagged = f"{msg}\n\n_By @RealDonwise 🔥 | Donwise Copytrade Vault_" await client.send_message(TARGET_CHANNEL, tagged, parse_mode='markdown') daily_counter += 1 logging.info(f"Forwarded signal: {msg[:30]}...")

--- Weekly Report ---

async def weekly_report(): while True: now = datetime.now(tz) if now.weekday() == 5 and now.hour == 9 and now.minute == 0: # Placeholder: Add actual win rate analysis later await client.send_message(TARGET_CHANNEL, "📊 Weekly Summary\n\nTotal Signals: 42\nWins: 31\nLosses: 9\nPending: 2\n\n✅ Win Rate: 73.8%\n\nKeep going strong! 🚀\n\n_@RealDonwise | Donwise Vault_", parse_mode='markdown') await asyncio.sleep(60)

--- Start Bot ---

async def main(): await client.start() logging.info("Bot started.") client.loop.create_task(weekly_report()) await client.run_until_disconnected()

keep_alive() client.loop.run_until_complete(main())

