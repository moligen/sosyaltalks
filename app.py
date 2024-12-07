from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Conversation states
NAME, SURNAME, EMAIL = range(3)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Merhaba! Kişisel bilgilerinizi toplamak için buradayım. İlk olarak, adınızı paylaşır mısınız?"
    )
    return NAME

# Collect name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Teşekkürler! Şimdi soyadınızı paylaşır mısınız?")
    return SURNAME

# Collect surname
async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['surname'] = update.message.text
    await update.message.reply_text("Son olarak, e-posta adresinizi paylaşır mısınız?")
    return EMAIL

# Collect email
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['email'] = update.message.text
    
    # Display collected information
    name = context.user_data['name']
    surname = context.user_data['surname']
    email = context.user_data['email']
    
    await update.message.reply_text(
        f"Teşekkürler! İşte topladığımız bilgiler:\n"
        f"Ad: {name}\n"
        f"Soyad: {surname}\n"
        f"E-posta: {email}\n"
    )
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("İşlem iptal edildi. Tekrar görüşmek üzere!")
    return ConversationHandler.END

# Main function
def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot's API token
    application = Application.builder().token("7973150966:AAGttJKka-imvBWOqnBn4bxqfvLBid3Smok").build()

    # Conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
