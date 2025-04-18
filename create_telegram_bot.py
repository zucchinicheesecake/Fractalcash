#!/usr/bin/env python3
"""
Auto‑create a Telegram Bot via BotFather and save its token to bot_token.txt.

Requirements:
  pip install telethon
"""

import asyncio
from telethon import TelegramClient, events

async def main():
    # 1) Prompt for your Telegram API credentials (get from my.telegram.org)
    api_id    = int(input("Enter your Telegram API ID: ").strip())
    api_hash  = input("Enter your Telegram API Hash: ").strip()
    phone     = input("Enter your phone number (e.g. +15551234567): ").strip()

    client = TelegramClient("session_bot_creator", api_id, api_hash)
    await client.start(phone)

    print("\n→ Connected! Now creating your bot via BotFather…")
    bf = await client.get_entity("BotFather")

    # 2) Send /newbot and follow prompts
    await client.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    bot_name = input("Enter a name for your new bot (e.g. FractalCashBot): ").strip()
    await client.send_message(bf, bot_name)
    await asyncio.sleep(1)
    bot_username = input("Enter a username (must end in 'bot', e.g. FractalCash_bot): ").strip()
    await client.send_message(bf, bot_username)

    # 3) Wait for BotFather’s reply containing the token
    token_event = asyncio.Event()
    bot_token = None

    @client.on(events.NewMessage(from_users=bf.id))
    async def handler(ev):
        nonlocal bot_token
        text = ev.message.message
        if "token" in text.lower():
            # extract the token-looking string
            for part in text.split():
                if part.count(":") == 2 and part.startswith("123456"): 
                    # naive pattern: your token always has two ':' separators
                    bot_token = part
                    break
            token_event.set()

    await token_event.wait()
    await client.disconnect()

    if not bot_token:
        print("❌ Failed to parse bot token. Check the BotFather chat.")
        return

    # 4) Save the bot token
    with open("bot_token.txt", "w") as f:
        f.write(bot_token.strip())
    print(f"✅ Bot created! Token saved to bot_token.txt:\n   {bot_token}")

if __name__ == "__main__":
    asyncio.run(main())
