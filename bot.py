from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from telegram import Bot
from telegram.ext import ApplicationBuilder

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

@app.route('/')
def home():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/edit_question', methods=['GET', 'POST'])
def edit_question():
    if request.method == 'POST':
        new_question = request.form.get('new_question')
        # Burada soruları güncelleyebilirsiniz
        # Soruları bir veritabanında tutabiliriz, ancak bu örnekte bir değişkenle gösteriyoruz
        global current_question
        current_question = new_question
        return redirect(url_for('home'))
    return render_template('edit_question.html')

@app.route('/user/<int:id>')
def user_details(id):
    user = User.query.get_or_404(id)
    return render_template('user_details.html', user=user)

if __name__ == '__main__':
    db.create_all()  # Veritabanını oluştur
    app.run(debug=True)
