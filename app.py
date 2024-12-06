from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite veritabanı
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Kullanıcı modelini tanımla
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    task_answer = db.Column(db.String(100), nullable=False)

# Telegram bot token
BOT_TOKEN = "7973150966:AAGttJKka-imvBWOqnBn4bxqfvLBid3Smok"
bot = Bot(BOT_TOKEN)

# Başlangıçta gösterilen soru
current_question = "Görev: 5 + 3 = ?"

@app.route('/')
def home():
    # Tüm kullanıcıları listele
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/edit_question', methods=['GET', 'POST'])
def edit_question():
    global current_question
    if request.method == 'POST':
        new_question = request.form.get('new_question')
        # Soruyu güncelle
        current_question = new_question
        return redirect(url_for('home'))
    return render_template('edit_question.html', current_question=current_question)

@app.route('/user/<int:id>')
def user_details(id):
    # Kullanıcı detaylarını görüntüle
    user = User.query.get_or_404(id)
    return render_template('user_details.html', user=user)

# Telegram bot komutlarını ekleme
async def start(update, context):
    reply_keyboard = [["Evet", "Hayır"]]
    await update.message.reply_text(
        "Göreve hazır mısın?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )

async def handle_ready(update, context):
    answer = update.message.text
    if answer == "Evet":
        await update.message.reply_text("Harika! Adını yazar mısın?")
        return GET_NAME
    else:
        await update.message.reply_text("Tekrar gel!", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

# Telegram Botu başlatmak için asenkron bir işlem
def run_telegram_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tabloyu oluştur
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
