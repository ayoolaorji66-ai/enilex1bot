import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

# Your social media information
CHANNEL_LINK = "https://t.me/DeFiAuthority23"
GROUP_LINK = "https://t.me/DeFiAuthority2"
TWITTER_USERNAME = "@OrjiAyoola"

# Conversation states
TASKS, TWITTER, WALLET = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_msg = f"""Hello {user.first_name}! 🎉
    
To qualify for the Mr Enilex airdrop, please complete these tasks:

1. Join our Telegram channel: {CHANNEL_LINK}
2. Join our Telegram group: {GROUP_LINK}
3. Follow our Twitter: {TWITTER_USERNAME}

Click 'DONE' after completing all tasks."""

    keyboard = [['DONE']]
    await update.message.reply_text(
        welcome_msg,
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True),
        disable_web_page_preview=True
    )
    return TASKS

async def check_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please share your Twitter username (e.g., @username):",
        reply_markup=ReplyKeyboardRemove()
    )
    return TWITTER

async def twitter_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    twitter_handle = update.message.text
    context.user_data['twitter'] = twitter_handle
    
    await update.message.reply_text(
        "Now please submit your Solana wallet address:"
    )
    return WALLET

async def wallet_submit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sol_wallet = update.message.text
    context.user_data['wallet'] = sol_wallet
    
    congratulation_msg = f"""
🎉 Congratulations! You've qualified for the Mr Enilex airdrop!

10 SOL will be sent to:
{sol_wallet}

Well done! Hope you didn't cheat the system 😉

Note: This is a test bot. No actual SOL will be sent.
    """
    
    await update.message.reply_text(congratulation_msg)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Process cancelled. Type /start to begin again.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    # Your bot token (in production, use environment variables)
    token = "8187045896:AAEYU-jaRKV_pqbFcK9TdXI6mGgI9iOloqM"
    
    app = Application.builder().token(token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            TASKS: [MessageHandler(filters.Regex('^DONE$'), check_tasks)],
            TWITTER: [MessageHandler(filters.TEXT & ~filters.COMMAND, twitter_submit)],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, wallet_submit)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    app.add_handler(conv_handler)
    
    # Start the bot (use polling for testing, webhook for production)
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
