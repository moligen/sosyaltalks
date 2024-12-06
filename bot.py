from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler

# Konuşma adımları
ASK_READY, GET_NAME, GET_SURNAME, GET_PHONE, ASK_TASK, GET_TASK = range(6)

# Kullanıcıya başlangıç sorusu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Evet", "Hayır"]]
    await update.message.reply_text(
        "Göreve hazır mısın?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return ASK_READY

# Kullanıcının cevabını işleme
async def handle_ready(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    if answer == "Evet":
        await update.message.reply_text("Harika! Biraz seni tanıyalım. Adını yazar mısın?")
        return GET_NAME
    else:
        await update.message.reply_text("Cesaretini topla, tekrar gel!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

# Adını alma
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Soyadını yazar mısın?")
    return GET_SURNAME

# Soyadını alma
async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["surname"] = update.message.text
    await update.message.reply_text("Cep telefonu numaranı yazar mısın?")
    return GET_PHONE

# Cep telefonu numarasını alma
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Harika! Şimdi görev sorusuna geçiyoruz. Sadece bir cevap hakkın var:")
    await update.message.reply_text("Görev: 5 + 3 = ?")
    return GET_TASK

# Görev cevabını alma
async def get_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    task_answer = update.message.text
    context.user_data["task_answer"] = task_answer

    await update.message.reply_text(
        f"Cevabın kaydedildi: {task_answer}. Görev tamamlandı!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Konuşmayı iptal etme
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Görev iptal edildi. Tekrar görüşmek üzere!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# Botu başlat
if __name__ == "__main__":
    BOT_TOKEN = "7973150966:AAGttJKka-imvBWOqnBn4bxqfvLBid3Smok"

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Konuşma işleyicisi
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_READY: [MessageHandler(filters.Regex("^(Evet|Hayır)$"), handle_ready)],
            GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            GET_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_surname)],
            GET_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            GET_TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot çalışıyor...")
    app.run_polling()
