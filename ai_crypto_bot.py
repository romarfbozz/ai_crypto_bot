import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "7384247990:AAEBad20wB0R30DNaORfwL3u5x8mtuz_MEU"
OPENAI_KEY = "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"

def ask_openai(question: str) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": question}],
        "temperature": 0.7,
        "max_tokens": 500,
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        answer = response.json()["choices"][0]["message"]["content"]
        return answer.strip()
    except Exception as e:
        return f"⚠️ Ошибка OpenAI API: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(f"💬 Получено сообщение: {user_msg}")
    reply = ask_openai(user_msg)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 ИИ агент запущен")
    app.run_polling()
