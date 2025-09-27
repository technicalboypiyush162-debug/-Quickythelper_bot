# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random

TOKEN = "8439564853:AAGkCnfCiNfmKIsu9yU68UXzXYv1lJ7E_vc"
# --- Start Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("✅ I Subscribed", callback_data="subscribed")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome! Pehle mera YouTube channel subscribe karo ❤️\n"
        "👉 [Teach With Piyush](https://youtube.com/@teachwithpiyush?si=jV16crytzwSpLHoo)\n\n"
        "Phir neeche button dabao:",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

# --- Handle Button Clicks ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "subscribed":
        keyboard = [
            [InlineKeyboardButton("🎬 Titles", callback_data="titles"),
             InlineKeyboardButton("🏷️ Tags", callback_data="tags")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("✅ Shukriya subscribe karne ke liye!\nAb choose karo:", reply_markup=reply_markup)

    elif query.data == "titles":
        context.user_data["mode"] = "titles"
        await query.edit_message_text("🎬 Apna video title bhejo, main usko improve karke naya title dunga + tags bhi.")
    elif query.data == "tags":
        context.user_data["mode"] = "tags"
        await query.edit_message_text("🏷️ Apna video title bhejo, main uske liye tags generate karunga.")

# --- Handle User Messages ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    mode = context.user_data.get("mode")

    if mode == "titles":
        # Improved title suggestions
        improved_titles = [
            f"{user_text} | Ultimate Guide for Creators",
            f"How to {user_text} in 2025 (Pro Tips)",
            f"{user_text} Explained Step by Step",
            f"Boost Your Views with {user_text}",
            f"Secrets About {user_text} You Must Know!"
        ]
        new_title = random.choice(improved_titles)

        # Generate more tags (10+)
        words = user_text.split()
        tags = [f"#{w.capitalize()}" for w in words if len(w) > 3]
        extra_tags = ["#YouTubeTips", "#ContentCreation", "#ViralVideos", "#TeachWithPiyush", "#YouTubeGrowth"]
        tags = tags + random.sample(extra_tags, min(5, len(extra_tags)))

        await update.message.reply_text(
            f"🎬 Suggested Title:\n{new_title}\n\n"
            f"🏷️ Tags:\n{' '.join(tags)}"
        )

    elif mode == "tags":
        words = user_text.split()
        tags = [f"#{w.capitalize()}" for w in words if len(w) > 3]
        if len(tags) < 8:
            tags += ["#YouTube", "#SEO", "#ContentCreator", "#TeachWithPiyush", "#Trending", "#Viral"]
        await update.message.reply_text(f"🏷️ Suggested Tags:\n{' '.join(tags)}")

    else:
        await update.message.reply_text("👉 Pehle /start dabao aur option choose karo.")

# --- Main Function ---
def main():
    app = Application.builder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 YouTube Assistant Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
