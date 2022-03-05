from flask import Flask, session, redirect, url_for, request
from flask import render_template
import locale
from models.db import db
from models.news import News
from sqlalchemy import desc

from models.raiting import Rating
from models.subject import Subject
from models.user import User

locale.setlocale(locale.LC_TIME, 'ru_RU')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///identifier.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = 'static/img/news/'
app.secret_key = 'oqhgfqwe;lawkjehg[0y2h4b[]'

db.init_app(app)


@app.route('/')
def main_page():
    news = News.query.order_by(desc(News.date)).limit(3)

    return render_template('main_page.html', news=news)


@app.route('/news/<int:news_id>')
def news_page(news_id):
    news = News.query.get(news_id)

    if news is None:
        return 'Новость не найдена'

    return render_template('news.html', news=news)


def format_datetime(value, format="%e %B %Y"):
    if value is None:
        return ""
    return value.strftime(format)


app.jinja_env.filters['formatdatetime'] = format_datetime


@app.route('/auth', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user is None:
            return render_template('auth.html', error=True, email=email)
        else:
            # все хорошо, авторизуем
            session['userId'] = user.id

            if user.is_teacher:
                session['teacher'] = True

                return redirect(url_for('add_news_page'))

            return redirect(url_for('journal_page'))

    if request.method == "GET":
        return render_template('auth.html')


@app.route('/journal')
def journal_page():
    from itertools import groupby

    def grouper(rating):
        return rating.subject.name

    user_id = session.get('userId')
    user = User.query.get(user_id)

    if user is None:
        return redirect(url_for('login_page'))

    ratings = groupby(sorted(user.ratings, key=grouper), key=grouper)

    return render_template('rating.html', data=ratings, user=user)


@app.route('/rating')
def rating_page():
    user_id = session.get('userId')

    if user_id is None:
        return redirect(url_for('login_page'))

    users = []

    for user in User.query.filter_by(is_teacher=0):
        sum = 0
        rating = 0

        if len(user.ratings) > 0:
            for r in user.ratings:
                sum += r.score
            rating = sum / len(user.ratings)

        user_data = {
            'user': user,
            'rating': rating
        }

        def grouped(user_data):
            return user_data['rating']

        users.append(user_data)

    return render_template('rat.html', users=sorted(users, key=grouped, reverse=True), user_id=user_id)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news_page():
    if request.method == 'POST':
        import string
        import random
        import os

        text = request.form['text']
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']

        file_ext = file.filename.rsplit('.', 1)[1].lower()
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)) + '.' + file_ext

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        news = News(title=title, description=description, text=text, img=filename)

        db.session.add(news)
        db.session.commit()

        return redirect('/news/' + str(news.id))

    if 'teacher' in session:
        return render_template('add_news.html')
    else:
        return redirect(url_for('login_page'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('userId', None)
    session.pop('teacher', None)

    return redirect(url_for('main_page'))


@app.route('/all_news')
def all_news_page():
    news = News.query.all()

    return render_template('all_news.html', news=news)


@app.route('/add_score', methods=['POST', 'GET'])
def add_score_page():
    subjects = Subject.query.all()
    students = User.query.order_by(User.name, User.id).filter_by(is_teacher=0)

    if request.method == 'POST':

        name_id = request.form['choice_of_students']
        id_subject = request.form['choice_of_subject']
        score = request.form['choice_of_score']

        new_score = Rating(subject_id=id_subject, user_id=name_id, score=score)

        db.session.add(new_score)
        db.session.commit()

    if 'teacher' in session:
        return render_template('add_score.html', subjects=subjects, students=students)
    else:
        return redirect(url_for('login_page'))

